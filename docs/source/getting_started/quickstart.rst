Quickstart
==========

1. Installation
---------------

.. code-block:: bash

    pip install -r inference/requirements.txt

2. Basic Usage
--------------

.. code-block:: python

    import torch
    from transformers import AutoModel, AutoTokenizer
    from PIL import Image

    # Load the model
    model = AutoModel.from_pretrained('openbmb/MiniCPM-V-4', trust_remote_code=True)
    tokenizer = AutoTokenizer.from_pretrained('openbmb/MiniCPM-V-4', trust_remote_code=True)

    # Start inference!
    # See our recipe notebooks for detailed instructions


🍽️ Menu
-------

🔥 Inference recipes
********************


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


.. list-table::
   :widths: 25 75
   :header-rows: 1

   * - Framework
     - Description
   * - `Transformers <../finetune/fintune.html#full-parameter-finetuning>`_
     - Most flexible for customization
   * - `LLaMA-Factory <../finetune/llamafactory.html>`_
     - Modular fine-tuning toolkit
   * - `SWIFT <../finetune/swift.html>`_
     - Lightweight and fast parameter-efficient tuning
   * - `Align-anything <../finetune/align-anything.html>`_
     - Visual instruction alignment for multimodal models


.. _serving-recipe:

🥡 Serving recipes
******************


.. list-table::
   :widths: 25 75
   :header-rows: 1

   * - Method
     - Description
   * - `vLLM <../deployment/vllm.html>`_
     - High-throughput GPU inference
   * - `SGLang <../deployment/sglang.html>`_
     - High-throughput GPU inference
   * - `Llama.cpp <../run_locally/llama.cpp.html>`_
     - Fast inference on PC, iPhone and iPad  
   * - `Ollama <../run_locally/ollama.html>`_
     - User-friendly setup
   * - `Fast API <../demo/webdemo.html>`_
     - Interactive Omni Streaming demo with FastAPI
   * - `OpenWebUI <../demo/openwebui.html>`_
     - Interactive Web demo with Open WebUI
   * - `iOS Demo <../demo/iosdemo.html>`_
     - Interactive iOS demo with llama.cpp


.. _quantization-recipe:

🥄 Quantization recipes
***********************


.. list-table::
   :widths: 25 75
   :header-rows: 1

   * - Format
     - Key Feature
   * - `GGUF <../quantization/gguf.html>`_
     - Simplest and most portable format
   * - `BNB <../quantization/bnb.html>`_
     - Efficient 4/8-bit weight quantization