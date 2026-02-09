# Omni Stream

## Overview

The MiniCPM-o 4.5 Omni Stream demo provides a real-time conversational AI experience with multimodal capabilities. It supports full-duplex streaming audio/video input/output, voice activity detection (VAD), voice cloning, and multimodal interactions.

## Key Features

### Full-Duplex Real-time Streaming
- **Streaming Audio/Video Processing**: Process audio and video input in real-time
- **Low-latency Response**: Optimized for real-time conversation scenarios
- **Full-Duplex Communication**: Simultaneous bidirectional audio streaming

### Voice Activity Detection (VAD)
- **Silero VAD Integration**: Automatic speech detection using pre-trained VAD models
- **Configurable Thresholds**: Customizable silence/speech detection parameters
- **Smart Segmentation**: Automatic audio segmentation based on speech patterns

### Voice Cloning & TTS
- **Reference Audio Support**: Clone voice characteristics from reference audio samples
- **Multiple Voice Options**: Built-in male, female, and default voice presets
- **Custom Audio Upload**: Upload your own reference audio for voice cloning

### Multimodal Support
- **Audio + Video Input**: Process both audio and visual information simultaneously
- **Text + Audio Output**: Generate both speech and text responses
- **High-definition Video**: Support for HD video processing

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Client App    │────│  WebRTC Server  │────│ llamacpp-omni   │
│                 │    │                 │    │                 │
│ • Audio/Video   │    │ • LiveKit       │    │ • Multimodal    │
│ • WebRTC        │    │ • Session Mgmt  │    │ • TTS/Voice     │
│ • UI Interface  │    │ • Real-time     │    │ • Full-Duplex   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## WebRTC Demo

For MiniCPM-o 4.5, we provide a WebRTC-based full-duplex real-time video interaction demo.

### Prerequisites

1. **Install Docker Desktop** (macOS)

```bash
# Install via Homebrew
brew install --cask docker

# Or download from: https://www.docker.com/products/docker-desktop

# Verify installation
docker --version
```

2. **Build llamacpp-omni Inference Service**

```bash
# Clone and enter the project directory
git clone https://github.com/tc-mb/llama.cpp-omni.git
cd llama.cpp-omni

# Build (Metal acceleration enabled by default on macOS)
cmake -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build --target llama-server -j

# Verify build
ls -la build/bin/llama-server
```

3. **Prepare GGUF Model Files**

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

### Quick Start

We provide a pre-built Docker image for quick deployment and experience. The Docker image includes all necessary dependencies and configurations.

#### macOS (Apple Silicon)

**Requirements**: Apple Silicon Mac (M1/M2/M3/M4), **M4 recommended** for optimal performance.

Download the Docker image for macOS:

📦 [Download Docker Image (macOS)](https://drive.google.com/file/d/1i7HrGBZE3E-6lsrHjQgaEQK0Qxdi6tSN/view?usp=sharing)

#### Deployment Steps

**Step 1: Extract and Load Docker Images**

```bash
# Extract the package
unzip omni_docker.zip
cd omni_docker

# Open Docker
open -a Docker

# Load Docker images
docker load -i o45-frontend.tar
docker load -i omini_backend_code/omni_backend.tar
```

**Step 2: Install Python Dependencies**

```bash
# Install required Python dependencies for the inference service
pip install -r cpp_server/requirements.txt
```

**Step 3: One-Click Deployment (Recommended)**

> **Note**: The `deploy_all.sh` script is located in the `omni_docker` directory.

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

**Step 4: Access the Web Interface**

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

## Technical Highlights

- **WebRTC Protocol**: Industry-standard real-time communication
- **Full-Duplex Architecture**: Simultaneous bidirectional streaming
- **Native llamacpp-omni Support**: Seamlessly integrates with [llamacpp-omni](https://github.com/tc-mb/llama.cpp-omni) as the inference backend

## Related Resources

- [MiniCPM-o 4.5 Model](https://huggingface.co/openbmb/MiniCPM-o-4_5)
- [llamacpp-omni Backend](https://github.com/OpenBMB/llama.cpp/tree/minicpm-omni)
- [WebRTC Demo README](../../demo/web_demo/WebRTC_Demo/README.md)
