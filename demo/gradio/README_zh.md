# Web Demo 服务器配置指南

为 MiniCPM-V 4.0 提供 Web 界面演示服务，支持图像和视频的多模态对话。Demo 分为[服务端](./server/)和[客户端](./client/)两个部分。

📖 [English Version](./README.md)

## 部署步骤

### 服务端

```bash
cd server
conda create -n v4-server python=3.10
conda activate v4-server
pip install -r requirements.txt
MODEL_TOKEN='openbmb/MiniCPM-V-4' python main.py
```

**自定义参数:**

```bash
# 指定模型路径、端口和日志目录
MODEL_TOKEN='/path/to/model' python main.py --port=39240 --log_dir=logs_v4
```

### 客户端

```bash
cd client
conda create -n v4-client python=3.10
conda activate v4-client
pip install -r requirements.txt
python web_demo_v4.py
```

**自定义参数:**

```bash
# 指定前端端口和后端服务地址
python web_demo_v4.py --port=9090 --server=http://localhost:39240/api
```

## 访问地址

默认配置下，服务启动完成后，在浏览器中访问 http://localhost:8889 可以看到 web demo 页面

![demo](./assets/demo.png)
