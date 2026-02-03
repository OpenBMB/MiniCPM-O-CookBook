from io import BytesIO
import torch
from PIL import Image
import base64
import json
import re
import logging
from transformers import AutoModel, AutoTokenizer, AutoConfig

logger = logging.getLogger(__name__)

class ModelMiniCPMO4_5:
    def __init__(self, path) -> None:
        # Load config and disable audio/TTS modules, keeping only vision module to save VRAM
        config = AutoConfig.from_pretrained(path, trust_remote_code=True)
        config.init_audio = False  # Disable audio module (Whisper)
        config.init_tts = False    # Disable TTS module
        config.init_vision = True  # Keep vision module
        
        logger.info(f"Loading MiniCPM-o 4.5 with vision-only mode (init_audio={config.init_audio}, init_tts={config.init_tts}, init_vision={config.init_vision})")
        
        self.model = AutoModel.from_pretrained(
            path, config=config, trust_remote_code=True, attn_implementation='sdpa', torch_dtype=torch.bfloat16)
        self.model.eval().cuda()
        self.tokenizer = AutoTokenizer.from_pretrained(
            path, trust_remote_code=True)

    def __call__(self, input_data):
        image = None
        if "image" in input_data and len(input_data["image"]) > 10:
            image = Image.open(BytesIO(base64.b64decode(
                input_data["image"]))).convert('RGB')

        msgs = input_data["question"]
        params = input_data.get("params", "{}")
        params = json.loads(params)
        msgs = json.loads(msgs)
        
        if params.get("max_new_tokens", 0) > 16384:
            logger.info(f"make max_new_tokens=16384, reducing limit to save memory")
            params["max_new_tokens"] = 16384
        if params.get("max_inp_length", 0) > 2048 * 10:
            logger.info(f"make max_inp_length={2048 * 10}, keeping high limit for video processing")
            params["max_inp_length"] = 2048 * 10

        for msg in msgs:
            if 'content' in msg:
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

        enable_thinking = params.pop('enable_thinking', False)
        is_streaming = params.pop('stream', False)
        
        logger.info(f'enable_thinking={enable_thinking} (type={type(enable_thinking).__name__}), is_streaming={is_streaming}')
        
        # Convert sampling param to do_sample (MiniCPM-o 4.5 uses do_sample)
        if 'sampling' in params:
            params['do_sample'] = params.pop('sampling')
        
        # Streaming mode doesn't support beam search, force num_beams=1
        if is_streaming:
            params['num_beams'] = 1
            params['do_sample'] = True
        
        # When thinking mode is disabled, use suppress_tokens to prevent <think> token generation
        # <think> token ID is 151667
        if not enable_thinking:
            params['suppress_tokens'] = [151667]
            logger.info(f'Suppressing <think> token (151667) since enable_thinking=False')
        
        if is_streaming:
            return self._stream_chat(image, msgs, enable_thinking, params)
        else:
            # MiniCPM-o 4.5's chat method doesn't need tokenizer and processor params
            chat_kwargs = {
                "image": image,
                "msgs": msgs,
                "enable_thinking": enable_thinking,
                **params
            }
            
            answer = self.model.chat(**chat_kwargs)

            res = re.sub(r'(<box>.*</box>)', '', answer)
            res = res.replace('<ref>', '')
            res = res.replace('</ref>', '')
            res = res.replace('<box>', '')
            answer = res.replace('</box>', '')
            
            # Log raw output for debugging
            logger.info(f'Raw answer (first 500 chars): {answer[:500] if len(answer) > 500 else answer}')
                
            oids = self.tokenizer.encode(answer)
            output_tokens = len(oids)
            return answer, output_tokens

    def _stream_chat(self, image, msgs, enable_thinking, params): 
        try:
            params['stream'] = True
            # MiniCPM-o 4.5's chat method doesn't need tokenizer and processor params
            chat_kwargs = {
                "image": image,
                "msgs": msgs,
                "enable_thinking": enable_thinking,
                **params
            }
            
            answer_generator = self.model.chat(**chat_kwargs)
            
            if not hasattr(answer_generator, '__iter__'):
                answer = answer_generator
                res = re.sub(r'(<box>.*</box>)', '', answer)
                res = res.replace('<ref>', '')
                res = res.replace('</ref>', '')
                res = res.replace('<box>', '')
                answer = res.replace('</box>', '')
                
                for char in answer:
                    yield char
            else:
                full_answer = ""
                
                for chunk in answer_generator:
                    if isinstance(chunk, str):
                        clean_chunk = re.sub(r'(<box>.*</box>)', '', chunk)
                        clean_chunk = clean_chunk.replace('<ref>', '')
                        clean_chunk = clean_chunk.replace('</ref>', '')
                        clean_chunk = clean_chunk.replace('<box>', '')
                        clean_chunk = clean_chunk.replace('</box>', '')
                        
                        full_answer += chunk
                        yield clean_chunk
                    else:
                        full_answer += str(chunk)
                        yield str(chunk)
                        
        except Exception as e:
            logger.error(f"Stream chat error: {e}")
            yield f"Error: {str(e)}"
