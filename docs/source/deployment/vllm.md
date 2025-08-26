# vLLM

:::{Note}
We've submitted a PR for MiniCPM-V 4.5 to the vLLM repo, and it's currently under review for merging. In the meantime, you can use our code via [this link](https://github.com/tc-mb/vllm/tree/Support-MiniCPM-V-4.5)..
:::

[vLLM](https://github.com/vllm-project/vllm) is a fast and easy-to-use library for LLM inference and serving.
To learn more about vLLM, please refer to the [documentation](https://docs.vllm.ai/en/latest/).

## 1. Environment Setup

### 1.1 Install vLLM

```bash
pip install vllm==0.10.1
```

For video inference, install the video module:
```bash
pip install vllm[video]
```

:::{note}
Please note that the prebuilt `vllm` has strict dependencies on `torch` and its CUDA versions.
Check the note in the official document for installation ([link](https://docs.vllm.ai/en/latest/getting_started/installation.html)) for more help.
:::

## 2. API Service Deployment

### 2.1 Launch API Service

It is easy to build an OpenAI-compatible API service with vLLM, which can be deployed as a server that implements OpenAI API protocol. By default, it starts the server at http://localhost:8000. You can specify the address with --host and --port arguments. Run the command as shown below:

```bash
vllm serve <model_path>  --dtype auto --max-model-len 2048 --api-key token-abc123 --gpu_memory_utilization 0.9 --trust-remote-code
```

**Parameter Description:**
- `<model_path>`: Specify the local path to your MiniCPM-V 4.5 model
- `--api-key`: Set the API access key
- `--max-model-len`: Set the maximum model length
- `--gpu_memory_utilization`: GPU memory utilization rate

### 2.2 Image Inference

```python
from openai import OpenAI
import base64

# API configuration
openai_api_key = "token-abc123"  # API key must match the one set when launching the service
openai_api_base = "http://localhost:8000/v1"

client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)

# Read and encode local image
with open('./assets/airplane.jpeg', 'rb') as file:
    image = "data:image/jpeg;base64," + base64.b64encode(file.read()).decode('utf-8')

chat_response = client.chat.completions.create(
    model="<model_path>",  # Specify model path or HuggingFace ID
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "Please describe this image"},
            {
                "type": "image_url",
                "image_url": {
                    "url": image,  # Supports network image URLs
                },
            },
        ],
    }],
    extra_body={
        "stop_token_ids": [1, 73440]
    }
)

print("Chat response:", chat_response)
print("Chat response content:", chat_response.choices[0].message.content)
```

### 2.3 Video Inference

```python
from openai import OpenAI
import base64

# API configuration
openai_api_key = "token-abc123"
openai_api_base = "http://localhost:8000/v1"

client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)

# Read video file and encode to base64
with open('./videos/video.mp4', 'rb') as video_file:
    video_base64 = base64.b64encode(video_file.read()).decode('utf-8')

chat_response = client.chat.completions.create(
    model="<model_path>",
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant.",
        },
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Please describe this video"},
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
        "stop_token_ids": [1, 73440]
    }
)

print("Chat response:", chat_response)
print("Chat response content:", chat_response.choices[0].message.content)
```

### 2.4 Multi-turn Conversation

#### Launch Parameter Configuration

For video multi-turn conversations, you need to add the `--limit-mm-per-prompt` parameter when launching vLLM:

**Video multi-turn conversation configuration (supports up to 3 videos):**
```bash
vllm serve <model_path> --dtype auto --max-model-len 4096 --api-key token-abc123 --gpu_memory_utilization 0.9 --trust-remote-code --limit-mm-per-prompt video=3
```

**Image and video mixed input configuration:**
```bash
vllm serve <model_path> --dtype auto --max-model-len 4096 --api-key token-abc123 --gpu_memory_utilization 0.9 --trust-remote-code --limit-mm-per-prompt image=5,video=2
```

#### Multi-turn Conversation Example Code

```python
from openai import OpenAI
import base64
import mimetypes
import os

# API configuration
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
    """Convert file to base64 encoding"""
    with open(file_path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')

def get_mime_type(file_path):
    """Get file MIME type"""
    mime, _ = mimetypes.guess_type(file_path)
    return mime or 'application/octet-stream'

def build_file_content(file_path):
    """Build multimedia file content"""
    mime_type = get_mime_type(file_path)
    base64_data = file_to_base64(file_path)
    url = f"data:{mime_type};base64,{base64_data}"

    if mime_type.startswith("image/"):
        return {"type": "image_url", "image_url": {"url": url}}
    elif mime_type.startswith("video/"):
        return {"type": "video_url", "video_url": {"url": url}}
    else:
        print(f"Unsupported file type: {mime_type}")
        return None

# Interactive conversation loop
while True:
    user_text = input("Please enter your question (type 'exit' to quit): ")
    if user_text.strip().lower() == "exit":
        break

    content = [{"type": "text", "text": user_text}]

    # File upload confirmation
    upload_file = input("Upload a file? (y/n): ").strip().lower() == 'y'
    if upload_file:
        file_path = input("Please enter file path: ").strip()
        if os.path.exists(file_path):
            file_content = build_file_content(file_path)
            if file_content:
                content.append(file_content)
        else:
            print("File path does not exist, skipping file upload.")

    messages.append({
        "role": "user",
        "content": content,
    })

    chat_response = client.chat.completions.create(
        model="<model_path>",
        messages=messages,
        extra_body={
            "stop_token_ids": [1, 73440]
        }
    )

    ai_message = chat_response.choices[0].message
    print("MiniCPM-V-4:", ai_message.content)
    
    messages.append({
        "role": "assistant",
        "content": ai_message.content,
    })
```

## 3. Offline Inference

```python
from transformers import AutoTokenizer
from PIL import Image
from vllm import LLM, SamplingParams

# Model configuration
MODEL_NAME = "<model_path>"
# Option to use HuggingFace model ID
# MODEL_NAME = "openbmb/MiniCPM-V-4"

# Load image
image = Image.open("./assets/airplane.jpeg").convert("RGB")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)

# Initialize LLM
llm = LLM(
    model=MODEL_NAME, 
    max_model_len=4096,
    trust_remote_code=True,
    disable_mm_preprocessor_cache=True,
    limit_mm_per_prompt={"image": 5}
)

# Build messages
messages = [{
    "role": "user",
    "content": "(<image>./</image>)\nPlease describe the content of this image"
}]

prompt = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True
)

# Single inference
inputs = {
    "prompt": prompt,
    "multi_modal_data": {
        "image": image
        # For multi-image inference, use list format:
        # "image": [image1, image2] 
    },
}

# Batch inference example
# inputs = [{
#     "prompt": prompt,
#     "multi_modal_data": {
#         "image": image
#     },
# } for _ in range(2)]

# Set stop tokens
stop_tokens = ['<|im_end|>', '<|endoftext|>']
stop_token_ids = [tokenizer.convert_tokens_to_ids(i) for i in stop_tokens]

# Sampling parameters
sampling_params = SamplingParams(
    stop_token_ids=stop_token_ids, 
    temperature=0.7,
    top_p=0.8,
    max_tokens=4096
)

# Generate results
outputs = llm.generate(inputs, sampling_params=sampling_params)
print(outputs[0].outputs[0].text)
```

## Notes

1. **Model Path**: Replace all `<model_path>` in the examples with the actual MiniCPM-V 4.5 model path
2. **API Key**: Ensure the API key when launching the service matches the key in the client code
3. **File Paths**: Adjust image and video file paths according to your actual situation
4. **Memory Configuration**: Adjust the `--gpu_memory_utilization` parameter appropriately based on GPU memory
5. **Multimodal Limits**: Set appropriate `--limit-mm-per-prompt` parameters when using multi-turn conversations 