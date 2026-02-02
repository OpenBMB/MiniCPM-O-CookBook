# MiniCPM-o 4.5 - llama.cpp

## 1. Build llama.cpp

Clone the llama.cpp repository:
```bash
git clone https://github.com/ggml-org/llama.cpp.git
cd llama.cpp
```

Build llama.cpp using `CMake`: https://github.com/ggerganov/llama.cpp/blob/master/docs/build.md

**CPU/Metal:**
```bash
cmake -B build
cmake --build build --config Release
```

**CUDA:**
```bash
cmake -B build -DGGML_CUDA=ON
cmake --build build --config Release
```
## 2. GGUF files

### Option 1: Download official GGUF files

Download converted language model file (e.g., `ggml-model-Q4_K_M.gguf`) and vision model file (`mmproj-model-f16.gguf`) from:
*   HuggingFace: https://huggingface.co/openbmb/MiniCPM-o-4_5-gguf
*   ModelScope: https://modelscope.cn/models/OpenBMB/MiniCPM-o-4_5-gguf

### Option 2: Convert from PyTorch model

Download the MiniCPM-o-4_5 PyTorch model to "MiniCPM-o-4_5" folder:
*   HuggingFace: https://huggingface.co/openbmb/MiniCPM-o-4_5
*   ModelScope: https://modelscope.cn/models/OpenBMB/MiniCPM-o-4_5

Convert the PyTorch model to GGUF:

```bash
bash ./tools/omni/convert/run_convert.sh

# You need to modify the paths in the script:
MODEL_DIR="/path/to/MiniCPM-o-4_5"  # Source model
LLAMACPP_DIR="/path/to/llamacpp"    # llamacpp directory
OUTPUT_DIR="${CONVERT_DIR}/gguf"    # Output directory
PYTHON="/path/to/python"            # Python path
```

## 3. Model Inference

```bash
cd build/bin/

# run f16 version
./llama-omni-cli -m /path/to/Llm-8.2B-F16.gguf --omni-cli-test /path/to/test_data

# run int8 quantized version
./llama-omni-cli -m /path/to/Llm-8.2B-Q8_0.gguf --omni-cli-test /path/to/test_data

# run int4 quantized version
./llama-omni-cli -m /path/to/Llm-8.2B-Q4_K_M.gguf --omni-cli-test /path/to/test_data
```

**Argument Reference:**

| Argument | `-m, --model` | `--omni-cli-test` |
| :--- | :--- | :--- |
| Description | Path to the language model | Path to the test data |
