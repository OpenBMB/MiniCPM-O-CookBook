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

🔥 Inference recipes
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
   * - `Fast API <./demo/webdemo.html>`_
     - Interactive Omni Streaming demo with FastAPI
   * - `OpenWebUI <./demo/openwebui.html>`_
     - Interactive Web demo with Open WebUI
   * - `Gradio Web Demo <./demo/gradiodemo.html>`_
     - Interactive Web demo with Gradio
   * - `iOS Demo <./demo/iosdemo.html>`_
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