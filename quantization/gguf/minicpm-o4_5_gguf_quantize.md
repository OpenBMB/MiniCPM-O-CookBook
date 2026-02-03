# MiniCPM-o 4.5 - GGUF Quantization Guide

This guide will walk you through the process of converting the MiniCPM-o 4.5 PyTorch model to GGUF format and performing quantization.

Models in this guide need to be used with [`llama.cpp`](../../deployment/llama.cpp/minicpm-o4_5_llamacpp.md)/[`ollama`](../../deployment/ollama/minicpm-o4_5_ollama.md).

### 1. Download the PyTorch Model

First, obtain the original PyTorch model files from one of the following sources:

*   **HuggingFace:** https://huggingface.co/openbmb/MiniCPM-o-4_5
*   **ModelScope Community:** https://modelscope.cn/models/OpenBMB/MiniCPM-o-4_5

### 2. Convert the PyTorch Model to GGUF Format

Run the following bash to perform model surgery and convert the model.

```bash
bash ./tools/omni/convert/run_convert.sh

# You need to modify the paths in the script:
MODEL_DIR="/path/to/MiniCPM-o-4_5"  # Source model
LLAMACPP_DIR="/path/to/llamacpp"    # llamacpp directory
OUTPUT_DIR="${CONVERT_DIR}/gguf"    # Output directory
PYTHON="/path/to/python"            # Python path
```

### 3. Perform INT4 Quantization

Once the conversion is complete, use the `llama-quantize` tool to quantize the F16 precision GGUF model to INT4.

```bash
./llama-quantize ./tools/omni/convert/gguf/Llm-8.2B-F16.gguf ./tools/omni/convert/gguf/Llm-8.2B-Q4_K_M.gguf Q4_K_M
```
