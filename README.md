<div align="center">

# 🍳 MiniCPM-o Cookbook


[🏠 Main Repository](https://github.com/OpenBMB/MiniCPM-o) | [📚 Full Documentation](https://minicpm-o.readthedocs.io/en/latest/index.html)

Cook up amazing multimodal AI applications effortlessly with MiniCPM-o, bringing vision, speech, and live-streaming capabilities right to your fingertips!

</div>


## ✨ What Makes Our Recipes Special?

### Broad User Spectrum

We support a wide range of users, from individuals to enterprises and researchers.

* **Individuals**: Enjoy effortless inference using [Ollama](./deployment/ollama/minicpm-v4_ollama.md) and [Llama.cpp](./deployment/llama.cpp/minicpm-v4_llamacpp.md) with minimal setup.
* **Enterprises**: Achieve high-throughput, scalable performance with [vLLM](./deployment/vllm/minicpm-v4_vllm.md) and [SGLang](./deployment/sglang/MiniCPM-v4_sglang.md).
* **Researchers**: Leverage advanced frameworks including [Transformers](./finetune/finetune_full.md) , [LLaMA-Factory](./finetune/finetune_llamafactory.md), [SWIFT](./finetune/swift.md), and [Align-anything](./finetune/align_anything.md) to enable flexible model development and cutting-edge experimentation.


### Versatile Deployment Scenarios

Our ecosystem delivers optimal solution for a variety of hardware environments and deployment demands.

* **Web demo**: Launch interactive multimodal AI web demo with [FastAPI](./demo/README.md).
* **Quantized deployment**: Maximize efficiency and minimize resource consumption using [GGUF](./quantization/gguf/minicpm-v4_gguf_quantize.md) and [BNB](./quantization/bnb/minicpm-v4_bnb_quantize.md).
* **Edge devices**: Bring powerful AI experiences to [iPhone and iPad](./demo/ios_demo/ios.md), supporting offline and privacy-sensitive applications.

## ⭐️ Live Demonstrations

Explore real-world examples of MiniCPM-o deployed on edge devices using our curated recipes. These demos highlight the model’s high efficiency and robust performance in practical scenarios.

- Run locally on iPhone with [iOS demo](./demo/ios_demo/ios.md).
<table align="center"> 
    <p align="center">
      <img src="inference/assets/gif_cases/iphone_cn.gif" width=32%/>
      &nbsp;&nbsp;&nbsp;&nbsp;
      <img src="inference/assets/gif_cases/iphone_en.gif" width=32%/>
    </p>
</table> 

- Run locally on iPad with [iOS demo](./demo/ios_demo/ios.md), observing the process of drawing a rabbit.
<table align="center">
    <p align="center">
      <video src="https://github.com/user-attachments/assets/43659803-8fa4-463a-a22c-46ad108019a7" width="360" /> </video>
    </p>
</table>

## 🔥 Inference Recipes
> *Ready-to-run examples*

| Recipe | Description | 
|---------|:-------------|
| **Vision Capabilities** | |
| 🖼️ [Single-image QA](./inference/single_image.md) | Question answering on a single image |
| 🧩 [Multi-image QA](./inference/multi_images.md) | Question answering with multiple images |
| 🎬 [Video QA](./inference/video_understanding.md) | Video-based question answering |
| 📄 [Document Parser](./inference/pdf_parse.md) | Parse and extract content from PDFs and webpages |
| 📝 [Text Recognition](./inference/ocr.md) | Reliable OCR for photos and screenshots |
| **Audio Capabilities** | |
| 🎤 [Speech-to-Text](./inference/speech2text.md) | Multilingual speech recognition |
| 🗣️ [Text-to-Speech](./inference/text2speech.md) | Instruction-following speech synthesis |
| 🎭 [Voice Cloning](./inference/voice_clone.md) | Realistic voice cloning and role-play |

## 🏋️ Fine-tuning Recipes
> *Customize your model with your own ingredients*

**Data preparation**

Follow the [guidance](./finetune/dataset_guidance.md) to set up your training datasets.


**Training**

We provide training methods serving different needs as following:


| Framework | Description|
|----------|--------|
| [Transformers](./finetune/finetune_full.md) | Most flexible for customization | 
| [LLaMA-Factory](./finetune/finetune_llamafactory.md) | Modular fine-tuning toolkit  |
| [SWIFT](./finetune/swift.md) | Lightweight and fast parameter-efficient tuning |
| [Align-anything](./finetune/align_anything.md) | Visual instruction alignment for multimodal models |



## 📦 Serving Recipes
> *Deploy your model efficiently*

| Method                                | Description                                  |
|-------------------------------------------|----------------------------------------------|
| [vLLM](./deployment/vllm/minicpm-v4_vllm.md)| High-throughput GPU inference                |
| [SGLang](./deployment/sglang/MiniCPM-v4_sglang.md)| High-throughput GPU inference                |
| [Llama.cpp](./deployment/llama.cpp/minicpm-v4_llamacpp.md)| Fast CPU inference on PC, iPhone and iPad                        |
| [Ollama](./deployment/ollama/minicpm-v4_ollama.md)| User-friendly setup  |
| [OpenWebUI](./demo/web_demo/openwebui) | Interactive Web demo with Open WebUI |
| [FastAPI](./demo/README.md) | Interactive Omni Streaming demo with FastAPI |
| [iOS](./demo/ios_demo/ios.md) | Interactive iOS demo with llama.cpp |

## 🥄 Quantization Recipes
> *Compress your model to improve efficiency*

| Format                                 | Key Feature                        |
|-----------------------------------------|------------------------------------|
| [GGUF](./quantization/gguf/minicpm-v4_gguf_quantize.md)| Simplest and most portable format  |
| [BNB](./quantization/bnb/minicpm-v4_bnb_quantize.md)   | Efficient 4/8-bit weight quantization |

## Awesome Works using MiniCPM-o
- [text-extract-api](https://github.com/CatchTheTornado/text-extract-api): Document extraction API using OCRs and Ollama supported models ![GitHub Repo stars](https://img.shields.io/github/stars/CatchTheTornado/text-extract-api)
- [comfyui_LLM_party](https://github.com/heshengtao/comfyui_LLM_party): Build LLM workflows and integrate into existing image workflows ![GitHub Repo stars](https://img.shields.io/github/stars/heshengtao/comfyui_LLM_party)
- [Ollama-OCR](https://github.com/imanoop7/Ollama-OCR): OCR package uses vlms through Ollama to extract text from images and PDF ![GitHub Repo stars](https://img.shields.io/github/stars/imanoop7/Ollama-OCR)
- [comfyui-mixlab-nodes](https://github.com/MixLabPro/comfyui-mixlab-nodes): ComfyUI node suite supports Workflow-to-APP、GPT&3D and more ![GitHub Repo stars](https://img.shields.io/github/stars/MixLabPro/comfyui-mixlab-nodes)
- [OpenAvatarChat](https://github.com/HumanAIGC-Engineering/OpenAvatarChat): Interactive digital human conversation implementation on single PC ![GitHub Repo stars](https://img.shields.io/github/stars/HumanAIGC-Engineering/OpenAvatarChat)
- [pensieve](https://github.com/arkohut/pensieve): A privacy-focused passive recording project by recording screen content ![GitHub Repo stars](https://img.shields.io/github/stars/arkohut/pensieve)
- [paperless-gpt](https://github.com/icereed/paperless-gpt): Use LLMs to handle paperless-ngx, AI-powered titles, tags and OCR ![GitHub Repo stars](https://img.shields.io/github/stars/icereed/paperless-gpt)
- [Neuro](https://github.com/kimjammer/Neuro): A recreation of Neuro-Sama, but running on local models on consumer hardware ![GitHub Repo stars](https://img.shields.io/github/stars/kimjammer/Neuro)

## 👥 Community

### Contributing

We love new recipes! Please share your creative dishes:

1. Fork the repository
2. Create your recipe
3. Submit a pull request

### Issues & Support

- Found a bug? [Open an issue](https://github.com/OpenBMB/MiniCPM-o/issues)
- Need help? Join our [Discord](https://discord.gg/rftuRMbqzf)


## 📜 License

This cookbook is served under the [Apache-2.0 License](LICENSE) - cook freely, share generously! 🍳
