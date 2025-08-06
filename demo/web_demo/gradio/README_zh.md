# Web Demo 服务器配置指南

为 MiniCPM-V 4.0 提供 Web 界面演示服务，支持图像和视频的多模态对话。Demo 分为[服务端](./server/)和[客户端](./client/)两个部分。

📖 [English Version](./README.md)

## 部署步骤

### 服务端

```bash
cd server
conda create -n gradio-server python=3.10
conda activate gradio-server
pip install -r requirements.txt
python gradio_server.py
```

**自定义参数:**

```bash
# 指定服务端口、日志目录、模型路径和类型
python gradio_server.py --port=39240 --log_dir=logs_v4 --model_path=/path/to/model --model_type=minicpmv4
```

### 客户端

```bash
cd client
conda create -n gradio-client python=3.10
conda activate gradio-client
pip install -r requirements.txt
python gradio_client_minicpmv4.py
```

**自定义参数:**

```bash
# 指定前端端口和后端服务地址
python gradio_client_minicpmv4.py --port=9090 --server=http://localhost:39240/api
```

## 访问地址

默认配置下，服务启动完成后，在浏览器中访问 http://localhost:8889 可以看到 web demo 页面

![demo](./assets/demo.png)
