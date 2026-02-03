#!/usr/bin/env python
# encoding: utf-8
import argparse
import gradio as gr
from PIL import Image
from decord import VideoReader, cpu
import io
import os
import copy
import requests
import base64
import json
import traceback
import re
import modelscope_studio as mgr
import time
import uuid

ERROR_MSG = "Error, please retry"
model_name = 'MiniCPM-o 4.5'
disable_text_only = True
MAX_NUM_FRAMES = 64
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}
VIDEO_EXTENSIONS = {'.mp4', '.mkv', '.mov',
                    '.avi', '.flv', '.wmv', '.webm', '.m4v'}
server_url = 'http://127.0.0.1:9999/api' 


def get_file_extension(filename):
    return os.path.splitext(filename)[1].lower()


def is_image(filename):
    return get_file_extension(filename) in IMAGE_EXTENSIONS


def is_video(filename):
    return get_file_extension(filename) in VIDEO_EXTENSIONS


form_radio = {
    'choices': ['Beam Search', 'Sampling'],
    'value': 'Sampling',
    'interactive': True,
    'label': 'Decode Type'
}

thinking_checkbox = {
    'value': False,
    'interactive': True,
    'label': 'Enable Thinking Mode',
}

streaming_checkbox = {
    'value': True,
    'interactive': True,
    'label': 'Enable Streaming Mode',
}


def create_component(params, comp='Slider'):
    if comp == 'Slider':
        return gr.Slider(
            minimum=params['minimum'],
            maximum=params['maximum'],
            value=params['value'],
            step=params['step'],
            interactive=params['interactive'],
            label=params['label']
        )
    elif comp == 'Radio':
        return gr.Radio(
            choices=params['choices'],
            value=params['value'],
            interactive=params['interactive'],
            label=params['label']
        )
    elif comp == 'Button':
        return gr.Button(
            value=params['value'],
            interactive=True
        )
    elif comp == 'Checkbox':
        return gr.Checkbox(
            value=params['value'],
            interactive=params['interactive'],
            label=params['label'],
            info=params.get('info', None)
        )


def update_streaming_mode_state(params_form):
    """
    Update streaming mode state based on decode type
    Beam Search mode forces streaming mode to be disabled
    """
    if params_form == 'Beam Search':
        return gr.update(value=False, interactive=False, info="Beam Search mode does not support streaming output")
    else:
        return gr.update(value=True, interactive=True, info="Enable real-time streaming response")


def stop_streaming(_app_cfg):
    """
    Stop streaming output for current session
    """
    _app_cfg['stop_streaming'] = True
    print(f"[stop_streaming] Set stop flag to True")
    return _app_cfg


def reset_stop_flag(_app_cfg):
    """
    Reset stop flag for current session
    """
    _app_cfg['stop_streaming'] = False
    print(f"[reset_stop_flag] Reset stop flag to False")
    return _app_cfg


def check_and_handle_stop(_app_cfg, context="unknown"):
    """
    Check stop flag and handle
    Returns True if should stop, False to continue
    """
    should_stop = _app_cfg.get('stop_streaming', False)
    is_streaming = _app_cfg.get('is_streaming', False)
    
    if should_stop:
        print(f"[check_and_handle_stop] *** Stop signal detected at {context} ***")
        print(f"[check_and_handle_stop] stop_streaming: {should_stop}, is_streaming: {is_streaming}")
        return True
    return False


def stop_button_clicked(_app_cfg):
    """
    Handle stop button click
    """
    print("[stop_button_clicked] *** Stop button clicked ***")
    print(f"[stop_button_clicked] Current state - is_streaming: {_app_cfg.get('is_streaming', False)}")
    print(f"[stop_button_clicked] Current state - stop_streaming: {_app_cfg.get('stop_streaming', False)}")
    
    _app_cfg['stop_streaming'] = True
    _app_cfg['is_streaming'] = False
    print(f"[stop_button_clicked] Set stop_streaming = True, is_streaming = False")
    
    return _app_cfg, gr.update(visible=False)



def create_multimodal_input(upload_image_disabled=False, upload_video_disabled=False):
    return mgr.MultimodalInput(upload_image_button_props={'label': 'Upload Image', 'disabled': upload_image_disabled, 'file_count': 'multiple'},
                               upload_video_button_props={
                                   'label': 'Upload Video', 'disabled': upload_video_disabled, 'file_count': 'single'},
                               submit_button_props={'label': 'Submit'})


def chat(img_b64, msgs, ctx, params=None, vision_hidden_states=None, session_id=None):
    default_params = {"num_beams": 3,
                      "repetition_penalty": 1.2, "max_new_tokens": 16284}
    if params is None:
        params = default_params

    use_streaming = params.get('stream', False)
    
    if use_streaming:
        return chat_stream(img_b64, msgs, ctx, params, vision_hidden_states, session_id)
    else:
        request_data = {
            "image": img_b64,
            "question": json.dumps(msgs, ensure_ascii=True),
            "params": json.dumps(params, ensure_ascii=True),
        }

        if session_id:
            request_data["session_id"] = session_id
        
        res = requests.post(server_url,
                            headers={
                                "X-Model-Best-Model": "luca-v-online",
                                "X-Model-Best-Trace-ID": "web_demo",
                            },
                            json=request_data)
        if res.status_code != 200:
            print(res.status_code, res.text)
            return -1, ERROR_MSG, None, None
        else:
            try:
                js = res.json()
                raw_result = js['data']['result']
                

                cleaned_result = re.sub(r'(<box>.*</box>)', '', raw_result)
                cleaned_result = cleaned_result.replace('<ref>', '')
                cleaned_result = cleaned_result.replace('</ref>', '')
                cleaned_result = cleaned_result.replace('<box>', '')
                cleaned_result = cleaned_result.replace('</box>', '')
                

                thinking_content_raw, formal_answer_raw = parse_thinking_response(cleaned_result)

                thinking_content_fmt = normalize_text_for_html(thinking_content_raw)
                formal_answer_fmt = normalize_text_for_html(formal_answer_raw)
                formatted_result = format_response_with_thinking(thinking_content_fmt, formal_answer_fmt)


                context_result = formal_answer_raw if formal_answer_raw else cleaned_result
                return 0, formatted_result, context_result, None
            except Exception as e:
                print(e)
                traceback.print_exc()
                return -1, ERROR_MSG, None, None


def chat_stream(img_b64, msgs, ctx, params=None, vision_hidden_states=None, session_id=None):
    """
    Simplified streaming chat function
    """
    try:
        stream_url = server_url.replace('/api', '/api/stream')
        

        request_data = {
            "image": img_b64,
            "question": json.dumps(msgs, ensure_ascii=True),
            "params": json.dumps(params, ensure_ascii=True),
        }

        if session_id:
            request_data["session_id"] = session_id
        

        response = requests.post(
            stream_url,
            headers={
                "X-Model-Best-Model": "luca-v-online",
                "X-Model-Best-Trace-ID": "web_demo",
                "Accept": "text/event-stream",
                "Cache-Control": "no-cache",
            },
            json=request_data,
            stream=True
        )
        
        if response.status_code != 200:
            print(f"Stream request failed: {response.status_code}, falling back to non-stream mode")

            fallback_params = params.copy()
            fallback_params['stream'] = False
            return chat(img_b64, msgs, ctx, fallback_params, vision_hidden_states, session_id)
        

        full_response = ""
        for line in response.iter_lines(decode_unicode=True):
            if line and line.startswith('data: '):
                try:
                    data_str = line[6:]
                    data = json.loads(data_str)
                    
                    if 'error' in data:
                        print(f"Stream error: {data['error']}")
                        return -1, ERROR_MSG, None, None
                    
                    if data.get('finished', False):
                        full_response = data.get('full_response', full_response)
                        break
                    else:
                        full_response = data.get('full_response', full_response)
                
                except json.JSONDecodeError:
                    continue
        
        if not full_response:
            return -1, ERROR_MSG, None, None
        

        cleaned_result = re.sub(r'(<box>.*</box>)', '', full_response)
        cleaned_result = cleaned_result.replace('<ref>', '')
        cleaned_result = cleaned_result.replace('</ref>', '')
        cleaned_result = cleaned_result.replace('<box>', '')
        cleaned_result = cleaned_result.replace('</box>', '')
        

        thinking_content_raw, formal_answer_raw = parse_thinking_response(cleaned_result)
        thinking_content_fmt = normalize_text_for_html(thinking_content_raw)
        formal_answer_fmt = normalize_text_for_html(formal_answer_raw)
        formatted_result = format_response_with_thinking(thinking_content_fmt, formal_answer_fmt)
        

        context_result = formal_answer_raw if formal_answer_raw else cleaned_result
        return 0, formatted_result, context_result, None
        
    except Exception as e:
        print(f"Stream chat error: {e}")
        traceback.print_exc()
        # Fallback to non-streaming mode
        fallback_params = params.copy()
        fallback_params['stream'] = False
        return chat(img_b64, msgs, ctx, fallback_params, vision_hidden_states, session_id)


def encode_image(image):
    if not isinstance(image, Image.Image):
        if hasattr(image, 'path'):
            image = Image.open(image.path)
        elif hasattr(image, 'file') and hasattr(image.file, 'path'):
            image = Image.open(image.file.path)
        elif hasattr(image, 'name'):
            image = Image.open(image.name)
        else:

            image_path = getattr(image, 'url', getattr(image, 'orig_name', str(image)))
            image = Image.open(image_path)
    # resize to max_size
    max_size = 448*16
    if max(image.size) > max_size:
        w, h = image.size
        if w > h:
            new_w = max_size
            new_h = int(h * max_size / w)
        else:
            new_h = max_size
            new_w = int(w * max_size / h)
        image = image.resize((new_w, new_h), resample=Image.BICUBIC)
        # image = image.resize((448, 448), resample=Image.BICUBIC)
    # save by BytesIO and convert to base64
    buffered = io.BytesIO()
    image.save(buffered, format="png")
    im_b64 = base64.b64encode(buffered.getvalue()).decode()
    return [{"type": "image", "pairs": im_b64}]


def encode_video(video):
    """Simple video encoding function"""
    def uniform_sample(l, n):
        gap = len(l) / n
        idxs = [int(i * gap + gap / 2) for i in range(n)]
        return [l[i] for i in idxs]

    if hasattr(video, 'path'):
        video_path = video.path
    elif hasattr(video, 'file') and hasattr(video.file, 'path'):
        video_path = video.file.path
    elif hasattr(video, 'name'):
        video_path = video.name
    else:
        video_path = getattr(video, 'url', getattr(video, 'orig_name', str(video)))
    
    vr = VideoReader(video_path, ctx=cpu(0))
    sample_fps = round(vr.get_avg_fps() / 1)  # FPS
    frame_idx = [i for i in range(0, len(vr), sample_fps)]
    if len(frame_idx) >= MAX_NUM_FRAMES:
        frame_idx = uniform_sample(frame_idx, MAX_NUM_FRAMES - 1)
    
    video_frames = vr.get_batch(frame_idx).asnumpy()
    video_frames = [Image.fromarray(v.astype('uint8')) for v in video_frames]
    video_frames = [encode_image(v)[0] for v in video_frames]
    return video_frames


def parse_thinking_response(response_text):
    """
    Parse response text containing <think> tags, separating thinking process and formal answer
    
    Args:
        response_text (str): Complete response text from model
        
    Returns:
        tuple: (thinking_content, formal_answer)
    """

    think_pattern = r'<think>(.*?)</think>'
    

    thinking_matches = re.findall(think_pattern, response_text, re.DOTALL)
    thinking_content = ""
    
    if thinking_matches:

        thinking_content = "\n\n".join(thinking_matches).strip()
        print("thinking_content---:", thinking_content)
        # thinking_content = thinking_matches.strip()
        # print("thinking_content===:", thinking_content)

        formal_answer = re.sub(think_pattern, '', response_text, flags=re.DOTALL).strip()
    else:

        formal_answer = response_text.strip()
    
    return thinking_content, formal_answer


def normalize_text_for_html(text):
    """
    Lightweight normalization of model output:
    - Unify line breaks to \n
    - Compress 3+ consecutive blank lines to 2
    - Remove extra whitespace from line start/end
    - Careful HTML escaping to avoid breaking thinking tags
    Maintain one blank line between paragraphs for readability
    """
    if not text:
        return ""

    text = re.sub(r"[\u200B\u200C\u200D\uFEFF]", "", text)

    lines = [line.strip() for line in text.split("\n")]
    text = "\n".join(lines)
    
    text = text.strip()
    return text


def format_response_with_thinking(thinking_content, formal_answer):
    """
    Format response with visual distinction between thinking process and formal answer
    
    Args:
        thinking_content (str): Thinking process content
        formal_answer (str): Formal answer content
        
    Returns:
        str: Formatted HTML content
    """

    print("thinking_content >>>>>>:", thinking_content)
    print("formal_answer >>>>>>:", formal_answer)

    if thinking_content:
        formatted_response = f"""
<div class="response-container">
<div class="thinking-section">
<div class="thinking-header">think</div>
<div class="thinking-content">{thinking_content}</div>
</div>
<div class="formal-section">
<div class="formal-header">answer</div>
<div class="formal-content">{formal_answer}</div>
</div>
</div>
"""
    else:
        formatted_response = f"""
<div class="response-container">
<div class="formal-section">
<div class="formal-content">{formal_answer}</div>
</div>
</div>
"""

    return "\n" + formatted_response.strip() + "\n"


def check_mm_type(mm_file):
    if hasattr(mm_file, 'path'):
        path = mm_file.path
    elif hasattr(mm_file, 'file') and hasattr(mm_file.file, 'path'):
        path = mm_file.file.path
    elif hasattr(mm_file, 'name'):
        path = mm_file.name
    else:
        path = getattr(mm_file, 'url', getattr(mm_file, 'orig_name', str(mm_file)))
    
    if is_image(path):
        return "image"
    if is_video(path):
        return "video"
    return None


def encode_mm_file(mm_file):
    if check_mm_type(mm_file) == 'image':
        return encode_image(mm_file)
    if check_mm_type(mm_file) == 'video':
        return encode_video(mm_file)
    return None


def encode_message(_question):
    files = _question.files
    question = _question.text
    pattern = r"\[mm_media\]\d+\[/mm_media\]"
    matches = re.split(pattern, question)
    message = []
    
    if len(matches) != len(files) + 1:
        gr.Warning(
            "Number of Images not match the placeholder in text, please refresh the page to restart!")
    assert len(matches) == len(files) + 1

    text = matches[0].strip()
    if text:
        message.append({"type": "text", "pairs": text})
    
    for i in range(len(files)):
        encoded_content = encode_mm_file(files[i])
        if encoded_content:
            message += encoded_content
        
        text = matches[i + 1].strip()
        if text:
            message.append({"type": "text", "pairs": text})
    
    return message


def check_has_videos(_question):
    images_cnt = 0
    videos_cnt = 0
    for file in _question.files:
        if check_mm_type(file) == "image":
            images_cnt += 1
        else:
            videos_cnt += 1
    return images_cnt, videos_cnt


def count_video_frames(_context):
    num_frames = 0
    for message in _context:
        for item in message["contents"]:
            if item["type"] == "image":
                num_frames += 1
    return num_frames


def respond_stream(_question, _chat_bot, _app_cfg, params_form, thinking_mode, streaming_mode):
    """
    Streaming response generator for real-time UI updates
    """
    print(f"[respond_stream] Called with streaming_mode: {streaming_mode}")
    
    _app_cfg['is_streaming'] = True
    _app_cfg['stop_streaming'] = False
    
    if params_form == 'Beam Search':
        streaming_mode = False
        print(f"[respond_stream] Beam Search mode, forcing streaming disabled")
        _app_cfg['is_streaming'] = False
    
    _context = _app_cfg['ctx'].copy()
    encoded_message = encode_message(_question)
    _context.append({'role': 'user', 'contents': encoded_message})

    images_cnt = _app_cfg['images_cnt']
    videos_cnt = _app_cfg['videos_cnt']
    files_cnts = check_has_videos(_question)
    
    if files_cnts[1] + videos_cnt > 1 or (files_cnts[1] + videos_cnt == 1 and files_cnts[0] + images_cnt > 0):
        gr.Warning("Only supports single video file input right now!")
        yield create_multimodal_input(True, True), _chat_bot, _app_cfg, gr.update(visible=False)
        return
        
    if disable_text_only and files_cnts[1] + videos_cnt + files_cnts[0] + images_cnt <= 0:
        gr.Warning("Please chat with at least one image or video.")
        yield create_multimodal_input(False, False), _chat_bot, _app_cfg, gr.update(visible=False)
        return

    if params_form == 'Beam Search':
        params = {
            'sampling': False,
            'num_beams': 3,
            'repetition_penalty': 1.2,
            "max_new_tokens": 16284,
            "enable_thinking": thinking_mode,
            "stream": False
        }
    else:
        params = {
            'sampling': True,
            'top_p': 0.8,
            'top_k': 100,
            'temperature': 0.7,
            'repetition_penalty': 1.03,
            "max_new_tokens": 16284,
            "enable_thinking": thinking_mode,
            "stream": streaming_mode
        }

    if files_cnts[1] + videos_cnt > 0:
        params["max_inp_length"] = 2048 * 10
        params["use_image_id"] = False
        params["max_slice_nums"] = 1

    images_cnt += files_cnts[0]
    videos_cnt += files_cnts[1]

    _chat_bot.append((_question, ""))
    _context.append({"role": "assistant", "contents": [{"type": "text", "pairs": ""}]}) 

    gen = chat_stream_character_generator("", _context[:-1], None, params, None, _app_cfg, _app_cfg['session_id'])
    
    upload_image_disabled = videos_cnt > 0
    upload_video_disabled = videos_cnt > 0 or images_cnt > 0
    
    yield create_multimodal_input(upload_image_disabled, upload_video_disabled), _chat_bot, _app_cfg, gr.update(visible=True)
    
    print(f"[respond_stream] Starting character-level streaming loop")
    char_count = 0
    
    for _char in gen:
        char_count += 1
        
        if check_and_handle_stop(_app_cfg, f"char {char_count}"):
            break
            
        _chat_bot[-1] = (_question, _chat_bot[-1][1] + _char)
        _context[-1]["contents"][0]["pairs"] += _char
        
        if char_count % 20 == 0:
            print(f"[respond_stream] Processed {char_count} chars, stop_flag: {_app_cfg.get('stop_streaming', False)}")
            yield create_multimodal_input(upload_image_disabled, upload_video_disabled), _chat_bot, _app_cfg, gr.update(visible=True)
            
            time.sleep(0.01)
        else:
            yield create_multimodal_input(upload_image_disabled, upload_video_disabled), _chat_bot, _app_cfg, gr.update(visible=True)
    
    if _app_cfg.get('stop_streaming', False):
        print("[respond_stream] Streaming stopped")
    
    final_content = _chat_bot[-1][1]
    thinking_content_raw, formal_answer_raw = parse_thinking_response(final_content)
    thinking_content_fmt = normalize_text_for_html(thinking_content_raw)
    formal_answer_fmt = normalize_text_for_html(formal_answer_raw)
    formatted_result = format_response_with_thinking(thinking_content_fmt, formal_answer_fmt)
    
    _chat_bot[-1] = (_question, formatted_result)
    _context[-1]["contents"][0]["pairs"] = formal_answer_raw if formal_answer_raw else final_content
    
    _app_cfg['ctx'] = _context
    _app_cfg['images_cnt'] = images_cnt
    _app_cfg['videos_cnt'] = videos_cnt
    
    _app_cfg['is_streaming'] = False
    
    upload_image_disabled = videos_cnt > 0
    upload_video_disabled = videos_cnt > 0 or images_cnt > 0
    yield create_multimodal_input(upload_image_disabled, upload_video_disabled), _chat_bot, _app_cfg, gr.update(visible=False)


def respond(_question, _chat_bot, _app_cfg, params_form, thinking_mode, streaming_mode):
    """
    Response function that selects streaming or non-streaming mode
    """
    if 'session_id' not in _app_cfg:
        _app_cfg['session_id'] = uuid.uuid4().hex[:16]
        print(f"[Session] Generated session_id: {_app_cfg['session_id']}")
    
    if params_form == 'Beam Search':
        streaming_mode = False
        print(f"[respond] Beam Search mode, forcing streaming disabled")
    
    if streaming_mode:
        print("[respond] Using streaming mode")
        yield from respond_stream(_question, _chat_bot, _app_cfg, params_form, thinking_mode, streaming_mode)
        return
    
    _context = _app_cfg['ctx'].copy()
    encoded_message = encode_message(_question)
    _context.append({'role': 'user', 'contents': encoded_message})

    images_cnt = _app_cfg['images_cnt']
    videos_cnt = _app_cfg['videos_cnt']
    files_cnts = check_has_videos(_question)
    if files_cnts[1] + videos_cnt > 1 or (files_cnts[1] + videos_cnt == 1 and files_cnts[0] + images_cnt > 0):
        gr.Warning("Only supports single video file input right now!")
        return _question, _chat_bot, _app_cfg, gr.update(visible=False)
    if disable_text_only and files_cnts[1] + videos_cnt + files_cnts[0] + images_cnt <= 0:
        gr.Warning("Please chat with at least one image or video.")
        return _question, _chat_bot, _app_cfg, gr.update(visible=False)
        
    if params_form == 'Beam Search':
        params = {
            'sampling': False,
            'num_beams': 3,
            'repetition_penalty': 1.2,
            "max_new_tokens": 16284,
            "enable_thinking": thinking_mode,
            "stream": False
        }
    else:
        params = {
            'sampling': True,
            'top_p': 0.8,
            'top_k': 100,
            'temperature': 0.7,
            'repetition_penalty': 1.03,
            "max_new_tokens": 16284,
            "enable_thinking": thinking_mode,
            "stream": False
        }

    if files_cnts[1] + videos_cnt > 0:
        params["max_inp_length"] = 2048 * 10
        params["use_image_id"] = False
        params["max_slice_nums"] = 1

    code, _answer, _context_answer, sts = chat("", _context, None, params, None, _app_cfg['session_id'])

    images_cnt += files_cnts[0]
    videos_cnt += files_cnts[1]
    
    if code == 0:
        context_content = _context_answer if _context_answer else _answer
        _context.append({"role": "assistant", "contents": [
                        {"type": "text", "pairs": context_content}]})
        
        thinking_content_raw, formal_answer_raw = parse_thinking_response(_answer)
        thinking_content_fmt = normalize_text_for_html(thinking_content_raw)
        formal_answer_fmt = normalize_text_for_html(formal_answer_raw)
        formatted_result = format_response_with_thinking(thinking_content_fmt, formal_answer_fmt)
        
        print(f"[respond] thinking formatting: thinking_content_raw len={len(thinking_content_raw) if thinking_content_raw else 0}")
        print(f"[respond] thinking formatting: formal_answer_raw len={len(formal_answer_raw) if formal_answer_raw else 0}")
        print(f"[respond] thinking formatting: formatted_result len={len(formatted_result) if formatted_result else 0}")
        print(f"[respond] formatted_result content: {formatted_result[:200]}...")
        
        _chat_bot.append((_question, formatted_result))
        print(f"[respond] Updated _chat_bot, current length: {len(_chat_bot)}")
        print(f"[respond] _chat_bot[-1] content: {_chat_bot[-1][1][:200]}...")
        
        _app_cfg['ctx'] = _context
        _app_cfg['sts'] = sts
    else:
        _context.append({"role": "assistant", "contents": [
                        {"type": "text", "pairs": "Error occurred during processing"}]})
        _chat_bot.append((_question, "Error occurred during processing"))
    
    _app_cfg['images_cnt'] = images_cnt
    _app_cfg['videos_cnt'] = videos_cnt
    
    _app_cfg['is_streaming'] = False

    upload_image_disabled = videos_cnt > 0
    upload_video_disabled = videos_cnt > 0 or images_cnt > 0
    
    # Since function has yield from at top, must use yield instead of return
    print(f"[respond] Non-streaming mode complete, using yield to return result")
    yield create_multimodal_input(upload_image_disabled, upload_video_disabled), _chat_bot, _app_cfg, gr.update(visible=False)


def chat_stream_character_generator(img_b64, msgs, ctx, params=None, vision_hidden_states=None, stop_control=None, session_id=None):
    """
    Character-level streaming generator
    """
    print(f"[chat_stream_character_generator] Starting character-level streaming")
    print(f"[chat_stream_character_generator] stop_control: {stop_control}")
    
    try:
        stream_url = server_url.replace('/api', '/api/stream')
        print(f"[chat_stream_character_generator] Stream URL: {stream_url}")
        

        request_data = {
            "image": img_b64,
            "question": json.dumps(msgs, ensure_ascii=True),
            "params": json.dumps(params, ensure_ascii=True),
        }

        if session_id:
            request_data["session_id"] = session_id
        

        response = requests.post(
            stream_url,
            headers={
                "X-Model-Best-Model": "luca-v-online",
                "X-Model-Best-Trace-ID": "web_demo",
                "Accept": "text/event-stream",
                "Cache-Control": "no-cache",
            },
            json=request_data,
            stream=True
        )
        
        if response.status_code != 200:
            for char in f"Stream request failed: {response.status_code}":
                yield char
            return
        
        last_length = 0
        char_count = 0
        
        for line in response.iter_lines(decode_unicode=True):
            if stop_control and stop_control.get('stop_streaming', False):
                print(f"[chat_stream_character_generator] *** Stop signal received at char {char_count}, interrupting streaming ***")
                break
                
            if line and line.startswith('data: '):
                try:
                    data_str = line[6:]
                    data = json.loads(data_str)
                    
                    if 'error' in data:
                        for char in f"Error: {data['error']}":
                            yield char
                        return
                    
                    current_response = data.get('full_response', '')
                    
                    if data.get('finished', False):
                        if len(current_response) > last_length:
                            remaining = current_response[last_length:]
                            clean_remaining = re.sub(r'(<box>.*</box>)', '', remaining)
                            clean_remaining = clean_remaining.replace('<ref>', '')
                            clean_remaining = clean_remaining.replace('</ref>', '')
                            clean_remaining = clean_remaining.replace('<box>', '')
                            clean_remaining = clean_remaining.replace('</box>', '')
                            
                            for char in clean_remaining:
                                if stop_control and stop_control.get('stop_streaming', False):
                                    print(f"[chat_stream_character_generator] *** Stop signal received during final output ***")
                                    break
                                char_count += 1
                                yield char
                        break
                    else:
                        if len(current_response) > last_length:
                            new_chars = current_response[last_length:]
                            last_length = len(current_response)
                            
                            clean_chars = re.sub(r'(<box>.*</box>)', '', new_chars)
                            clean_chars = clean_chars.replace('<ref>', '')
                            clean_chars = clean_chars.replace('</ref>', '')
                            clean_chars = clean_chars.replace('<box>', '')
                            clean_chars = clean_chars.replace('</box>', '')
                            
                            for char in clean_chars:
                                if stop_control and stop_control.get('stop_streaming', False):
                                    print(f"[chat_stream_character_generator] *** Stop signal received at char {char_count} ***")
                                    return
                                char_count += 1
                                if char_count % 10 == 0:
                                    print(f"[chat_stream_character_generator] Output {char_count} chars, stop_flag: {stop_control.get('stop_streaming', False) if stop_control else 'None'}")
                                yield char
                
                except json.JSONDecodeError:
                    continue
        
        print(f"[chat_stream_character_generator] Streaming complete, total {char_count} chars output")
        
    except Exception as e:
        print(f"[chat_stream_character_generator] Exception: {e}")
        for char in f"Stream error: {str(e)}":
            yield char


def fewshot_add_demonstration(_image, _user_message, _assistant_message, _chat_bot, _app_cfg):
    if 'session_id' not in _app_cfg:
        _app_cfg['session_id'] = uuid.uuid4().hex[:16]
        print(f"[Session] Generated session_id for FewShot: {_app_cfg['session_id']}")
    
    ctx = _app_cfg["ctx"]
    message_item = []
    if _image is not None:
        image = Image.open(_image).convert("RGB")
        ctx.append({"role": "user", "contents": [
            *encode_image(image),
            {"type": "text", "pairs": _user_message}
        ]})
        message_item.append(
            {"text": "[mm_media]1[/mm_media]" + _user_message, "files": [_image]})
    else:
        if _user_message:
            ctx.append({"role": "user", "contents": [
                {"type": "text", "pairs": _user_message}
            ]})
            message_item.append({"text": _user_message, "files": []})
        else:
            message_item.append(None)
    if _assistant_message:
        ctx.append({"role": "assistant", "contents": [
            {"type": "text", "pairs": _assistant_message}
        ]})
        message_item.append({"text": _assistant_message, "files": []})
    else:
        message_item.append(None)

    _chat_bot.append(message_item)
    return None, "", "", _chat_bot, _app_cfg


def fewshot_respond(_image, _user_message, _chat_bot, _app_cfg, params_form, thinking_mode, streaming_mode):
    """
    FewShot response function supporting streaming and non-streaming modes
    """
    print(f"[fewshot_respond] Called with streaming_mode: {streaming_mode}")
    
    if 'session_id' not in _app_cfg:
        _app_cfg['session_id'] = uuid.uuid4().hex[:16]
        print(f"[Session] Generated session_id for FewShot: {_app_cfg['session_id']}")
    
    if params_form == 'Beam Search':
        streaming_mode = False
        print(f"[fewshot_respond] Beam Search mode, forcing streaming disabled")
    
    user_message_contents = []
    _context = _app_cfg["ctx"].copy()
    images_cnt = _app_cfg["images_cnt"]
    
    if _image:
        image = Image.open(_image).convert("RGB")
        user_message_contents += encode_image(image)
        images_cnt += 1
    if _user_message:
        user_message_contents += [{"type": "text", "pairs": _user_message}]
    if user_message_contents:
        _context.append({"role": "user", "contents": user_message_contents})

    if params_form == 'Beam Search':
        params = {
            'sampling': False,
            'num_beams': 3,
            'repetition_penalty': 1.2,
            "max_new_tokens": 16284,
            "enable_thinking": thinking_mode,
            "stream": False
        }
    else:
        params = {
            'sampling': True,
            'top_p': 0.8,
            'top_k': 100,
            'temperature': 0.7,
            'repetition_penalty': 1.03,
            "max_new_tokens": 16284,
            "enable_thinking": thinking_mode,
            "stream": streaming_mode
        }

    if disable_text_only and images_cnt == 0:
        gr.Warning("Please chat with at least one image or video.")
        yield _image, _user_message, '', _chat_bot, _app_cfg
        return

    if streaming_mode:
        print(f"[fewshot_respond] Using streaming mode")
        _app_cfg['is_streaming'] = True
        _app_cfg['stop_streaming'] = False
        if _image:
            _chat_bot.append([
                {"text": "[mm_media]1[/mm_media]" + _user_message, "files": [_image]},
                {"text": "", "files": []}
            ])
        else:
            _chat_bot.append([
                {"text": _user_message, "files": [_image]},
                {"text": "", "files": []}
            ])
        
        _context.append({"role": "assistant", "contents": [{"type": "text", "pairs": ""}]})
        
        _app_cfg['stop_streaming'] = False
        
        gen = chat_stream_character_generator("", _context[:-1], None, params, None, _app_cfg, _app_cfg['session_id'])
        
        yield _image, _user_message, '', _chat_bot, _app_cfg
        
        for _char in gen:
            if _app_cfg.get('stop_streaming', False):
                print("[fewshot_respond] Stop signal received, interrupting streaming")
                break
                
            _chat_bot[-1][1]["text"] += _char
            _context[-1]["contents"][0]["pairs"] += _char
            
            yield _image, _user_message, '', _chat_bot, _app_cfg
        
        final_content = _context[-1]["contents"][0]["pairs"]
        
        _app_cfg['ctx'] = _context
        _app_cfg['images_cnt'] = images_cnt
        _app_cfg['is_streaming'] = False
        
        yield _image, '', '', _chat_bot, _app_cfg
        
    else:
        code, _answer, _context_answer, sts = chat("", _context, None, params, None, _app_cfg['session_id'])

        context_content = _context_answer if _context_answer else _answer
        _context.append({"role": "assistant", "contents": [
                        {"type": "text", "pairs": context_content}]})

        if _image:
            _chat_bot.append([
                {"text": "[mm_media]1[/mm_media]" +
                    _user_message, "files": [_image]},
                {"text": _answer, "files": []}
            ])
        else:
            _chat_bot.append([
                {"text": _user_message, "files": [_image]},
                {"text": _answer, "files": []}
            ])
        if code == 0:
            _app_cfg['ctx'] = _context
            _app_cfg['sts'] = sts
            _app_cfg['images_cnt'] = images_cnt
        
        _app_cfg['is_streaming'] = False
        yield None, '', '', _chat_bot, _app_cfg


def regenerate_button_clicked(_question, _image, _user_message, _assistant_message, _chat_bot, _app_cfg, params_form, thinking_mode, streaming_mode):
    print(f"[regenerate] streaming_mode: {streaming_mode}")
    print(f"[regenerate] thinking_mode: {thinking_mode}")

    print(f"[regenerate] chat_type: {_app_cfg.get('chat_type', 'unknown')}")
    
    if params_form == 'Beam Search':
        streaming_mode = False
        print(f"[regenerate] Beam Search mode, forcing streaming disabled")
    
    if len(_chat_bot) <= 1 or not _chat_bot[-1][1]:
        gr.Warning('No question for regeneration.')
        yield '', _image, _user_message, _assistant_message, _chat_bot, _app_cfg
        return
        
    if _app_cfg["chat_type"] == "Chat":
        images_cnt = _app_cfg['images_cnt']
        videos_cnt = _app_cfg['videos_cnt']
        _question = _chat_bot[-1][0]
        _chat_bot = _chat_bot[:-1]
        _app_cfg['ctx'] = _app_cfg['ctx'][:-2]
        files_cnts = check_has_videos(_question)
        images_cnt -= files_cnts[0]
        videos_cnt -= files_cnts[1]
        _app_cfg['images_cnt'] = images_cnt
        _app_cfg['videos_cnt'] = videos_cnt
        upload_image_disabled = videos_cnt > 0
        upload_video_disabled = videos_cnt > 0 or images_cnt > 0
        
        print(f"[regenerate] About to call respond with streaming_mode: {streaming_mode}")
        for result in respond(_question, _chat_bot, _app_cfg, params_form, thinking_mode, streaming_mode):
            new_input, _chat_bot, _app_cfg, _stop_button = result
            _question = new_input
            yield _question, _image, _user_message, _assistant_message, _chat_bot, _app_cfg
    else:
        last_message = _chat_bot[-1][0]
        last_image = None
        last_user_message = ''
        if last_message.text:
            last_user_message = last_message.text
        if last_message.files:
            file_obj = last_message.files[0]
            if hasattr(file_obj, 'path'):
                last_image = file_obj.path
            elif hasattr(file_obj, 'file') and hasattr(file_obj.file, 'path'):
                last_image = file_obj.file.path
            elif hasattr(file_obj, 'name'):
                last_image = file_obj.name
            else:
    
                last_image = getattr(file_obj, 'url', getattr(file_obj, 'orig_name', str(file_obj)))
        _chat_bot = _chat_bot[:-1]
        _app_cfg['ctx'] = _app_cfg['ctx'][:-2]
        print(f"[regenerate] About to call fewshot_respond with streaming_mode: {streaming_mode}")
        for result in fewshot_respond(last_image, last_user_message, _chat_bot, _app_cfg, params_form, thinking_mode, streaming_mode):
            _image, _user_message, _assistant_message, _chat_bot, _app_cfg = result
            yield _question, _image, _user_message, _assistant_message, _chat_bot, _app_cfg


def flushed():
    return gr.update(interactive=True)


def clear(txt_message, chat_bot, app_session):
    txt_message.files.clear()
    txt_message.text = ''
    chat_bot = copy.deepcopy(init_conversation)
    app_session['sts'] = None
    app_session['ctx'] = []
    app_session['images_cnt'] = 0
    app_session['videos_cnt'] = 0
    app_session['stop_streaming'] = False
    app_session['is_streaming'] = False
    app_session['session_id'] = uuid.uuid4().hex[:16]
    print(f"[Session] Generated new session_id: {app_session['session_id']}")
    return create_multimodal_input(), chat_bot, app_session, None, '', ''


def select_chat_type(_tab, _app_cfg):
    _app_cfg["chat_type"] = _tab
    return _app_cfg


init_conversation = [
    [
        None,
        {
            "text": format_response_with_thinking("", "You can talk to me now"),
            "flushing": False
        }
    ],
]


css = """
video { height: auto !important; }
.example label { font-size: 16px;}

/* Thinking process and formal answer styles */
.response-container {
    margin: 10px 0;
}

.thinking-section {
    background: linear-gradient(135deg, #f8f9ff 0%, #f0f4ff 100%);
    border: 1px solid #d1d9ff;
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 0px;
    box-shadow: 0 2px 8px rgba(67, 90, 235, 0.1);
}

.thinking-header {
    font-weight: 600;
    color: #4c5aa3;
    font-size: 14px;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.thinking-content {
    color: #5a6ba8;
    font-size: 13px;
    line-height: 1;
    font-style: italic;
    background: rgba(255, 255, 255, 0.6);
    padding: 12px;
    border-radius: 8px;
    border-left: 3px solid #4c5aa3;
    white-space: pre-wrap;
}

.formal-section {
    background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
    border: 1px solid #e9ecef;
    border-radius: 12px;
    padding: 16px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.formal-header {
    font-weight: 600;
    color: #28a745;
    font-size: 14px;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.formal-content {
    color: #333;
    font-size: 14px;
    line-height: 1;
    white-space: pre-wrap;
}

/* Chatbot container styles */
.thinking-chatbot .message {
    border-radius: 12px;
    overflow: visible;
    margin-top: 0 !important;
    margin-bottom: 0 !important;
}

.thinking-chatbot .message-wrap {
    margin-top: 0 !important;
    margin-bottom: 0 !important;
}

.thinking-chatbot .message-warp {
    margin-top: 0 !important;
    margin-bottom: 0 !important;
}

.thinking-chatbot .mseeage-warp {
    margin-top: 0 !important;
    margin-bottom: 0 !important;
}

.thinking-chatbot .message.bot {
    background: transparent !important;
    border: none !important;
    padding: 8px !important;
}

.thinking-chatbot .message.bot .content {
    background: transparent !important;
}

/* Markdown paragraph spacing fixes */
.thinking-chatbot .message .content p:first-child { margin-top: 0; }
.thinking-chatbot .message .content p:last-child { margin-bottom: 0; }
.thinking-chatbot .message .content { margin: 0; }
.thinking-chatbot .message .content p { margin: 0 !important; }
.thinking-chatbot .message .content p > br:only-child { display: none; }
.thinking-chatbot .message .content p:empty { display: none; }
.thinking-chatbot .message .content p > .response-container { display: block; margin: 0 !important; }
.thinking-chatbot .message .content p > br { display: none; }

/* Markdown list spacing fixes */
.thinking-chatbot .message .content .markdown-body ol {
    margin-top: 0 !important;
    margin-bottom: 0 !important;
}

.thinking-chatbot .message .content .markdown-body p,
.thinking-chatbot .message .content .markdown-body blockquote,
.thinking-chatbot .message .content .markdown-body ul,
.thinking-chatbot .message .content .markdown-body ol,
.thinking-chatbot .message .content .markdown-body dl,
.thinking-chatbot .message .content .markdown-body table,
.thinking-chatbot .message .content .markdown-body pre,
.thinking-chatbot .message .content .markdown-body details {
    margin-bottom: 0 !important;
}

.thinking-chatbot .message .content .markdown-body ul,
.thinking-chatbot .message .content .markdown-body ol {
    margin-top: 0 !important;
    margin-bottom: 0 !important;
    padding-left: 1.25em;
    padding-top: 0 !important;
    padding-bottom: 0 !important;
    min-height: 0 !important;
    height: auto !important;
}

.thinking-chatbot .message .content .markdown-body li {
    margin-top: 0 !important;
    margin-bottom: 0 !important;
}

.thinking-chatbot .message .content .markdown-body li + li {
    margin-top: 0 !important;
}

.thinking-chatbot .message .content .markdown-body ul ul,
.thinking-chatbot .message .content .markdown-body ol ul,
.thinking-chatbot .message .content .markdown-body ul ol,
.thinking-chatbot .message .content .markdown-body ol ol {
    margin-top: 0 !important;
    margin-bottom: 0 !important;
}

.thinking-chatbot .message .content .markdown-body li {
    padding-top: 0 !important;
    padding-bottom: 0 !important;
}

.thinking-chatbot .message .content .markdown-body li > *:first-child {
    margin-top: 0 !important;
}

.thinking-chatbot .message .content .markdown-body li > *:last-child {
    margin-bottom: 0 !important;
}

.thinking-chatbot .message .content .markdown-body ul,
.thinking-chatbot .message .content .markdown-body ol {
    margin-block-start: 0 !important;
    margin-block-end: 0 !important;
    padding-block-start: 0 !important;
    padding-block-end: 0 !important;
    gap: 0 !important;
    border: 0 !important;
    outline: 0 !important;
    vertical-align: top !important;
    box-sizing: border-box !important;
}

.thinking-chatbot .message .content .markdown-body,
.thinking-chatbot .message .content .markdown-body p,
.thinking-chatbot .message .content .markdown-body blockquote,
.thinking-chatbot .message .content .markdown-body ul,
.thinking-chatbot .message .content .markdown-body ol,
.thinking-chatbot .message .content .markdown-body li,
.thinking-chatbot .message .content .markdown-body dl,
.thinking-chatbot .message .content .markdown-body table,
.thinking-chatbot .message .content .markdown-body pre,
.thinking-chatbot .message .content .markdown-body details,
.thinking-chatbot .message .content .markdown-body h1,
.thinking-chatbot .message .content .markdown-body h2,
.thinking-chatbot .message .content .markdown-body h3,
.thinking-chatbot .message .content .markdown-body h4,
.thinking-chatbot .message .content .markdown-body h5,
.thinking-chatbot .message .content .markdown-body h6 {
    margin-block-start: 0 !important;
    margin-block-end: 0 !important;
    padding-top: 0 !important;
    padding-bottom: 0 !important;
}

/* Unified line-height */
.thinking-chatbot .message .content .markdown-body,
.thinking-chatbot .message .content .markdown-body p,
.thinking-chatbot .message .content .markdown-body li,
.thinking-chatbot .message .content .markdown-body ul,
.thinking-chatbot .message .content .markdown-body ol,
.thinking-chatbot .message .content .markdown-body blockquote,
.thinking-chatbot .message .content .markdown-body dl,
.thinking-chatbot .message .content .markdown-body table,
.thinking-chatbot .message .content .markdown-body td,
.thinking-chatbot .message .content .markdown-body th,
.thinking-chatbot .message .content .markdown-body pre,
.thinking-chatbot .message .content .markdown-body details,
.thinking-chatbot .message .content .markdown-body code,
.thinking-chatbot .message .content .markdown-body pre code {
    line-height: 1 !important;
}

/* Chat container spacing */
.thinking-chatbot .bubble-wrap,
.thinking-chatbot .message-wrap,
.thinking-chatbot .bubble-gap {
    padding-top: 0 !important;
    padding-bottom: 0 !important;
    gap: 0 !important;
    row-gap: 0 !important;
    column-gap: 0 !important;
}

.thinking-chatbot .message-row {
    margin-top: 0 !important;
    margin-bottom: 0 !important;
    padding-top: 0 !important;
    padding-bottom: 0 !important;
}

.thinking-chatbot .message-content-button {
    padding: 0 !important;
    line-height: 1 !important;
}

.thinking-chatbot .ms-markdown.markdown-body {
    margin: 0 !important;
    padding: 0 !important;
}

.thinking-chatbot .ms-markdown.markdown-body * {
    margin-block-start: 0 !important;
    margin-block-end: 0 !important;
}

.thinking-chatbot .response-container {
    margin: 0 !important;
}

.thinking-chatbot .message .content .markdown-body ul,
.thinking-chatbot .message .content .markdown-body ol {
    display: block !important;
    font-size: inherit !important;
    list-style-position: inside !important;
    overflow: visible !important;
    -webkit-margin-before: 0 !important;
    -webkit-margin-after: 0 !important;
    -webkit-padding-start: 1.25em !important;
}

.thinking-chatbot .message .content .markdown-body li {
    display: list-item !important;
    text-align: inherit !important;
    -webkit-margin-before: 0 !important;
    -webkit-margin-after: 0 !important;
    vertical-align: baseline !important;
}

/* Responsive design */
@media (max-width: 768px) {
    .thinking-section, .formal-section {
        padding: 12px;
        margin-bottom: 12px;
    }
    
    .thinking-content, .formal-content {
        padding: 8px;
        font-size: 13px;
    }
}
"""

introduction = """

## Features:
1. Chat with single image
2. Chat with multiple images  
3. Chat with video
4. In-context few-shot learning
5. Streaming Mode: Real-time response streaming
6. Thinking Mode: Show model reasoning process

Click `How to use` tab to see examples.
"""


with gr.Blocks(css=css) as demo:
    with gr.Tab(model_name):
        with gr.Row():
            with gr.Column(scale=1, min_width=300):
                gr.Markdown(value=introduction)
                params_form = create_component(form_radio, comp='Radio')
                thinking_mode = create_component(thinking_checkbox, comp='Checkbox')
                streaming_mode = create_component(streaming_checkbox, comp='Checkbox')

                regenerate = create_component(
                    {'value': 'Regenerate'}, comp='Button')
                clear_button = create_component(
                    {'value': 'Clear History'}, comp='Button')
                
                stop_button = gr.Button("Stop", visible=False)

            with gr.Column(scale=3, min_width=500):
                initial_session_id = uuid.uuid4().hex[:16]
                print(f"[Session] Initializing session, generated session_id: {initial_session_id}")
                app_session = gr.State(
                    {'sts': None, 'ctx': [], 'images_cnt': 0, 'videos_cnt': 0, 'chat_type': 'Chat', 'stop_streaming': False, 'is_streaming': False, 'session_id': initial_session_id})
                chat_bot = mgr.Chatbot(label=f"Chat with {model_name}", value=copy.deepcopy(
                    init_conversation), height=600, flushing=False, bubble_full_width=False, 
                    elem_classes="thinking-chatbot")

                with gr.Tab("Chat") as chat_tab:
                    txt_message = create_multimodal_input()
                    chat_tab_label = gr.Textbox(
                        value="Chat", interactive=False, visible=False)

                    txt_message.submit(
                        respond,
                        [txt_message, chat_bot, app_session, params_form, thinking_mode, streaming_mode],
                        [txt_message, chat_bot, app_session, stop_button]
                    )

                with gr.Tab("Few Shot") as fewshot_tab:
                    fewshot_tab_label = gr.Textbox(
                        value="Few Shot", interactive=False, visible=False)
                    with gr.Row():
                        with gr.Column(scale=1):
                            image_input = gr.Image(
                                type="filepath", sources=["upload"])
                        with gr.Column(scale=3):
                            user_message = gr.Textbox(label="User")
                            assistant_message = gr.Textbox(label="Assistant")
                            with gr.Row():
                                add_demonstration_button = gr.Button(
                                    "Add Example")
                                generate_button = gr.Button(
                                    value="Generate", variant="primary")
                    add_demonstration_button.click(
                        fewshot_add_demonstration,
                        [image_input, user_message,
                            assistant_message, chat_bot, app_session],
                        [image_input, user_message,
                            assistant_message, chat_bot, app_session]
                    )
                    generate_button.click(
                        fewshot_respond,
                        [image_input, user_message, chat_bot,
                            app_session, params_form, thinking_mode, streaming_mode],
                        [image_input, user_message,
                            assistant_message, chat_bot, app_session]
                    )

                chat_tab.select(
                    select_chat_type,
                    [chat_tab_label, app_session],
                    [app_session]
                )
                chat_tab.select(
                    clear,
                    [txt_message, chat_bot, app_session],
                    [txt_message, chat_bot, app_session,
                        image_input, user_message, assistant_message]
                )
                fewshot_tab.select(
                    select_chat_type,
                    [fewshot_tab_label, app_session],
                    [app_session]
                )
                fewshot_tab.select(
                    clear,
                    [txt_message, chat_bot, app_session],
                    [txt_message, chat_bot, app_session,
                        image_input, user_message, assistant_message]
                )
                chat_bot.flushed(
                    flushed,
                    outputs=[txt_message]
                )
                
                params_form.change(
                    update_streaming_mode_state,
                    inputs=[params_form],
                    outputs=[streaming_mode]
                )
                
                regenerate.click(
                    regenerate_button_clicked,
                    [txt_message, image_input, user_message,
                        assistant_message, chat_bot, app_session, params_form, thinking_mode, streaming_mode],
                    [txt_message, image_input, user_message,
                        assistant_message, chat_bot, app_session]
                )
                clear_button.click(
                    clear,
                    [txt_message, chat_bot, app_session],
                    [txt_message, chat_bot, app_session,
                        image_input, user_message, assistant_message]
                )
                
                stop_button.click(
                    stop_button_clicked,
                    [app_session],
                    [app_session, stop_button]
                )

    with gr.Tab("How to use"):
        with gr.Column():
            with gr.Row():
                image_example = gr.Image(value="http://thunlp.oss-cn-qingdao.aliyuncs.com/multi_modal/never_delete/m_bear2.gif",
                                         label='1. Chat with single or multiple images', interactive=False, width=400, elem_classes="example")
                example2 = gr.Image(value="http://thunlp.oss-cn-qingdao.aliyuncs.com/multi_modal/never_delete/video2.gif",
                                    label='2. Chat with video', interactive=False, width=400, elem_classes="example")
                example3 = gr.Image(value="http://thunlp.oss-cn-qingdao.aliyuncs.com/multi_modal/never_delete/fshot.gif",
                                    label='3. Few shot', interactive=False, width=400, elem_classes="example")


# launch
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Web Demo for MiniCPM-o 4.5')
    parser.add_argument('--port', type=int, default=8889,
                        help='Port to run the web demo on')
    parser.add_argument('--server', type=str, default=server_url,
                        help='Server URL to connect to')
    args = parser.parse_args()
    port = args.port
    server_url = args.server
    
    demo.launch(share=False, debug=True, show_api=False,
                server_port=port, server_name="0.0.0.0")
