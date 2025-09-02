<div align="center">

# 🍳 MiniCPM-V & o Cookbook


[🏠 Main Repository](https://github.com/OpenBMB/MiniCPM-o) | [📚 Full Documentation](https://minicpm-o.readthedocs.io/en/latest/index.html)

Cook up amazing multimodal AI applications effortlessly with MiniCPM-o, bringing vision, speech, and live-streaming capabilities right to your fingertips!

</div>


## ✨ What Makes Our Recipes Special?

### Easy Usage Documentation

Our comprehensive [documentation website](https://minicpm-o.readthedocs.io/en/latest/index.html) presents every recipe in a clear, well-organized manner.
All features are displayed at a glance, making it easy for you to quickly find exactly what you need.

### Broad User Spectrum

We support a wide range of users, from individuals to enterprises and researchers.

* **Individuals**: Enjoy effortless inference using [Ollama](./deployment/ollama/minicpm-v4_5_ollama.md) and [Llama.cpp](./deployment/llama.cpp/minicpm-v4_5_llamacpp.md) with minimal setup.
* **Enterprises**: Achieve high-throughput, scalable performance with [vLLM](./deployment/vllm/minicpm-v4_5_vllm.md) and [SGLang](./deployment/sglang/MiniCPM-v4_5_sglang.md).
* **Researchers**: Leverage advanced frameworks including [Transformers](./finetune/finetune_full.md) , [LLaMA-Factory](./finetune/finetune_llamafactory.md), [SWIFT](./finetune/swift.md), and [Align-anything](./finetune/align_anything.md) to enable flexible model development and cutting-edge experimentation.


### Versatile Deployment Scenarios

Our ecosystem delivers optimal solution for a variety of hardware environments and deployment demands.

* **Web demo**: Launch interactive multimodal AI web demo with [FastAPI](./demo/README.md).
* **Quantized deployment**: Maximize efficiency and minimize resource consumption using [GGUF](./quantization/gguf/minicpm-v4_5_gguf_quantize.md), [BNB](./quantization/bnb/minicpm-v4_5_bnb_quantize.md), and [AWQ](./quantization/awq/minicpm-v4_awq_quantize.md).
* **Edge devices**: Bring powerful AI experiences to [iPhone and iPad](./demo/ios_demo/ios.md), supporting offline and privacy-sensitive applications.

## ⭐️ Live Demonstrations

Explore real-world examples of MiniCPM-V deployed on edge devices using our curated recipes. These demos highlight the model’s high efficiency and robust performance in practical scenarios.

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
| 🖼️ [Single-image QA](./inference/minicpm-v4_5_single_image.md) | Question answering on a single image |
| 🧩 [Multi-image QA](./inference/minicpm-v4_5_multi_images.md) | Question answering with multiple images |
| 🎬 [Video QA](./inference/minicpm-v4_5_video_understanding.md) | Video-based question answering |
| 📄 [Document Parser](./inference/minicpm-v4_5_pdf_parse.md) | Parse and extract content from PDFs and webpages |
| 📝 [Text Recognition](./inference/minicpm-v4_5_ocr.md) | Reliable OCR for photos and screenshots |
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
| [vLLM](./deployment/vllm/minicpm-v4_5_vllm.md)| High-throughput GPU inference                |
| [SGLang](./deployment/sglang/MiniCPM-v4_5_sglang.md)| High-throughput GPU inference                |
| [Llama.cpp](./deployment/llama.cpp/minicpm-v4_5_llamacpp.md)| Fast CPU inference on PC, iPhone and iPad                        |
| [Ollama](./deployment/ollama/minicpm-v4_5_ollama.md)| User-friendly setup  |
| [OpenWebUI](./demo/web_demo/openwebui) | Interactive Web demo with Open WebUI |
| [Gradio](./demo/web_demo/gradio/README.md) | Interactive Web demo with Gradio |
| [FastAPI](./demo/README.md) | Interactive Omni Streaming demo with FastAPI |
| [iOS](./demo/ios_demo/ios.md) | Interactive iOS demo with llama.cpp |

## 🥄 Quantization Recipes
> *Compress your model to improve efficiency*

| Format                                 | Key Feature                        |
|-----------------------------------------|------------------------------------|
| [GGUF](./quantization/gguf/minicpm-v4_5_gguf_quantize.md)| Simplest and most portable format  |
| [BNB](./quantization/bnb/minicpm-v4_5_bnb_quantize.md)   | Simple and easy-to-use quantization method |
| [AWQ](./quantization/awq/minicpm-v4_awq_quantize.md)   | High-performance quantization for efficient inference |

## Framework Support Matrix
<table>
  <thead>
    <tr>
      <th>Category</th>
      <th>Framework</th>
      <th>Cookbook Link</th>
      <th>Upstream PR</th>
      <th>Supported since (branch)</th>
      <th>Supported since (release)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td rowspan="2">Edge (On-device)</td>
      <td>Llama.cpp</td>
      <td><a href="https://github.com/OpenSQZ/MiniCPM-V-CookBook/blob/main/deployment/llama.cpp/minicpm-v4_5_llamacpp.md">Llama.cpp Doc</a></td>
      <td><a href="https://github.com/ggml-org/llama.cpp/pull/15575">#15575</a> (2025-08-26)</td>
      <td>master (2025-08-26)</td>
      <td><a href="https://github.com/ggml-org/llama.cpp/releases/tag/b6282">b6282</a></td>
    </tr>
    <tr>
      <td>Ollama</td>
      <td><a href="https://github.com/OpenSQZ/MiniCPM-V-CookBook/blob/main/deployment/ollama/minicpm-v4_5_ollama.md">Ollama Doc</a></td>
      <td><a href="https://github.com/ollama/ollama/pull/12078">#12078</a> (2025-08-26)</td>
      <td>Merging</td>
      <td>Waiting for official release</td>
    </tr>
    <tr>
      <td rowspan="2">Serving (Cloud)</td>
      <td>vLLM</td>
      <td><a href="https://github.com/OpenSQZ/MiniCPM-V-CookBook/blob/main/deployment/vllm/minicpm-v4_5_vllm.md">vLLM Doc</a></td>
      <td><a href="https://github.com/vllm-project/vllm/pull/23586">#23586</a> (2025-08-26)</td>
      <td>main (2025-08-27)</td>
      <td>Waiting for official release</td>
    </tr>
    <tr>
      <td>SGLang</td>
      <td><a href="https://github.com/OpenSQZ/MiniCPM-V-CookBook/blob/main/deployment/sglang/MiniCPM-v4_5_sglang.md">SGLang Doc</a></td>
      <td><a href="https://github.com/sgl-project/sglang/pull/9610">#9610</a> (2025-08-26)</td>
      <td>Merging</td>
      <td>Waiting for official release</td>
    </tr>
    <tr>
      <td>Finetuning</td>
      <td>LLaMA-Factory</td>
      <td><a href="https://github.com/OpenSQZ/MiniCPM-V-CookBook/blob/main/finetune/finetune_llamafactory.md">LLaMA-Factory Doc</a></td>
      <td><a href="https://github.com/hiyouga/LLaMA-Factory/pull/9022">#9022</a> (2025-08-26)</td>
      <td>main (2025-08-26)</td>
      <td>Waiting for official release</td>
    </tr>
    <tr>
      <td rowspan="3">Quantization</td>
      <td>GGUF</td>
      <td><a href="https://github.com/OpenSQZ/MiniCPM-V-CookBook/blob/main/quantization/gguf/minicpm-v4_5_gguf_quantize.md">GGUF Doc</a></td>
      <td>—</td>
      <td>—</td>
      <td>—</td>
    </tr>
    <tr>
      <td>BNB</td>
      <td><a href="https://github.com/OpenSQZ/MiniCPM-V-CookBook/blob/main/quantization/bnb/minicpm-v4_5_bnb_quantize.md">BNB Doc</a></td>
      <td>—</td>
      <td>—</td>
      <td>—</td>
    </tr>
    <tr>
      <td>AWQ</td>
      <td><a href="https://github.com/OpenSQZ/MiniCPM-V-CookBook/blob/main/quantization/awq/minicpm-v4_5_awq_quantize.md">AWQ Doc</a></td>
      <td>—</td>
      <td>—</td>
      <td>—</td>
    </tr>
    <tr>
      <td>Demos</td>
      <td>Gradio Demo</td>
      <td><a href="https://github.com/OpenSQZ/MiniCPM-V-CookBook/blob/main/demo/web_demo/gradio/README.md">Gradio Demo Doc</a></td>
      <td>—</td>
      <td>—</td>
      <td>—</td>
    </tr>
  </tbody>
 </table>


If you'd like us to prioritize support for another open-source framework, please let us know via this
[short form](https://docs.google.com/forms/d/e/1FAIpQLSdyTUrOPBgWqPexs3ORrg47ZcZ1r4vFQaA4ve2iA7L9sMfMWw/viewform).


## Awesome Works using MiniCPM-V & o
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


## Institutions

This cookbook is developed by [OpenBMB](https://github.com/openbmb) and [OpenSQZ](https://github.com/opensqz).



## 📜 License

This cookbook is served under the [Apache-2.0 License](LICENSE) - cook freely, share generously! 🍳

## Citation <!-- omit in toc -->

If you find our model/code/paper helpful, please consider citing our papers 📝 and staring us ⭐️！

```bib
@article{yao2024minicpm,
  title={MiniCPM-V: A GPT-4V Level MLLM on Your Phone},
  author={Yao, Yuan and Yu, Tianyu and Zhang, Ao and Wang, Chongyi and Cui, Junbo and Zhu, Hongji and Cai, Tianchi and Li, Haoyu and Zhao, Weilin and He, Zhihui and others},
  journal={arXiv preprint arXiv:2408.01800},
  year={2024}
}
```
