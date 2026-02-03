# MiniCPM-o 4.5 - GGUF 量化指南

本指南将引导您完成将 MiniCPM-o 4.5 PyTorch 模型转换为 GGUF 格式并进行量化的过程。

本指南涉及的模型需要基于 [`llama.cpp`](../../deployment/llama.cpp/minicpm-o4_5_llamacpp_zh.md)/[`ollama`](../../deployment/ollama/minicpm-o4_5_ollama_zh.md) 使用。

### 1. 下载 PyTorch 模型

首先，请从以下任一来源获取原始的 PyTorch 模型文件：

*   **HuggingFace:** https://huggingface.co/openbmb/MiniCPM-o-4_5
*   **魔搭社区:** https://modelscope.cn/models/OpenBMB/MiniCPM-o-4_5

### 2. 将 PyTorch 模型转换为 GGUF 格式

请执行以下脚本，以完成模型结构调整和模型转换。

```bash
bash ./tools/omni/convert/run_convert.sh

# 需要修改脚本中的路径：
MODEL_DIR="/path/to/MiniCPM-o-4_5"  # 源模型
LLAMACPP_DIR="/path/to/llamacpp"    # llamacpp 目录
OUTPUT_DIR="${CONVERT_DIR}/gguf"    # 输出目录
PYTHON="/path/to/python"            # Python 路径
```

### 3. 执行 INT4 量化

转换完成后，使用 `llama-quantize` 工具对 F16 精度的 GGUF 模型进行 INT4 量化。

```bash
./llama-quantize ./tools/omni/convert/gguf/Llm-8.2B-F16.gguf ./tools/omni/convert/gguf/Llm-8.2B-Q4_K_M.gguf Q4_K_M
```
