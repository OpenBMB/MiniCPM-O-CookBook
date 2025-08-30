# Web Demo Server Configuration Guide

Provides web interface demonstration service for MiniCPM-V 4.5 (compatible with 4.0), supporting multimodal conversations with images and videos. The demo consists of two parts: [server](./server/) and [client](./client/).

📖 [中文版本](./README_zh.md)

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
# Specify server port, log directory, model path and model type (MiniCPM-V 4.5)
# If VRAM is limited, set /path/to/model to an INT4-quantized model; ensure required dependencies are installed.
python gradio_server.py --port=9999 --log_dir=logs_v4_5 --model_path=/path/to/model --model_type=minicpmv4_5
```

### Client

```bash
cd client
conda create -n gradio-client python=3.10
conda activate gradio-client
pip install -r requirements.txt
python gradio_client_minicpmv4_5.py
```

**Custom Parameters:**

```bash
# Specify frontend port and backend service address (MiniCPM-V 4.5)
python gradio_client_minicpmv4_5.py --port=8889 --server=http://localhost:9999/api
```

## Access

By default, after the services are started, you can access the web demo by visiting http://localhost:8889 in your browser.

![demo](./assets/demo.png)
