# WebRTC Real-Time Video Interaction Demo

A full-duplex real-time video interaction solution based on WebRTC, enabling seamless streaming input/output with high responsiveness and low latency.

📖 [中文版本](./README_zh.md) | [Back to Demo](../../)

## Overview

This demo implements a **full-duplex real-time video interaction** solution using WebRTC technology. It fills a significant gap in the open-source community by providing a **streaming duplex conversation** capability that was previously unavailable.

## Key Features

### 🔄 Full-Duplex Communication
- Simultaneous bidirectional audio and video streaming
- Natural conversation flow without turn-taking delays

### ⚡ High Responsiveness & Low Latency
- Streaming input/output for real-time interactions
- Optimized for minimal end-to-end latency
- Immediate feedback during conversations

### 🚀 Native llamacpp-omni Support
- Seamlessly integrates with [llamacpp-omni](https://github.com/OpenBMB/llama.cpp/tree/minicpm-omni) as the inference backend
- Quick deployment and easy setup
- Efficient resource utilization

### 🎯 MiniCPM-o 4.5 Experience
- Rapidly experience the full capabilities of MiniCPM-o 4.5
- Real-time multimodal understanding and generation
- Voice and video interaction in one unified interface

## Technical Highlights

- **WebRTC Protocol**: Industry-standard real-time communication
- **Streaming Architecture**: Continuous data flow for smooth interactions
- **Duplex Design**: Fills the gap in open-source streaming duplex conversation solutions

## Prerequisites

### 1. Install Docker Desktop (macOS)

```bash
# Install via Homebrew
brew install --cask docker

# Or download from: https://www.docker.com/products/docker-desktop

# Verify installation
docker --version
```

### 2. Build llamacpp-omni Inference Service

```bash
# Clone and enter the project directory
cd /path/to/llama.cpp-omni

# Build (Metal acceleration enabled by default on macOS)
cmake -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build --target llama-server -j

# Verify build
ls -la build/bin/llama-server
```

### 3. Prepare GGUF Model Files

Download and organize the model files with the following structure:

```
<MODEL_DIR>/
├── MiniCPM-o-4_5-Q4_K_M.gguf        # LLM main model (~5GB)
├── audio/                            # Audio encoder
│   └── MiniCPM-o-4_5-audio-F16.gguf
├── vision/                           # Vision encoder
│   └── MiniCPM-o-4_5-vision-F16.gguf
├── tts/                              # TTS model
│   ├── MiniCPM-o-4_5-tts-F16.gguf
│   └── MiniCPM-o-4_5-projector-F16.gguf
└── token2wav-gguf/                   # Token2Wav model
    ├── encoder.gguf
    ├── flow_matching.gguf
    ├── flow_extra.gguf
    ├── hifigan2.gguf
    └── prompt_cache.gguf
```

## Quick Start

We provide a pre-built Docker image for quick deployment and experience. The Docker image includes all necessary dependencies and configurations.

### macOS (Apple Silicon)

Download the Docker image for macOS with Apple Silicon (M1/M2/M3/M4):

📦 [Download Docker Image (macOS)](https://drive.google.com/file/d/1vOi2T_l-MED7-q7fW-G1GHiHoDDcObxJ/view?usp=sharing)

### Deployment Steps

#### Step 1: Extract and Load Docker Images

```bash
# Extract the package
unzip omni_docker.zip
cd omni_docker

# Load Docker images
docker load -i o45-frontend.tar
docker load -i omini_backend_code/omni_backend.tar
```

#### Step 2: One-Click Deployment (Recommended)

```bash
# Run the deployment script with required paths
./deploy_all.sh \
    --cpp-dir /path/to/llama.cpp-omni \
    --model-dir /path/to/gguf

# For duplex mode
./deploy_all.sh \
    --cpp-dir /path/to/llama.cpp-omni \
    --model-dir /path/to/gguf \
    --duplex
```

The script automatically:
- Checks Docker environment
- Updates LiveKit configuration with local IP
- Starts Docker services (frontend, backend, LiveKit, Redis)
- Installs Python dependencies
- Starts C++ inference service
- Registers inference service to backend

#### Step 3: Access the Web Interface

```bash
# Open the frontend in browser
open http://localhost:3000
```

### Service Ports

| Service | Port | Description |
|---------|------|-------------|
| Frontend | 3000 | Web UI |
| Backend | 8021 | Backend API |
| LiveKit | 7880 | Real-time communication |
| Inference | 9060 | Python HTTP API |

> More platform support (Linux, Windows) coming soon.

## Coming Soon

> 🚧 **We are currently organizing and refining the code. The complete source code will be open-sourced within the next few days. Stay tuned!**

## Related Resources

- [MiniCPM-o 4.5 Model](https://huggingface.co/openbmb/MiniCPM-o-4_5)
- [llamacpp-omni Backend](https://github.com/OpenBMB/llama.cpp/tree/minicpm-omni)
