# Ollama

:::{Note}
We've submitted a PR for MiniCPM-V 4.5 to the Ollama repo, and it's currently under review for merging. In the meantime, you can use our code via [this link](https://github.com/tc-mb/ollama/tree/Support-MiniCPM-V-4.5)..
:::

[Ollama](https://ollama.com/) helps you run LLMs locally with only a few commands. It is available at macOS, Linux, and Windows. Now, MiniCPM-V 4.5 is officially on Ollama, and you can run it with one command:

```bash
ollama run openbmb/minicpm-v4.5
```

Next, we introduce more detailed usages of Ollama for running MiniCPM-V 4.5.

## Install Ollama

*   **macOS**: Download from [https://ollama.com/download/Ollama.dmg](https://ollama.com/download/Ollama.dmg).

*   **Windows**: Download from [https://ollama.com/download/OllamaSetup.exe](https://ollama.com/download/OllamaSetup.exe).

*   **Linux**: `curl -fsSL https://ollama.com/install.sh | sh`, or refer to the guide from [ollama](https://github.com/ollama/ollama/blob/main/docs/linux.md).

*   **Docker**: The official [Ollama Docker image](https://hub.docker.com/r/ollama/ollama) `ollama/ollama` is available on Docker Hub.

## Build Ollama locally

Environment requirements:

- [go](https://go.dev/doc/install) version 1.22 or above
- cmake version 3.24 or above
- C/C++ Compiler e.g. Clang on macOS, [TDM-GCC](https://github.com/jmeubank/tdm-gcc/releases) (Windows amd64) or [llvm-mingw](https://github.com/mstorsjo/llvm-mingw) (Windows arm64), GCC/Clang on Linux.

Clone OpenBMB Ollama Fork:

```sh
git clone https://github.com/tc-mb/ollama.git
cd ollama
git checkout Support-MiniCPM-V-4.5
```

Then build and run Ollama from the root directory of the repository:

```sh
go build .
./ollama serve
```

## Quickstart

Once the Ollama service has been built and launched, the MiniCPM-V/o series models can be run using the following commands:

*   `./ollama run openbmb/minicpm-v4.5`
*   `./ollama run openbmb/minicpm-o2.6`
*   `./ollama run openbmb/minicpm-v2.6`
*   `./ollama run openbmb/minicpm-v2.5`

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
    "model": "minicpm-v4.5",
    "prompt": query,
    "stream": False,
    "images": [encoded_string] # The 'images' list can hold multiple base64-encoded images.
    }

    # Set request URL
    url = "http://localhost:11434/api/generate"
    response = requests.post(url, json=data)

    return response
```

## Run Ollama with Your GGUF Files

You can alse use Ollama with your own GGUF files of MiniCPM-V 4.5. For the first step, you need to create a file called `Modelfile`. The content of the file is shown below:

```dockerfile
FROM ./MiniCPM-V-4/model/Model-3.6B-Q4_K_M.gguf
FROM ./MiniCPM-V-4/mmproj-model-f16.gguf

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

Create Ollama Model:
```bash
./ollama create minicpm-v4.5 -f minicpmv4.5.Modelfile
```

Run your Ollama model:
In a new terminal window, run the model instance:
```bash
./ollama run minicpm-v4.5
```

Enter the prompt and the image path, separated by a space.
```
What is in the picture? xx.jpg
```
