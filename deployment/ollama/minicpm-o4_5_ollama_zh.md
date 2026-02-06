# MiniCPM-o 4.5 - Ollama

## 1. 安装 Ollama

*   **macOS**: [下载](https://ollama.com/download/Ollama.dmg)

*   **Windows**: [下载](https://ollama.com/download/OllamaSetup.exe)

*   **Linux**: `curl -fsSL https://ollama.com/install.sh | sh`, 或参照 Ollama 官方[手动安装指南](https://github.com/ollama/ollama/blob/main/docs/linux.md).

*   **Docker**: 官方的 [Ollama Docker 镜像](https://hub.docker.com/r/ollama/ollama) `ollama/ollama` 已在 Docker Hub 上提供。

### 本地构建运行 Ollama

环境需求：

- [go](https://go.dev/doc/install) version 1.22 or above
- cmake version 3.24 or above
- C/C++ Compiler e.g. Clang on macOS, [TDM-GCC](https://github.com/jmeubank/tdm-gcc/releases) (Windows amd64) or [llvm-mingw](https://github.com/mstorsjo/llvm-mingw) (Windows arm64), GCC/Clang on Linux.

获取 OpenBMB 官方 Ollama 分支：

```sh
git clone https://github.com/tc-mb/ollama.git
cd ollama
git checkout MIniCPM-V
```

在仓库根目录下编译并运行 Ollama：

```sh
go build .
./ollama serve
```

## 2. 快速使用

Ollama 可以直接使用:

```shell
./ollama run openbmb/minicpm-o4.5
```

### 命令行
用空格分割输入问题、图片路径
```
这张图片描述了什么？ xx.jpg
```
### API
```python
with open(image_path, 'rb') as image_file:
    # 将图片文件转换为 base64 编码
    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    data = {
    "model": "minicpm-o4.5",
    "prompt": query,
    "stream": False,
    "images": [encoded_string]# 列表可以放多张图，每张图用上面的方式转化为base64的格式
    }

    # 设置请求 URL
    url = "http://localhost:11434/api/generate"
    response = requests.post(url, json=data)

    return response
```

## 3. 自定义方式

**若上述方式无法运行，请参考以下教程。**

### 获取 GGUF 模型

*   HuggingFace: https://huggingface.co/openbmb/MiniCPM-o-4_5-gguf
*   魔搭社区: https://modelscope.cn/models/OpenBMB/MiniCPM-o-4_5-gguf

### 创建 ModelFile

编辑 ModelFile:

```sh
vim minicpmv4.5.Modelfile
```

ModelFile 的内容如下:

```plaintext
FROM ./MiniCPM-o-4_5/model/MiniCPM-o-4_5-Q4_K_M.gguf
FROM ./MiniCPM-o-4_5/mmproj-model-f16.gguf

TEMPLATE """{{- if .Messages }}{{- range $i, $_ := .Messages }}{{- $last := eq (len (slice $.Messages $i)) 1 -}}<|im_start|>{{ .Role }}{{ .Content }}{{- if $last }}{{- if (ne .Role "assistant") }}<|im_end|><|im_start|>assistant{{ end }}{{- else }}<|im_end|>{{ end }}{{- end }}{{- else }}{{- if .System }}<|im_start|>system{{ .System }}<|im_end|>{{ end }}{{ if .Prompt }}<|im_start|>user{{ .Prompt }}<|im_end|>{{ end }}<|im_start|>assistant{{ end }}{{ .Response }}{{ if .Response }}<|im_end|>{{ end }}"""

SYSTEM """You are a helpful assistant."""

PARAMETER top_p 0.8
PARAMETER num_ctx 4096
PARAMETER stop ["<|im_start|>","<|im_end|>"]
PARAMETER temperature 0.7
```
参数说明:

| first from | second from | num_ctx |
|-----|-----|-----|
| Your language GGUF model path | Your vision GGUF model path | Max Model length |

### 创建 Ollama 模型实例：
```bash
./ollama create minicpm-o4.5 -f minicpmv4.5.Modelfile
```

### 另起一个命令行窗口，运行 Ollama 模型实例：
```bash
./ollama run minicpm-o4.5
```

### 输入问题和图片 URL，以空格分隔
```bash
这张图片描述了什么？ xx.jpg
```
