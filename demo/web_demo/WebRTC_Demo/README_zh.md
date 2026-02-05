# WebRTC 实时视频交互演示

基于 WebRTC 实现的全双工实时视频交互方案，支持流式输入输出，具有高响应、低延迟的特性。

📖 [English Version](./README.md) | [返回 Demo](../../)

## 概述

本演示采用 WebRTC 技术实现了**全双工实时视频交互**方案。该方案填补了目前开源社区中**流式双工对话方案**的技术空白，为实时多模态交互提供了完整的解决方案。

## 核心特性

### 🔄 全双工通信
- 支持音视频双向同时传输
- 自然流畅的对话体验，无需等待轮次切换

### ⚡ 高响应低延迟
- 流式输入输出，实现实时交互
- 端到端延迟优化
- 对话过程中即时反馈

### 🚀 原生支持 llamacpp-omni
- 无缝集成 [llamacpp-omni](https://github.com/OpenBMB/llama.cpp/tree/minicpm-omni) 作为推理后端
- 快速部署，简单配置
- 高效的资源利用

### 🎯 快速体验 MiniCPM-o 4.5
- 快速体验 MiniCPM-o 4.5 的完整能力
- 实时多模态理解与生成
- 语音与视频交互一体化

## 技术亮点

- **WebRTC 协议**：业界标准的实时通信协议
- **流式架构**：连续数据流，交互流畅
- **双工设计**：填补开源社区流式双工对话方案的空白

## 前置条件

### 1. 安装 Docker Desktop (macOS)

```bash
# 使用 Homebrew 安装
brew install --cask docker

# 或从官网下载：https://www.docker.com/products/docker-desktop

# 验证安装
docker --version
```

### 2. 编译 llamacpp-omni 推理服务

```bash
# 克隆并进入项目目录
cd /path/to/llama.cpp-omni

# 编译（macOS 默认启用 Metal 加速）
cmake -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build --target llama-server -j

# 验证编译结果
ls -la build/bin/llama-server
```

### 3. 准备 GGUF 模型文件

下载并按以下结构组织模型文件：

```
<MODEL_DIR>/
├── MiniCPM-o-4_5-Q4_K_M.gguf        # LLM 主模型 (~5GB)
├── audio/                            # 音频编码器
│   └── MiniCPM-o-4_5-audio-F16.gguf
├── vision/                           # 视觉编码器
│   └── MiniCPM-o-4_5-vision-F16.gguf
├── tts/                              # TTS 模型
│   ├── MiniCPM-o-4_5-tts-F16.gguf
│   └── MiniCPM-o-4_5-projector-F16.gguf
└── token2wav-gguf/                   # Token2Wav 模型
    ├── encoder.gguf
    ├── flow_matching.gguf
    ├── flow_extra.gguf
    ├── hifigan2.gguf
    └── prompt_cache.gguf
```

## 快速开始

我们提供了预构建的 Docker 镜像，方便快速部署和体验。Docker 镜像包含了所有必要的依赖和配置。

### macOS (Apple Silicon)

**设备要求**：Apple Silicon Mac（M1/M2/M3/M4），**推荐使用 M4** 以获得最佳性能。

下载适用于 macOS 的 Docker 镜像：

📦 [下载 Docker 镜像 (macOS)](https://drive.google.com/file/d/1vOi2T_l-MED7-q7fW-G1GHiHoDDcObxJ/view?usp=sharing)

### 部署步骤

#### 第一步：解压并加载 Docker 镜像

```bash
# 解压压缩包
unzip omni_docker.zip
cd omni_docker

# 加载 Docker 镜像
docker load -i o45-frontend.tar
docker load -i omini_backend_code/omni_backend.tar
```

#### 第二步：一键部署（推荐）

```bash
# 运行部署脚本，指定必要路径
./deploy_all.sh \
    --cpp-dir /path/to/llama.cpp-omni \
    --model-dir /path/to/gguf

# 使用双工模式
./deploy_all.sh \
    --cpp-dir /path/to/llama.cpp-omni \
    --model-dir /path/to/gguf \
    --duplex
```

脚本自动完成以下任务：
- 检查 Docker 环境
- 自动更新 LiveKit 配置中的本机 IP
- 启动 Docker 服务（前端、后端、LiveKit、Redis）
- 安装 Python 依赖
- 启动 C++ 推理服务
- 注册推理服务到后端

#### 第三步：访问 Web 界面

```bash
# 在浏览器中打开前端
open http://localhost:3000
```

### 服务端口说明

| 服务 | 端口 | 说明 |
|------|------|------|
| 前端 | 3000 | Web UI |
| 后端 | 8021 | 后端 API |
| LiveKit | 7880 | 实时通信 |
| 推理服务 | 9060 | Python HTTP API |

> 更多平台支持（Linux、Windows）即将推出。

## 即将开源

> 🚧 **我们正在整理和完善代码，完整源代码将在未来几天内开源，敬请期待！**

## 相关资源

- [MiniCPM-o 4.5 模型](https://huggingface.co/openbmb/MiniCPM-o-4_5)
- [llamacpp-omni 推理后端](https://github.com/OpenBMB/llama.cpp/tree/minicpm-omni)
