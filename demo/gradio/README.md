# Web Demo Server Configuration Guide

Provides web interface demonstration service for MiniCPM-V 4.0, supporting multimodal conversations with images and videos. The demo consists of two parts: [server](./server/) and [client](./client/).

📖 [中文版本](./README_zh.md)

## Deployment Steps

### Server

```bash
cd server
conda create -n v4-server python=3.10
conda activate v4-server
pip install -r requirements.txt
MODEL_TOKEN='openbmb/MiniCPM-V-4' python main.py
```

**Custom Parameters:**

```bash
# Specify model path, port, and log directory
MODEL_TOKEN='/path/to/model' python main.py --port=39240 --log_dir=logs_v4
```

### Client

```bash
cd client
conda create -n v4-client python=3.10
conda activate v4-client
pip install -r requirements.txt
python web_demo_v4.py
```

**Custom Parameters:**

```bash
# Specify frontend port and backend service address
python web_demo_v4.py --port=9090 --server=http://localhost:39240/api
```

## Access

By default, after the services are started, you can access the web demo by visiting http://localhost:8889 in your browser.

![demo](./assets/demo.png)
