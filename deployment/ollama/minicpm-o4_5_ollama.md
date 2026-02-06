# MiniCPM-o 4.5 - Ollama

## 1. Install Ollama

*   **macOS**: Download from [https://ollama.com/download/Ollama.dmg](https://ollama.com/download/Ollama.dmg).

*   **Windows**: Download from [https://ollama.com/download/OllamaSetup.exe](https://ollama.com/download/OllamaSetup.exe).

*   **Linux**: `curl -fsSL https://ollama.com/install.sh | sh`, or refer to the guide from [ollama](https://github.com/ollama/ollama/blob/main/docs/linux.md).

*   **Docker**: The official [Ollama Docker image](https://hub.docker.com/r/ollama/ollama) `ollama/ollama` is available on Docker Hub.

### Build Ollama locally

Environment requirements:

- [go](https://go.dev/doc/install) version 1.22 or above
- cmake version 3.24 or above
- C/C++ Compiler e.g. Clang on macOS, [TDM-GCC](https://github.com/jmeubank/tdm-gcc/releases) (Windows amd64) or [llvm-mingw](https://github.com/mstorsjo/llvm-mingw) (Windows arm64), GCC/Clang on Linux.

Clone OpenBMB Ollama Fork:

```sh
git clone https://github.com/tc-mb/ollama.git
cd ollama
git checkout MIniCPM-V
```

Then build and run Ollama from the root directory of the repository:

```sh
go build .
./ollama serve
```

## 2. Quick Start

The MiniCPM-o 4.5 model can be used directly:

```shell
./ollama run openbmb/minicpm-o4.5
```

### Command Line
Separate the input prompt and the image path with space.
```
What is in the picture? xx.jpg
```
### API
```python
with open(image_path, 'rb') as image_file:
    # Convert the image file to a base64 encoded string
    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    data = {
    "model": "minicpm-o4.5",
    "prompt": query,
    "stream": False,
    "images": [encoded_string] # The 'images' list can hold multiple base64-encoded images.
    }

    # Set request URL
    url = "http://localhost:11434/api/generate"
    response = requests.post(url, json=data)

    return response
```

## 3. Customize model

**If the method above fails, please refer to the following guide.**

### Download GGUF Model

*   HuggingFace: https://huggingface.co/openbmb/MiniCPM-o-4_5-gguf
*   ModelScope: https://modelscope.cn/models/OpenBMB/MiniCPM-o-4_5-gguf

### Create a ModelFile

Create and edit a ModelFile:

```sh
vim minicpmv4.5.Modelfile
```

The content of the Modelfile should be as follows:

```plaintext
FROM ./MiniCPM-o-4_5/model/MiniCPM-o-4_5-Q4_K_M.gguf
FROM ./MiniCPM-o-4_5/MiniCPM-o-4_5-vision-F16.gguf

TEMPLATE """{{- if .Messages }}{{- range $i, $_ := .Messages }}{{- $last := eq (len (slice $.Messages $i)) 1 -}}<|im_start|>{{ .Role }}{{ .Content }}{{- if $last }}{{- if (ne .Role "assistant") }}<|im_end|><|im_start|>assistant{{ end }}{{- else }}<|im_end|>{{ end }}{{- end }}{{- else }}{{- if .System }}<|im_start|>system{{ .System }}<|im_end|>{{ end }}{{ if .Prompt }}<|im_start|>user{{ .Prompt }}<|im_end|>{{ end }}<|im_start|>assistant{{ end }}{{ .Response }}{{ if .Response }}<|im_end|>{{ end }}"""

SYSTEM """You are a helpful assistant."""

PARAMETER top_p 0.8
PARAMETER num_ctx 4096
PARAMETER stop ["<|im_start|>","<|im_end|>"]
PARAMETER temperature 0.7
```
Parameter Descriptions:

| first from | second from | num_ctx |
|-----|-----|-----|
| Your language GGUF model path | Your vision GGUF model path | Max Model length |

### Create Ollama Model
```bash
./ollama create minicpm-o4.5 -f minicpmv4.5.Modelfile
```

### Run
In a new terminal window, run the model instance:
```bash
./ollama run minicpm-o4.5
```

### Input Prompt
Enter the prompt and the image path, separated by a space.
```bash
What is in the picture? xx.jpg
```
