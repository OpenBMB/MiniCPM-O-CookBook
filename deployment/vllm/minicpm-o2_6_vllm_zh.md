# MiniCPM-O2.6 vLLM 部署指南

## 1. 环境准备

>  [!NOTE]
> MiniCPM-O2.6在vllm上使用需要特定的transformers来进行运行
>
> 目前测试可行的方案：
> 
> 1、`0.9.2>vllm >= 0.7.1 + 4.52.3 >= transformers >= 4.48.2`
>
> 2、`vllm >= 0.10.0 + 4.53.3 >= transformers >= 4.53.0` 
>
> 3、**临时方案（马上会提交）**：一个新分支修复了不同transformers版本的问题，可以使用源码安装该分支 [Fix-minicpm-o-2_6](https://github.com/tc-mb/vllm/tree/Fix/Fix-minicpm-o-2_6-WhisperEncodingLayer)，安装方式详见[vLLM文档](https://docs.vllm.ai/en/v0.10.1.1/getting_started/installation/index.html)

### 1.1 安装 vLLM

```bash
pip install vllm == 0.7.1
pip install transformers == 4.48.2
```

进行视频推理时，需要安装相应的视频模块：
```bash
pip install vllm[video]
```

进行音频推理时，需要安装相应的音频模块：
```bash
pip install vllm[audio]
```

## 2. API 服务部署

### 2.1 启动 API 服务

```bash
vllm serve <模型路径>  --dtype auto --max-model-len 2048 --api-key token-abc123 --gpu_memory_utilization 0.9 --trust-remote-code
```

**参数说明：**
- `<模型路径>`：指定 MiniCPM-O2.6 模型的本地路径
- `--api-key`：设置 API 访问密钥
- `--max-model-len`：设置最大模型长度
- `--gpu_memory_utilization`：GPU 内存使用率

### 2.2 图片推理

```python
from openai import OpenAI
import base64

# API 配置
openai_api_key = "token-abc123"  # API 密钥需与启动服务时设置的密钥保持一致
openai_api_base = "http://localhost:8000/v1"

client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)

# 读取本地图片并编码
with open('./assets/airplane.jpeg', 'rb') as file:
    image = "data:image/jpeg;base64," + base64.b64encode(file.read()).decode('utf-8')

chat_response = client.chat.completions.create(
    model="<模型路径>",  # 指定模型路径或 HuggingFace ID
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "请描述这张图片"},
            {
                "type": "image_url",
                "image_url": {
                    "url": image,  # 支持网络图片 URL
                },
            },
        ],
    }],
    extra_body={
        "stop_token_ids": [1, 151645]
    }
)

print("Chat response:", chat_response)
print("Chat response content:", chat_response.choices[0].message.content)
```

### 2.3 视频推理

```python
from openai import OpenAI
import base64

# API 配置
openai_api_key = "token-abc123"
openai_api_base = "http://localhost:8000/v1"

client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)

# 读取视频文件并编码为 base64
with open('./videos/video.mp4', 'rb') as video_file:
    video_base64 = base64.b64encode(video_file.read()).decode('utf-8')

chat_response = client.chat.completions.create(
    model="<模型路径>",
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant.",
        },
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "请描述这个视频"},
                {
                    "type": "video_url",
                    "video_url": {
                        "url": f"data:video/mp4;base64,{video_base64}",
                    },
                },
            ],
        },
    ],
    extra_body={
        "stop_token_ids": [1, 151645]
    }
)

print("Chat response:", chat_response)
print("Chat response content:", chat_response.choices[0].message.content)
```

### 2.4 音频推理

```python
from openai import OpenAI
import base64

# API 配置
openai_api_key = "token-abc123"
openai_api_base = "http://localhost:8000/v1"

client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)

# 读取音频文件并编码为 base64
with open('./audio/audio.wav', 'rb') as audio_file:
    video_base64 = base64.b64encode(audio_file.read()).decode('utf-8')

chat_response = client.chat.completions.create(
    model="<模型路径>",
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant.",
        },
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "请描述这个音频"},
                {
                    "type": "video_url",
                    "video_url": {
                        "url": f"data:audio/wav;base64,{video_base64}",
                    },
                },
            ],
        },
    ],
    extra_body={
        "stop_token_ids": [1, 151645]
    }
)

print("Chat response:", chat_response)
print("Chat response content:", chat_response.choices[0].message.content)
```

### 2.5 多轮对话

#### 启动参数配置

进行视频多轮对话时，需要在 vLLM 启动时添加 `--limit-mm-per-prompt` 参数：

**视频多轮对话配置（支持最多3个视频）：**
```bash
vllm serve <模型路径> --dtype auto --max-model-len 4096 --api-key token-abc123 --gpu_memory_utilization 0.9 --trust-remote-code --limit-mm-per-prompt '{"video": 3}'
```

**图片和视频混合输入配置：**
```bash
vllm serve <模型路径> --dtype auto --max-model-len 4096 --api-key token-abc123 --gpu_memory_utilization 0.9 --trust-remote-code --limit-mm-per-prompt '{"image":5, "video": 2}'
```

#### 多轮对话示例代码

```python
from openai import OpenAI
import base64
import mimetypes
import os

# API 配置
openai_api_key = "token-abc123"
openai_api_base = "http://localhost:8000/v1"

client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)

messages = [
    {
        "role": "system",
        "content": "You are a helpful assistant.",
    }
]

def file_to_base64(file_path):
    """将文件转换为 base64 编码"""
    with open(file_path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')

def get_mime_type(file_path):
    """获取文件 MIME 类型"""
    mime, _ = mimetypes.guess_type(file_path)
    return mime or 'application/octet-stream'

def build_file_content(file_path):
    """构建多媒体文件内容"""
    mime_type = get_mime_type(file_path)
    base64_data = file_to_base64(file_path)
    url = f"data:{mime_type};base64,{base64_data}"

    if mime_type.startswith("image/"):
        return {"type": "image_url", "image_url": {"url": url}}
    elif mime_type.startswith("video/"):
        return {"type": "video_url", "video_url": {"url": url}}
    else:
        print(f"不支持的文件类型: {mime_type}")
        return None

# 交互式对话循环
while True:
    user_text = input("请输入问题（输入 'exit' 退出）：")
    if user_text.strip().lower() == "exit":
        break

    content = [{"type": "text", "text": user_text}]

    # 文件上传确认
    upload_file = input("是否上传文件？(y/n): ").strip().lower() == 'y'
    if upload_file:
        file_path = input("请输入文件路径: ").strip()
        if os.path.exists(file_path):
            file_content = build_file_content(file_path)
            if file_content:
                content.append(file_content)
        else:
            print("文件路径不存在，跳过文件上传。")

    messages.append({
        "role": "user",
        "content": content,
    })

    chat_response = client.chat.completions.create(
        model="<模型路径>",
        messages=messages,
        extra_body={
            "stop_token_ids": [1, 151645]
        }
    )

    ai_message = chat_response.choices[0].message
    print("MiniCPM-O2.6:", ai_message.content)
    
    messages.append({
        "role": "assistant",
        "content": ai_message.content,
    })
```

## 3. 离线推理

```python
from transformers import AutoTokenizer
from PIL import Image
from vllm import LLM, SamplingParams

# 模型配置
MODEL_NAME = "<模型路径>"
# 可选择使用 HuggingFace 模型 ID
# MODEL_NAME = "openbmb/MiniCPM-V-4"

# 加载图片
image = Image.open("./assets/airplane.jpeg").convert("RGB")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)

# 初始化 LLM
llm = LLM(
    model=MODEL_NAME, 
    max_model_len=2048,
    trust_remote_code=True,
    disable_mm_preprocessor_cache=True,
    limit_mm_per_prompt={"image": 5}
)

# 构建消息
messages = [{
    "role": "user",
    "content": "(<image>./</image>)\n请描述这张图片的内容"
}]

prompt = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True
)

# 单次推理
inputs = {
    "prompt": prompt,
    "multi_modal_data": {
        "image": image
        # 多图片推理需使用列表格式：
        # "image": [image1, image2] 
    },
}

# 批量推理示例
# inputs = [{
#     "prompt": prompt,
#     "multi_modal_data": {
#         "image": image
#     },
# } for _ in range(2)]

# 设置停止标记
stop_tokens = ['<|im_end|>', '<|endoftext|>']
stop_token_ids = [tokenizer.convert_tokens_to_ids(i) for i in stop_tokens]

# 采样参数
sampling_params = SamplingParams(
    stop_token_ids=stop_token_ids, 
    temperature=0.7,
    top_p=0.7,
    max_tokens=1024
)

# 生成结果
outputs = llm.generate(inputs, sampling_params=sampling_params)
print(outputs[0].outputs[0].text)
```

## 注意事项

1. **模型路径**：需将所有示例中的 `<模型路径>` 替换为实际的 MiniCPM-O2.6 模型路径
2. **API 密钥**：确保启动服务时的 API 密钥与客户端代码中的密钥保持一致
3. **文件路径**：需根据实际情况调整图片、视频文件的路径
4. **内存配置**：应根据 GPU 内存情况合理调整 `--gpu_memory_utilization` 参数
5. **多模态限制**：使用多轮对话时需设置合适的 `--limit-mm-per-prompt` 参数