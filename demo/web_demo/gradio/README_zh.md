# MiniCPM-o 4.5 Web Demo

为 MiniCPM-o 4.5 提供 Web 界面演示服务，支持图片和视频的多模态对话。演示由两部分组成：[服务端](./server/) 和 [客户端](./client/)。

📖 [English Version](./README_o45.md)

## 主要特性

- **多模态输入**：支持图片和视频
- **流式输出**：实时流式响应
- **思考模式**：显示模型的推理过程（`<think>` 标签）
- **显存优化**：仅加载视觉和语言模块，禁用音频/TTS以节省显存

## 部署步骤

### 服务端

```bash
cd server
conda create -n gradio-server python=3.10
conda activate gradio-server
pip install -r requirements.txt
python gradio_server.py
```

**自定义参数：**

```bash
# 指定服务端口、日志目录、模型路径和模型类型 (MiniCPM-o 4.5)
# 如果显存有限，可以使用 INT4 量化模型
python gradio_server.py --port=9999 --log_dir=logs_o45 --model_path=openbmb/MiniCPM-o-4_5 --model_type=minicpmo4_5
```

### 客户端

```bash
cd client
conda create -n gradio-client python=3.10
conda activate gradio-client
pip install -r requirements.txt
python gradio_client_minicpmo4_5.py
```

**自定义参数：**

```bash
# 指定前端端口和后端服务地址 (MiniCPM-o 4.5)
python gradio_client_minicpmo4_5.py --port=8889 --server=http://localhost:9999/api
```

## 访问

默认情况下，服务启动后，可以通过浏览器访问 http://localhost:8889 来使用 Web Demo。

## UI 功能

### 解码类型
- **Sampling**：默认模式，支持实时流式输出
- **Beam Search**：输出质量更高但不支持流式输出

### 思考模式
启用后可以看到模型的推理过程。思考内容会以视觉区分的方式显示在单独的区域。

### 流式模式
启用后可以实时逐字符输出。仅在 Sampling 模式下可用。

![demo](./assets/demo.png)
