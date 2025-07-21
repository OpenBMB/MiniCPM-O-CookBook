# SGLang 

## 1.Installing SGLang
### Install SGLang from Source Code
```bash
git clone https://github.com/sgl-project/sglang.git
cd sglang

pip install --upgrade pip
pip install -e "python[all]"
```

### Installing flashinfer Dependencies

Method 1: pip installation (network speed may be insufficient)
```bash
pip install flashinfer -i https://flashinfer.ai/whl/cu121/torch2.4/
```

Method 2: whl file installation
- Visit: [https://flashinfer.ai/whl/cu121/torch2.4/flashinfer/](https://flashinfer.ai/whl/cu121/torch2.4/flashinfer/)
- Locate and download the whl file compatible with your server, e.g. `flashinfer-0.1.6+cu121torch2.4-cp310-cp310-linux_x86_64.whl`
- Install using pip:
    ```bash
    pip install flashinfer-0.1.6+cu121torch2.4-cp310-cp310-linux_x86_64.whl
    ```
For any installation issues, please consult the [official installation documentation](https://docs.sglang.ai/start/install.html)

## 2.Launching Inference Service with SGLang

By default, it downloads model files from Hugging Face Hub
```bash
python -m sglang.launch_server --model-path openbmb/MiniCPM-V-4 --port 30000
```
Alternatively, you can specify a local path after the `--model-path` parameter
```bash
python -m sglang.launch_server --model-path your_model_path --port 30000 --trust-remote-code
```

## 3.Service API Calls
- Bash call
    ```python
    curl -s http://localhost:30000/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d '{
        "model": "MiniCPM-V-4",
        "messages": [
        {
            "role": "user",
            "content": [
            {
                "type": "text",
                "text": "What's in this image?"
            },
            {
                "type": "image_url",
                "image_url": {
                "url": "https://github.com/OpenSQZ/MiniCPM-o-cookbook/blob/main/inference/assets/airplane.jpeg?raw=true"
                }
            }
            ]
        }
        ],
        "max_tokens": 300
    }'
    ```

- Python call
    ```python
    from openai import OpenAI

    client = OpenAI(base_url=f"http://localhost:30000/v1", api_key="None")

    response = client.chat.completions.create(
        model="MiniCPM-V-4",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "What is in this image?",
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": "https://github.com/OpenSQZ/MiniCPM-o-cookbook/blob/main/inference/assets/airplane.jpeg?raw=true",
                        },
                    },
                ],
            }
        ],
        max_tokens=300,
    )

    print(response.choices[0].message.content)
    ```
> **If the image_url is inaccessible, it can be replaced with a local image path**
> 
> For more calling methods, please refer to the [SGLang documentation](https://docs.sglang.ai/backend/openai_api_vision.html)