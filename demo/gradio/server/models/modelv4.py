from io import BytesIO
import torch
from PIL import Image
import base64
import json
import re
import logging
from transformers import AutoModel, AutoTokenizer, AutoProcessor, set_seed
# set_seed(42)


logger = logging.getLogger(__name__)


class ModelV4:
    def __init__(self, path, multi_gpus=False) -> None:
        self.model = AutoModel.from_pretrained(
            path, trust_remote_code=True, attn_implementation='sdpa', torch_dtype=torch.bfloat16)
        self.model.eval().cuda()
        self.tokenizer = AutoTokenizer.from_pretrained(
            path, trust_remote_code=True)
        self.processor = AutoProcessor.from_pretrained(
            path, trust_remote_code=True)

    def __call__(self, input_data):
        image = None
        # legacy API
        if "image" in input_data and len(input_data["image"]) > 10:
            image = Image.open(BytesIO(base64.b64decode(
                input_data["image"]))).convert('RGB')

        msgs = input_data["question"]
        params = input_data.get("params", "{}")
        params = json.loads(params)
        msgs = json.loads(msgs)
        if params.get("max_new_tokens", 0) > 4096:
            logger.info(f"make max_new_tokens=4096")
            params["max_new_tokens"] = 2048
        if params.get("max_inp_length", 0) > 4352:
            logger.info(f"make max_inp_length=4352")
            params["max_inp_length"] = 4352

        for msg in msgs:
            if 'content' in msg:  # legacy API
                contents = msg['content']
            else:
                contents = msg.pop('contents')

            new_cnts = []
            for c in contents:
                if isinstance(c, dict):
                    if c['type'] == 'text':
                        c = c['pairs']
                    elif c['type'] == 'image':
                        c = Image.open(
                            BytesIO(base64.b64decode(c["pairs"]))).convert('RGB')
                    else:
                        raise ValueError(
                            "contents type only support text and image.")
                new_cnts.append(c)
            msg['content'] = new_cnts
        logger.info(f'msgs: {str(msgs)}')

        answer = self.model.chat(
            image=image,
            msgs=msgs,
            tokenizer=self.tokenizer,
            processor=self.processor,
            **params
        )
        res = re.sub(r'(<box>.*</box>)', '', answer)
        res = res.replace('<ref>', '')
        res = res.replace('</ref>', '')
        res = res.replace('<box>', '')
        answer = res.replace('</box>', '')

        oids = self.tokenizer.encode(answer)
        output_tokens = len(oids)
        return answer, output_tokens
