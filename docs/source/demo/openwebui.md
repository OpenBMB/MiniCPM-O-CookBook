# OpenWebUI

## Overview

Open WebUI is an extensible web interface designed for Ollama with full OpenAI API compatibility. It provides seamless interaction with MiniCPM-V multimodal models through an intuitive chat interface.

MiniCPM-V is a series of efficient multimodal models with strong OCR capabilities, supporting high-resolution images, multi-image reasoning, and video understanding.

## Requirements
- Python 3.11+
- Docker (recommended) or local Python environment
- 18GB+ RAM (24GB+ recommended)
- CUDA-compatible GPU (for local inference)

## Quick Setup

### Option 1: Docker (Recommended)

```bash
# Basic installation
docker run -d -p 3000:8080 \
  -v open-webui:/app/backend/data \
  --name open-webui \
  --restart always \
  ghcr.io/open-webui/open-webui:main
```

### Option 2: pip Installation

```bash
pip install open-webui
open-webui serve
```

Access at: http://localhost:8080

## Model Deployment

### Using Ollama (Easiest)

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Run MiniCPM-V model
ollama run openbmb/minicpm-v4.5
```

Configure in Open WebUI: Settings → Connections → Ollama API → `http://localhost:11434`

### Using vLLM (High Performance)

```bash
# Install and start vLLM service
pip install vllm==0.10.1
vllm serve openbmb/MiniCPM-V-4_5 \
  --dtype auto \
  --api-key token-abc123 \
  --trust-remote-code
```

Configure in Open WebUI: Settings → Connections → OpenAI API
- API Base URL: `http://localhost:8000/v1`
- API Key: `token-abc123`

### Using SGLang (Structured Generation)

```bash
# Install SGLang
git clone https://github.com/sgl-project/sglang.git
cd sglang && pip install -e "python[all]"

# Start service
python -m sglang.launch_server \
  --model-path openbmb/MiniCPM-V-4_5 \
  --port 30000 \
  --trust-remote-code
```

Configure API Base URL: `http://localhost:30000/v1`

## Usage Examples

### Image Understanding
Upload an image and ask:
```
Describe this image in detail.
```

### OCR Text Extraction
```
Extract all text from this image while maintaining the original format.
```

### Multi-image Comparison
```
Compare these two images and analyze their similarities and differences.
```

### Document Analysis
```
What type of document is this? Summarize its main content.
```

## API Integration

### Python Example

```python
import requests
import base64

with open('image.jpg', 'rb') as f:
    image_data = base64.b64encode(f.read()).decode()

response = requests.post(
    'http://localhost:8000/v1/chat/completions',
    headers={'Authorization': 'Bearer token-abc123'},
    json={
        'model': 'MiniCPM-V-4_5',
        'messages': [{
            'role': 'user',
            'content': [
                {'type': 'text', 'text': 'Describe this image'},
                {'type': 'image_url', 'image_url': {'url': f'data:image/jpeg;base64,{image_data}'}}
            ]
        }]
    }
)
```

## Resources

- [Open WebUI Documentation](https://docs.openwebui.com/)
- [MiniCPM-V Models](https://huggingface.co/openbmb)
- [Ollama Official Site](https://ollama.ai/)
- [vLLM Documentation](https://docs.vllm.ai/)