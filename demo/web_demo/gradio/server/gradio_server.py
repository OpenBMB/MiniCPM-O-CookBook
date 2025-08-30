from pydantic import BaseModel
import uvicorn
import fastapi
import argparse
from models import ModelMiniCPMV4, ModelMiniCPMV4_5
import logging
from logging_util import setup_root_logger

logger = logging.getLogger(__name__)


class Model:
    def __init__(self, model_path: str, model_type: str) -> None:
        match model_type.lower():
            case 'minicpmv4':
                self.model = ModelMiniCPMV4(model_path)
            case 'minicpmv4_5':
                self.model = ModelMiniCPMV4_5(model_path)
            case _:
                raise ValueError(f"Unsupported model type: {model_type}")

    def handler(self, query):
        res, output_tokens = self.model({
            "image": query["image"],
            "question": query["question"],
            "params": query.get("params", "{}")
        })
        return {
            "result": res,
            "usage": {"output_tokens": output_tokens}
        }


class Item(BaseModel):
    image: str
    question: str
    params: str


parser = argparse.ArgumentParser(description='Server for MiniCPM-V 4.0 & 4.5')
parser.add_argument('--port', type=int, default=9999,
                    help='Port to run the server on')
parser.add_argument('--log_dir', type=str, default='logs',
                    help='Directory for log files')
parser.add_argument('--model_path', type=str, default='openbmb/MiniCPM-V-4_5',
                    help='Path to the model directory')
parser.add_argument('--model_type', type=str, default='minicpmv4',
                    help='Type of the model to use')
args = parser.parse_args()

setup_root_logger(local_dir=args.log_dir)

model = Model(args.model_path, args.model_type)

app = fastapi.FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/api")
def websocket(item: Item):
    logger.info(f'params: {str(item.params)}')
    query = item.dict()
    res = model.handler(query)
    logger.info(f'result: {str(res)}')
    return {'data': res}


_cfg = uvicorn.Config(app, host="0.0.0.0", port=args.port, workers=1)
uvicorn.Server(_cfg).run()
