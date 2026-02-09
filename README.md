<div align="center">

# 🍳 MiniCPM-o Cookbook


[🏠 Main Repository](https://github.com/OpenBMB/MiniCPM-o) | [📚 Full Documentation](https://minicpm-o.readthedocs.io/en/latest/index.html)

Cook up amazing multimodal AI applications effortlessly with MiniCPM-o, bringing vision, speech, and live-streaming capabilities right to your fingertips! For version-specific deployment instructions, see the files in the [deployment](./deployment/) directory.

</div>


## ✨ What Makes Our Recipes Special?

### Easy Usage Documentation

Our comprehensive [documentation website](https://minicpm-o.readthedocs.io/en/latest/index.html) presents every recipe in a clear, well-organized manner.
All features are displayed at a glance, making it easy for you to quickly find exactly what you need.

### Broad User Spectrum

We support a wide range of users, from individuals to enterprises and researchers.

* **Individuals**: Enjoy effortless inference using [Ollama](./deployment/ollama/minicpm-o4_5_ollama.md) and [Llama.cpp](./deployment/llama.cpp/minicpm-o4_5_llamacpp.md) with minimal setup.
* **Enterprises**: Achieve high-throughput, scalable performance with [vLLM](./deployment/vllm/minicpm-o4_5_vllm.md) and [SGLang](./deployment/sglang/MiniCPM-o4_5_sglang.md).
* **Researchers**: Leverage advanced frameworks including [Transformers](./finetune/finetune_full.md) , [LLaMA-Factory](./finetune/finetune_llamafactory.md), [SWIFT](./finetune/swift.md), and [Align-anything](./finetune/align_anything.md) to enable flexible model development and cutting-edge experimentation.


### Versatile Deployment Scenarios

Our ecosystem delivers optimal solution for a variety of hardware environments and deployment demands.

* **Web demo**: Launch interactive multimodal AI web demo with [FastAPI](./demo/README.md) for streaming omni capabilities.
* **Quantized deployment**: Maximize efficiency and minimize resource consumption using [GGUF](./quantization/gguf/minicpm-o4_5_gguf_quantize.md) and [AWQ](./quantization/awq/minicpm-o4_5_awq_quantize.md).
* **Full-modal inference**: Experience seamless vision, speech, and text interaction with our omni models.

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
| 🌐 [Omni Recognition](./inference/omni_recognition.md) | Full-modal understanding with vision, audio, and text |
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

| [Align-anything](./finetune/align_anything.md) | Visual instruction alignment for multimodal models |



## 📦 Serving Recipes
> *Deploy your model efficiently*

| Method                                | Description                                  |
|-------------------------------------------|----------------------------------------------|
| [vLLM](./deployment/vllm/minicpm-o4_5_vllm.md)| High-throughput GPU inference                |
| [SGLang](./deployment/sglang/MiniCPM-o4_5_sglang.md)| High-throughput GPU inference                |
| [Llama.cpp](./deployment/llama.cpp/minicpm-o4_5_llamacpp.md)| Fast CPU inference on PC                        |
| [Ollama](./deployment/ollama/minicpm-o4_5_ollama.md)| User-friendly setup  |
| [OpenWebUI](./demo/web_demo/openwebui) | Interactive Web demo with Open WebUI |
| [Gradio](./demo/web_demo/gradio/README_o45.md) | Interactive Web demo with Gradio |
| [FastAPI](./demo/README.md) | Interactive Omni Streaming demo with FastAPI |

## 🥄 Quantization Recipes
> *Compress your model to improve efficiency*

| Format                                 | Key Feature                        |
|-----------------------------------------|------------------------------------|
| [GGUF](./quantization/gguf/minicpm-o4_5_gguf_quantize.md)| Simplest and most portable format  |
| [AWQ](./quantization/awq/minicpm-o4_5_awq_quantize.md)   | High-performance quantization for efficient inference |

## Framework Support Matrix
<table>
  <thead>
    <tr>
      <th>Category</th>
      <th>Framework</th>
      <th>Cookbook Link</th>
      <th>Upstream PR</th>
      <th>Supported since(branch)</th>
      <th>Supported since(release)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td rowspan="2">Edge(On-device)</td>
      <td>Llama.cpp</td>
      <td><a href="https://github.com/OpenSQZ/MiniCPM-o-CookBook/blob/main/deployment/llama.cpp/minicpm-o4_5_llamacpp.md">Llama.cpp Doc</a></td>
      <td><a href="https://github.com/ggml-org/llama.cpp/pull/19211">#19211</a>(2026-01-30)</td>
      <td>master(2026-01-30)</td>
      <td><a href="https://github.com/ggml-org/llama.cpp/releases/tag/b7895">b7895</a></td>
    </tr>
    <tr>
      <td>Ollama</td>
      <td><a href="https://github.com/OpenSQZ/MiniCPM-o-CookBook/blob/main/deployment/ollama/minicpm-o4_5_ollama.md">Ollama Doc</a></td>
      <td><a href="https://github.com/ollama/ollama/pull/12078">#12078</a>(2025-08-26)</td>
      <td>Merging</td>
      <td>Waiting for official release</td>
    </tr>
    <tr>
      <td rowspan="2">Serving(Cloud)</td>
      <td>vLLM</td>
      <td><a href="https://github.com/OpenSQZ/MiniCPM-o-CookBook/blob/main/deployment/vllm/minicpm-o4_5_vllm.md">vLLM Doc</a></td>
      <td><a href="https://github.com/vllm-project/vllm/pull/33431">#33431</a>(2026-01-30)</td>
      <td>Merging</td>
      <td>Waiting for official release</td>
    </tr>
    <tr>
      <td>SGLang</td>
      <td><a href="https://github.com/OpenSQZ/MiniCPM-o-CookBook/blob/main/deployment/sglang/MiniCPM-o4_5_sglang.md">SGLang Doc</a></td>
      <td><a href="https://github.com/sgl-project/sglang/pull/9610">#9610</a>(2025-08-26)</td>
      <td>Merging</td>
      <td>Waiting for official release</td>
    </tr>
    <tr>
      <td>Finetuning</td>
      <td>LLaMA-Factory</td>
      <td><a href="https://github.com/OpenSQZ/MiniCPM-o-CookBook/blob/main/finetune/finetune_llamafactory.md">LLaMA-Factory Doc</a></td>
      <td><a href="https://github.com/hiyouga/LLaMA-Factory/pull/9022">#9022</a>(2025-08-26)</td>
      <td>main(2025-08-26)</td>
      <td>Waiting for official release</td>
    </tr>
    <tr>
      <td rowspan="2">Quantization</td>
      <td>GGUF</td>
      <td><a href="https://github.com/OpenSQZ/MiniCPM-o-CookBook/blob/main/quantization/gguf/minicpm-o4_5_gguf_quantize.md">GGUF Doc</a></td>
      <td>—</td>
      <td>—</td>
      <td>—</td>
    </tr>
    <tr>
      <td>AWQ</td>
      <td><a href="https://github.com/OpenSQZ/MiniCPM-o-CookBook/blob/main/quantization/awq/minicpm-o4_5_awq_quantize.md">AWQ Doc</a></td>
      <td><a href="https://github.com/tc-mb/AutoAWQ">tc-mb/AutoAWQ</a></td>
      <td>—</td>
      <td>—</td>
    </tr>
    <tr>
      <td>Demos</td>
      <td>Gradio Demo</td>
      <td><a href="https://github.com/OpenSQZ/MiniCPM-o-CookBook/blob/main/demo/web_demo/gradio/README_o45.md">Gradio Demo Doc</a></td>
      <td>—</td>
      <td>—</td>
      <td>—</td>
    </tr>
  </tbody>
 </table>


If you'd like us to prioritize support for another open-source framework, please let us know via this
[short form](https://docs.google.com/forms/d/e/1FAIpQLSdyTUrOPBgWqPexs3ORrg47ZcZ1r4vFQaA4ve2iA7L9sMfMWw/viewform).


## Awesome Works using MiniCPM-o
- [OpenAvatarChat](https://github.com/HumanAIGC-Engineering/OpenAvatarChat): Interactive digital human conversation implementation on single PC ![GitHub Repo stars](https://img.shields.io/github/stars/HumanAIGC-Engineering/OpenAvatarChat)
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
@misc{yu2025minicpmv45cookingefficient,
      title={MiniCPM-o 4.5: A Gemini 2.5 Flash Level MLLM for Vision, Speech, and Full-Duplex Mulitmodal Live Streaming on Your Phone}, 
      author={Tianyu Yu and Zefan Wang and Chongyi Wang and Fuwei Huang and Wenshuo Ma and Zhihui He and Tianchi Cai and Weize Chen and Yuxiang Huang and Yuanqian Zhao and Bokai Xu and Junbo Cui and Yingjing Xu and Liqing Ruan and Luoyuan Zhang and Hanyu Liu and Jingkun Tang and Hongyuan Liu and Qining Guo and Wenhao Hu and Bingxiang He and Jie Zhou and Jie Cai and Ji Qi and Zonghao Guo and Chi Chen and Guoyang Zeng and Yuxuan Li and Ganqu Cui and Ning Ding and Xu Han and Yuan Yao and Zhiyuan Liu and Maosong Sun},
      year={2025},
      eprint={2509.18154},
      archivePrefix={arXiv},
      primaryClass={cs.LG},
      url={https://arxiv.org/abs/2509.18154}, 
}

@article{yao2024minicpm,
  title={MiniCPM-V: A GPT-4V Level MLLM on Your Phone},
  author={Yao, Yuan and Yu, Tianyu and Zhang, Ao and Wang, Chongyi and Cui, Junbo and Zhu, Hongji and Cai, Tianchi and Li, Haoyu and Zhao, Weilin and He, Zhihui and others},
  journal={Nat Commun 16, 5509 (2025)},
  year={2025}
}

```
