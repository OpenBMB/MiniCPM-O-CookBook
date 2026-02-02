# MiniCPM-o 4.5 - llama.cpp

## 1. 编译安装 llama.cpp

克隆 llama.cpp 代码仓库: 
```bash
git clone https://github.com/ggml-org/llama.cpp.git
cd llama.cpp
```

使用 `CMake` 构建 llama.cpp: 
https://github.com/ggerganov/llama.cpp/blob/master/docs/build.md

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
## 2. 获取模型 GGUF 权重

### 方法一: 下载官方 GGUF 文件

*   HuggingFace: https://huggingface.co/openbmb/MiniCPM-o-4_5-gguf
*   魔搭社区: https://modelscope.cn/models/OpenBMB/MiniCPM-o-4_5-gguf

从仓库中下载语言模型文件（如: `ggml-model-Q4_K_M.gguf`）与视觉模型文件（`mmproj-model-f16.gguf`）

### 方法二: 从 Pytorch 模型转换

下载 MiniCPM-o-4_5 PyTorch 模型到 "MiniCPM-o-4_5" 文件夹:
*   HuggingFace: https://huggingface.co/openbmb/MiniCPM-o-4_5
*   魔搭社区: https://modelscope.cn/models/OpenBMB/MiniCPM-o-4_5

将 PyTorch 模型转换为 GGUF 格式:

```bash
bash ./tools/omni/convert/run_convert.sh

# 需要修改脚本中的路径：
MODEL_DIR="/path/to/MiniCPM-o-4_5"  # 源模型
LLAMACPP_DIR="/path/to/llamacpp"    # llamacpp 目录
OUTPUT_DIR="${CONVERT_DIR}/gguf"    # 输出目录
PYTHON="/path/to/python"            # Python 路径
```

## 3. 模型推理

```bash
cd build/bin/

# 运行 f16 版本
./llama-omni-cli -m /path/to/Llm-8.2B-F16.gguf --omni-cli-test /path/to/test_data

# 运行 int8 量化版本
./llama-omni-cli -m /path/to/Llm-8.2B-Q8_0.gguf --omni-cli-test /path/to/test_data

# 运行 int4 量化版本
./llama-omni-cli -m /path/to/Llm-8.2B-Q4_K_M.gguf --omni-cli-test /path/to/test_data
```

**命令行参数解析:**

| 参数 | `-m, --model` | `--omni-cli-test` |
| :--- | :--- | :--- |
| 含义 | 语言模型路径 | 测试数据路径 |
