from pydantic import BaseModel
import uvicorn
import fastapi
from fastapi.responses import StreamingResponse
import argparse
from models import ModelMiniCPMV4, ModelMiniCPMV4_5
import logging
import json

from logging_util import setup_root_logger

logger = logging.getLogger(__name__)


class Model:
    def __init__(self, model_path: str, model_type: str, instance_id: int = 0, gpu_id: int = None) -> None:
        self.instance_id = instance_id
        self.gpu_id = gpu_id
        
        if gpu_id is not None:
            import os
            os.environ['CUDA_VISIBLE_DEVICES'] = str(gpu_id)
            logger.info(f"实例 {instance_id}: 设置CUDA_VISIBLE_DEVICES={gpu_id}")
        
        logger.info(f"实例 {instance_id}: 初始化模型类型 {model_type}")
        
        match model_type.lower():
            case 'minicpmv4':   
                self.model = ModelMiniCPMV4(model_path)
            case 'minicpmv4_5':
                self.model = ModelMiniCPMV4_5(model_path)
            case _:
                raise ValueError(f"Unsupported model type: {model_type}")
        
        logger.info(f"实例 {instance_id}: 模型加载完成")

    def handler(self, query):
        res, output_tokens = self.model({
            "image": query["image"],
            "question": query["question"],
            "params": query.get("params", "{}"),
            "temporal_ids": query.get("temporal_ids", None)
        })
        return {
            "result": res,
            "usage": {"output_tokens": output_tokens}
        }

    def stream_handler(self, query):
        params = json.loads(query.get("params", "{}"))
        params["stream"] = True
        query["params"] = json.dumps(params)
        
        generator = self.model({
            "image": query["image"],
            "question": query["question"],
            "params": query["params"],
            "temporal_ids": query.get("temporal_ids", None)
        })
        
        return generator


class Item(BaseModel):
    image: str
    question: str
    params: str
    temporal_ids: str = None

model = None
args = None

def initialize_server():
    """初始化服务器配置和模型"""
    global model, args
    
    parser = argparse.ArgumentParser(description='Server for MiniCPM-V')
    parser.add_argument('--port', type=int, default=9999,
                        help='Port to run the server on')
    parser.add_argument('--log_dir', type=str, default='logs',
                        help='Directory for log files')
    parser.add_argument('--model_path', type=str, default='openbmb/MiniCPM-V-4_5',
                        help='Path to the model directory')
    parser.add_argument('--model_type', type=str, default='minicpmv4_5',
                        help='Type of the model to use')
    parser.add_argument('--instance_id', type=int, default=0,
                        help='Instance ID for multi-instance deployment')
    parser.add_argument('--gpu_id', type=int, default=None,
                        help='GPU ID to use for this instance')
    args = parser.parse_args()

    setup_root_logger(local_dir=args.log_dir)

    # 打印实例信息
    logger.info(f"="*50)
    logger.info(f"启动MiniCPM-V服务实例")
    logger.info(f"实例ID: {args.instance_id}")
    logger.info(f"GPU ID: {args.gpu_id}")
    logger.info(f"端口: {args.port}")
    logger.info(f"模型路径: {args.model_path}")
    logger.info(f"模型类型: {args.model_type}")
    logger.info(f"日志目录: {args.log_dir}")
    logger.info(f"="*50)

    model = Model(args.model_path, args.model_type, args.instance_id, args.gpu_id)

app = fastapi.FastAPI()


@app.get("/")
def read_root():
    return {
        "message": "MiniCPM-V server", 
        "instance_id": args.instance_id,
        "gpu_id": args.gpu_id,
        "port": args.port,
        "model_type": args.model_type,
        "status": "running"
    }


@app.post("/api")
def websocket(item: Item):
    logger.info(f'params: {str(item.params)}')
    query = item.dict()
    res = model.handler(query)

    logger.info(f'result: {str(res)}')
    return {'data': res}


@app.post("/api/stream")
def stream_api(item: Item):
    query = item.dict()
    def event_generator():
        try:
            generator = model.stream_handler(query)
            full_response = ""
            output_tokens = 0
            
            for chunk in generator:
                full_response += chunk
                output_tokens += 1
                data = {
                    "chunk": chunk,
                    "full_response": full_response,
                    "finished": False
                }
                yield f"data: {json.dumps(data, ensure_ascii=False)}\n\n"
            
            final_data = {
                "chunk": "",
                "full_response": full_response,
                "finished": True
            }
            yield f"data: {json.dumps(final_data, ensure_ascii=False)}\n\n"
            
        except Exception as e:
            error_data = {
                "error": str(e),
                "finished": True
            }
            logger.error(f"Stream error: {e}")
            yield f"data: {json.dumps(error_data, ensure_ascii=False)}\n\n"
    
    return StreamingResponse(
        event_generator(), 
        media_type="text/plain",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*",
        }
    )

if __name__ == "__main__":
    initialize_server()
    
    _cfg = uvicorn.Config(app, host="0.0.0.0", port=args.port, workers=2)
    uvicorn.Server(_cfg).run()
