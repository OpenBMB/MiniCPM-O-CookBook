# Web Demo for MiniCPM-o 4.5

Provides web interface demonstration service for MiniCPM-o 4.5, supporting multimodal conversations with images and videos. The demo consists of two parts: [server](./server/) and [client](./client/).

📖 [中文版本](./README_o45_zh.md)

## Key Features

- **Multi-modal Input**: Support images and videos
- **Streaming Output**: Real-time response streaming
- **Thinking Mode**: Display model's reasoning process with `<think>` tags
- **Memory Optimization**: Only loads vision and LLM modules, disables audio/TTS to save VRAM

## Deployment Steps

### Server

```bash
cd server
conda create -n gradio-server python=3.10
conda activate gradio-server
pip install -r requirements.txt
python gradio_server.py
```

**Custom Parameters:**

```bash
# Specify server port, log directory, model path and model type (MiniCPM-o 4.5)
# If VRAM is limited, you can use INT4-quantized model
python gradio_server.py --port=9999 --log_dir=logs_o45 --model_path=openbmb/MiniCPM-o-2_6 --model_type=minicpmo4_5
```

### Client

```bash
cd client
conda create -n gradio-client python=3.10
conda activate gradio-client
pip install -r requirements.txt
python gradio_client_minicpmo4_5.py
```

**Custom Parameters:**

```bash
# Specify frontend port and backend service address (MiniCPM-o 4.5)
python gradio_client_minicpmo4_5.py --port=8889 --server=http://localhost:9999/api
```

## Access

By default, after the services are started, you can access the web demo by visiting http://localhost:8889 in your browser.

## UI Features

### Decode Type
- **Sampling**: Default mode with real-time streaming support
- **Beam Search**: Higher quality output but no streaming support

### Thinking Mode
Enable to see the model's reasoning process. The thinking content is displayed in a separate section with visual distinction.

### Streaming Mode
Enable real-time character-by-character output. Only available in Sampling mode.

![demo](./assets/demo.png)
