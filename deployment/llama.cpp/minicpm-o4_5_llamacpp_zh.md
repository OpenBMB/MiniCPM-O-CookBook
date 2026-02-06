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

从仓库中下载语言模型文件（如: `MiniCPM-o-4_5-Q4_K_M.gguf`）与视觉模型文件（`MiniCPM-o-4_5-vision-F16.gguf`）

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
./llama-mtmd-cli -m ../MiniCPM-o-4_5/model/Model-8.2B-F16.gguf --mmproj ../MiniCPM-o-4_5/MiniCPM-o-4_5-vision-F16.gguf -c 4096 --temp 0.7 --top-p 0.8 --top-k 100 --repeat-penalty 1.05 --image xx.jpg -p "What is in the image?"

# 运行 int4 量化版本
./llama-mtmd-cli -m ../MiniCPM-o-4_5/model/MiniCPM-o-4_5-Q4_K_M.gguf --mmproj ../MiniCPM-o-4_5/MiniCPM-o-4_5-vision-F16.gguf -c 4096 --temp 0.7 --top-p 0.8 --top-k 100 --repeat-penalty 1.05 --image xx.jpg -p "What is in the image?"

# 或以交互模式运行
./llama-mtmd-cli -m ../MiniCPM-o-4_5/model/MiniCPM-o-4_5-Q4_K_M.gguf --mmproj ../MiniCPM-o-4_5/MiniCPM-o-4_5-vision-F16.gguf -c 4096 --temp 0.7 --top-p 0.8 --top-k 100 --repeat-penalty 1.05 --image xx.jpg -i

# 或以思考模式运行(思考输出的token无限制)
./llama-mtmd-cli -m ../MiniCPM-o-4_5/model/MiniCPM-o-4_5-Q4_K_M.gguf --mmproj ../MiniCPM-o-4_5/MiniCPM-o-4_5-vision-F16.gguf -c 4096 --temp 0.7 --top-p 0.8 --top-k 100 --repeat-penalty 1.05 --image xx.jpg --jinja --reasoning-budget -1 -p "what is it?"

# 或以禁止思考模式运行
./llama-mtmd-cli -m ../MiniCPM-o-4_5/model/MiniCPM-o-4_5-Q4_K_M.gguf --mmproj ../MiniCPM-o-4_5/MiniCPM-o-4_5-vision-F16.gguf -c 4096 --temp 0.7 --top-p 0.8 --top-k 100 --repeat-penalty 1.05 --image xx.jpg --jinja --reasoning-budget 0 -p "what is it?"
```

**命令行参数解析:**

| 参数 | `-m, --model` | `--mmproj` | `--image` | `-p, --prompt` | `-c, --ctx-size` | `--reasoning-budget` | `--jinja` |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 含义 | 语言模型路径 | 视觉模型路径 | 输入图片路径 | 提示词 | 输入上下文最大长度 | 最大思考输出token数量 | 使用jinja模板 |
