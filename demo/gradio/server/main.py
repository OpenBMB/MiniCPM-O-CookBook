from pydantic import BaseModel
import uvicorn
import fastapi
import os
import sys
import argparse
from models import ModelV4
import logging
from logging_util import setup_root_logger

logger = logging.getLogger(__name__)


class Model:
    def __init__(self, model_token) -> None:
        self.model = ModelV4(model_token, multi_gpus=True)

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


parser = argparse.ArgumentParser(description='Server for MiniCPM-V 4.0')
parser.add_argument('--port', type=int, default=9999,
                    help='Port to run the server on')
parser.add_argument('--log_dir', type=str, default='logs',
                    help='Directory for log files')
args = parser.parse_args()

port = args.port
log_dir = args.log_dir

setup_root_logger(local_dir=log_dir)

model_token = os.environ.get("MODEL_TOKEN", None)
model = Model(model_token)

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


_cfg = uvicorn.Config(app, host="0.0.0.0", port=port, workers=1)
uvicorn.Server(_cfg).run()
