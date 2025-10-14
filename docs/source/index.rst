.. MiniCPM Cookbook documentation master file, created by
   sphinx-quickstart on Sat Jul 12 18:12:12 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to MiniCPM-V & o Cookbook
==================================

.. figure:: assets/minicpm.svg
  :width: 70%
  :align: center
  :alt: MiniCPM
  :class: no-scaled-link

.. raw:: html

   <br>

.. _`🏠 Main Repository`: https://github.com/OpenBMB/MiniCPM-o 
.. _`🤗 Hugging Face`: https://huggingface.co/openbmb/MiniCPM-V-4_5 
.. _`🤖 ModelScope`: https://modelscope.cn/models/openbmb/MiniCPM-V-4_5 
.. _`📖 Technical Blog`: https://huggingface.co/papers/2509.18154
| `🏠 Main Repository`_  |  `🤗 Hugging Face`_  |  `🤖 ModelScope`_  |  `📖 Technical Blog`_ 

Cook up amazing multimodal AI applications effortlessly with MiniCPM-o / MiniCPM-V, bringing vision, speech, and live-streaming capabilities right to your fingertips!


✨ What Makes Our Recipes Special?
**********************************

Easy Usage Documentation
~~~~~~~~~~~~~~~~~~~~~~~~

Our comprehensive `documentation website <https://minicpm-o.readthedocs.io/en/latest/index.html>`_
presents every recipe in a clear, well-organized manner.
All features are displayed at a glance, making it easy for you to quickly find exactly what you need.

Broad User Spectrum
~~~~~~~~~~~~~~~~~~~

We support a wide range of users, from individuals to enterprises and researchers.

* Individuals: Enjoy effortless inference using **Ollama** and **Llama.cpp** with minimal setup.
* Enterprises: Achieve high-throughput, scalable performance with **vLLM** and **SGLang**.
* Researchers: Leverage advanced frameworks including **Transformers**, **LLaMA-Factory**, **SWIFT**, and **Align-anything** to enable flexible model development and cutting-edge experimentation.

Versatile Deployment Scenarios
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Our ecosystem delivers optimal solution for a variety of hardware environments and deployment demands.

* Private Web demo: Launch interactive multimodal AI web demo with **FastAPI**.
* Quantized deployment: Maximize efficiency and minimize resource consumption using **GGUF** and **BNB**.
* Edge devices: Bring powerful AI experiences directly to **iPhone** and **iPad**, supporting mobile and privacy-sensitive applications.

⭐️ Live Demonstrations
*********************

Explore real-world examples of MiniCPM-V deployed on edge devices using our curated recipes. 
These demos highlight the model’s high efficiency and robust performance in practical scenarios.

Run locally on iPhone with `iOS demo <demo/iosdemo.html>`_.

.. raw:: html

   <p align="center">
     <img src="../inference/assets/gif_cases/iphone_cn.gif" width="32%">
     &nbsp;&nbsp;&nbsp;&nbsp;
     <img src="../inference/assets/gif_cases/iphone_en.gif" width="32%">
   </p>

Run locally on iPad with `iOS demo <demo/iosdemo.html>`_, observing the process of drawing a rabbit.

.. raw:: html

   <p align="center">
     <video width="360" controls>
       <source src="https://github.com/user-attachments/assets/43659803-8fa4-463a-a22c-46ad108019a7" type="video/mp4">
       Your browser does not support the video tag.
     </video>
   </p>


🔥 Inference Recipes
********************

*Ready-to-run examples*

.. list-table::
   :widths: 25 75
   :header-rows: 1

   * - Recipe
     - Description

   * - **Vision Capabilities**
     - 

   * - 🎬 `Video QA <https://github.com/OpenSQZ/MiniCPM-o-cookbook/blob/main/inference/video_understanding.md>`_
     - Video-based question answering

   * - 🧩 `Multi-image QA <https://github.com/OpenSQZ/MiniCPM-o-cookbook/blob/main/inference/multi_images.md>`_
     - Question answering with multiple images

   * - 🖼️ `Single-image QA <https://github.com/OpenSQZ/MiniCPM-o-cookbook/blob/main/inference/single_image.md>`_
     - Question answering on a single image

   * - 📄 `Document Parser <https://github.com/OpenSQZ/MiniCPM-o-cookbook/blob/main/inference/pdf_parse.md>`_
     - Parse and extract content from PDFs and webpages

   * - 📝 `Text Recognition <https://github.com/OpenSQZ/MiniCPM-o-cookbook/blob/main/inference/ocr.md>`_
     - Reliable OCR for photos and screenshots

   * - **Audio Capabilities**
     -

   * - 🎤 `Speech-to-Text <https://github.com/OpenSQZ/MiniCPM-o-cookbook/blob/main/inference/speech2text.md>`_
     - Multilingual speech recognition

   * - 🎭 `Voice Cloning <https://github.com/OpenSQZ/MiniCPM-o-cookbook/blob/main/inference/voice_clone.md>`_
     - Realistic voice cloning and role-play

   * - 🗣️ `Text-to-Speech <https://github.com/OpenSQZ/MiniCPM-o-cookbook/blob/main/inference/text2speech.md>`_
     - Instruction-following speech synthesis

🏋️ Fine-tuning recipes
**********************

*Customize your model with your own ingredients*

**Data preparation**

Follow the `guidance <./finetune/fintune.html#data-preparation>`_ to set up your training datasets.


**Training**

We provide training methods serving different needs as following:

.. list-table::
   :widths: 25 75
   :header-rows: 1

   * - Framework
     - Description
   * - `Transformers <./finetune/fintune.html#full-parameter-finetuning>`_
     - Most flexible for customization
   * - `LLaMA-Factory <./finetune/llamafactory.html>`_
     - Modular fine-tuning toolkit
   * - `SWIFT <./finetune/swift.html>`_
     - Lightweight and fast parameter-efficient tuning
   * - `Align-anything <./finetune/align-anything.html>`_
     - Visual instruction alignment for multimodal models


.. _serving-recipes:

📦 Serving recipes
******************

*Deploy your model efficiently*

.. list-table::
   :widths: 25 75
   :header-rows: 1

   * - Method
     - Description
   * - `vLLM <./deployment/vllm.html>`_
     - High-throughput GPU inference
   * - `SGLang <./deployment/sglang.html>`_
     - High-throughput GPU inference
   * - `Llama.cpp <./run_locally/llama.cpp.html>`_
     - Fast inference on PC, iPhone and iPad  
   * - `Ollama <./run_locally/ollama.html>`_
     - User-friendly setup
   * - `OpenWebUI <./demo/openwebui.html>`_
     - Interactive Web demo with Open WebUI
   * - `Gradio <./demo/web_demo/gradio/README.html>`_
     - Interactive Web demo with Gradio
   * - `FastAPI <./demo/webdemo.html>`_
     - Interactive Omni Streaming demo with FastAPI
   * - `iOS <./demo/ios_demo/ios.html>`_
     - Interactive iOS demo with llama.cpp


.. _quantization-recipes:

🥄 Quantization recipes
***********************
*Compress your model to improve efficiency*

.. list-table::
   :widths: 25 75
   :header-rows: 1

   * - Format
     - Key Feature
   * - `GGUF <./quantization/gguf.html>`_
     - Simplest and most portable format
   * - `BNB <./quantization/bnb.html>`_
     - Simple and easy-to-use quantization method
   * - `AWQ <./quantization/awq.html>`_
     - High-performance quantization for efficient inference

.. _support-matrix:

Framework Support Matrix
************************

.. list-table::
   :widths: 15 15 25 15 15 15
   :header-rows: 1

   * - Category
     - Framework
     - Cookbook Link
     - Upstream PR
     - Supported since (branch)
     - Supported since (release)

   * - Edge (On-device)
     - Llama.cpp
     - `Llama.cpp Doc <https://github.com/OpenSQZ/MiniCPM-V-CookBook/blob/main/deployment/llama.cpp/minicpm-v4_5_llamacpp.md>`_
     - `#15575 <https://github.com/ggml-org/llama.cpp/pull/15575>`_ (2025-08-26)
     - master (2025-08-26)
     - `b6282 <https://github.com/ggml-org/llama.cpp/releases/tag/b6282>`_

   * - 
     - Ollama
     - `Ollama Doc <https://github.com/OpenSQZ/MiniCPM-V-CookBook/blob/main/deployment/ollama/minicpm-v4_5_ollama.md>`_
     - `#12078 <https://github.com/ollama/ollama/pull/12078>`_ (2025-08-26)
     - Merging
     - Waiting for official release

   * - Serving (Cloud)
     - vLLM
     - `vLLM Doc <https://github.com/OpenSQZ/MiniCPM-V-CookBook/blob/main/deployment/vllm/minicpm-v4_5_vllm.md>`_
     - `#23586 <https://github.com/vllm-project/vllm/pull/23586>`_ (2025-08-26)
     - main (2025-08-27)
     - `v0.10.2 <https://github.com/vllm-project/vllm/releases/tag/v0.10.2>`_

   * - 
     - SGLang
     - `SGLang Doc <https://github.com/OpenSQZ/MiniCPM-V-CookBook/blob/main/deployment/sglang/MiniCPM-v4_5_sglang.md>`_
     - `#9610 <https://github.com/sgl-project/sglang/pull/9610>`_ (2025-08-26)
     - Merging
     - Waiting for official release

   * - Finetuning
     - LLaMA-Factory
     - `LLaMA-Factory Doc <https://github.com/OpenSQZ/MiniCPM-V-CookBook/blob/main/finetune/finetune_llamafactory.md>`_
     - `#9022 <https://github.com/hiyouga/LLaMA-Factory/pull/9022>`_ (2025-08-26)
     - main (2025-08-26)
     - Waiting for official release

   * - Quantization
     - GGUF
     - `GGUF Doc <https://github.com/OpenSQZ/MiniCPM-V-CookBook/blob/main/quantization/gguf/minicpm-v4_5_gguf_quantize.md>`_
     - —
     - —
     - —

   * - 
     - BNB
     - `BNB Doc <https://github.com/OpenSQZ/MiniCPM-V-CookBook/blob/main/quantization/bnb/minicpm-v4_5_bnb_quantize.md>`_
     - —
     - —
     - —

   * - 
     - AWQ
     - `AWQ Doc <https://github.com/OpenSQZ/MiniCPM-V-CookBook/blob/main/quantization/awq/minicpm-v4_5_awq_quantize.md>`_
     - —
     - —
     - —

   * - Demos
     - Gradio Demo
     - `Gradio Demo Doc <https://github.com/OpenSQZ/MiniCPM-V-CookBook/blob/main/demo/web_demo/gradio/README.md>`_
     - —
     - —
     - —

If you'd like us to prioritize support for another open-source framework,
please let us know via this
`short form <https://docs.google.com/forms/d/e/1FAIpQLSdyTUrOPBgWqPexs3ORrg47ZcZ1r4vFQaA4ve2iA7L9sMfMWw/viewform>`_.


Awesome Works using MiniCPM-V & o
=================================

* `text-extract-api <https://github.com/CatchTheTornado/text-extract-api>`_ — Document extraction API using OCRs and Ollama supported models
* `comfyui_LLM_party <https://github.com/heshengtao/comfyui_LLM_party>`_ — Build LLM workflows and integrate into existing image workflows
* `Ollama-OCR <https://github.com/imanoop7/Ollama-OCR>`_ — OCR package uses VLMs through Ollama to extract text from images and PDFs
* `comfyui-mixlab-nodes <https://github.com/MixLabPro/comfyui-mixlab-nodes>`_ — ComfyUI node suite supports Workflow-to-APP、GPT&3D and more
* `OpenAvatarChat <https://github.com/HumanAIGC-Engineering/OpenAvatarChat>`_ — Interactive digital human conversation implementation on single PC
* `pensieve <https://github.com/arkohut/pensieve>`_ — A privacy-focused passive recording project by recording screen content
* `paperless-gpt <https://github.com/icereed/paperless-gpt>`_ — Use LLMs to handle paperless-ngx, AI-powered titles, tags and OCR
* `Neuro <https://github.com/kimjammer/Neuro>`_ — A recreation of Neuro-Sama, but running on local models on consumer hardware


.. _community:

👥 Community
============

.. _contributing:

**Contributing**

We love new recipes! Please share your creative dishes:

1. Fork the repository
2. Create your recipe
3. Submit a pull request


.. _issues-support:

**Issues & Support**

- Found a bug? `Open an issue <https://github.com/OpenBMB/MiniCPM-o/issues>`__
- Need help? Join our `Discord <https://discord.gg/rM6sC9G2MA>`__ and `WeChat <https://github.com/OpenBMB/MiniCPM-o/blob/main/assets/wechat-QR.jpeg>`__ group.

For more information, please visit our:

* `GitHub <https://github.com/OpenBMB>`__
* `Hugging Face <https://huggingface.co/OpenBMB>`__
* `Modelscope <https://modelscope.cn/organization/OpenBMB>`__

.. toctree::
   :maxdepth: 1
   :caption: Getting Started
   :hidden:

   getting_started/quickstart
   getting_started/model_download

.. toctree::
   :maxdepth: 1
   :caption: Inference
   :hidden:

   inference/transformers

.. toctree::
   :maxdepth: 1
   :caption: Deployment
   :hidden:

   deployment/vllm
   deployment/sglang

.. toctree::
   :maxdepth: 1
   :caption: Run Locally
   :hidden:

   run_locally/llama.cpp
   run_locally/ollama

.. toctree::
   :maxdepth: 1
   :caption: Quantization
   :hidden:

   quantization/awq
   quantization/bnb
   quantization/gguf
   

.. toctree::
   :maxdepth: 1
   :caption: finetune
   :hidden:

   finetune/fintune
   finetune/llamafactory
   finetune/swift
   finetune/align-anything
   
.. toctree::
   :maxdepth: 1
   :caption: Demo
   :hidden:

   demo/gradiodemo
   demo/webdemo
   demo/openwebui
   demo/iosdemo