# Quickstart

## 1. Installation
```bash
pip install -r inference/requirements.txt
```

## 2. Basic Usage
```python
import torch
from transformers import AutoModel, AutoTokenizer

# Load the model
model = AutoModel.from_pretrained('openbmb/MiniCPM-V-4', trust_remote_code=True)
tokenizer = AutoTokenizer.from_pretrained('openbmb/MiniCPM-V-4', trust_remote_code=True)

# Start inference!
# See our recipe notebooks for detailed instructions
```

## 🍽️ Menu

### 🔥 Hot Dishes (Inference)
> *Ready-to-serve examples for immediate satisfaction*

| Recipe | Description | 
|---------|-------------|
| **Vision Capabilities** | |
| 🖼️ [Single Image](./inference/single_image.md) | Image understanding with high-resolution support |
| 🧩 [Multi Images](./inference/multi_images.md) | Multi-image reasoning and comparison |
| 🎬 [Video Understanding](./inference/video_understanding.md) | Real-time video analysis and dense captions |
| 📝 [OCR](./inference/ocr.md) | Robust text extraction and recognition |
| 🔍 [Scene Text Recognition](./inference/scene_text_recognize.md) | Scene text detection and license plate recognition |
| 📄 [PDF Parse](./inference/pdf_parse.md) | PDF document parsing and text extraction |
| **Omni Capabilities** | |
| 🎤 [Speech-to-Text](./inference/speech2text.md) | Multilingual speech recognition |
| 🗣️ [Text-to-Speech](./inference/text2speech.md) | Natural speech synthesis with emotion control |
| 🎭 [Voice Clone](./inference/voice_clone.md) | End-to-end voice cloning and role-playing |

### 🏋️ Training Camp (Fine-tuning)
> *Customize your model with your own ingredients*

- **[Fine-tuning Guide](./finetune/readme.md)** - Complete training recipes
- **[LoRA Training](./finetune/finetune_lora.sh)** - Efficient parameter tuning
- **[Full Training](./finetune/finetune_ds.sh)** - Deep customization
- **[Custom Datasets](./finetune/dataset.py)** - Prepare your own data

### 🥡 Takeaway (Deployment)
> *Package your model for production*

| Platform | Recipe | Best For |
|----------|--------|----------|
| [Llama.cpp](./run_locally/llamacpp) | CPU inference | Local deployment |
| [Ollama](./run_locally/ollama) | Easy management | Quick setup |
| [vLLM](./deployment/vllm) | High throughput | Production servers |
| [SGLang](./deployment/sglang) | Structured generation | Complex workflows |
| [Web Demo](./demo/webdemo) | FastAPI interactive interface | User-friendly apps |

### 🥄 Light Bites (Quantization)
> *Compress your model without losing flavor*

- **[GGUF](./quantization/gguf/)** - Ultra-lightweight format
- **[BNB](./quantization/bnb/)** - Bits and bytes optimization
- **[AWQ](./quantization/awq)** - Activation-aware quantization  

### 📱 Special Menu (Demos)
> *Showcase dishes to impress your guests*

- **[Web Demo](./demo/web_demo/)** - Interactive web interface and production API
