# Omni Stream

## Overview

The MiniCPM-o Omni Stream demo provides a real-time conversational AI experience with multimodal capabilities. It supports streaming audio input/output, voice activity detection (VAD), voice cloning, and multimodal interactions.

## Key Features

### Real-time Streaming
- **Streaming Audio Processing**: Process audio input in real-time chunks
- **Low-latency Response**: Optimized for real-time conversation scenarios
- **Concurrent Processing**: Handle multiple audio streams with session management

### Voice Activity Detection (VAD)
- **Silero VAD Integration**: Automatic speech detection using pre-trained VAD models
- **Configurable Thresholds**: Customizable silence/speech detection parameters
- **Smart Segmentation**: Automatic audio segmentation based on speech patterns

### Voice Cloning & TTS
- **Reference Audio Support**: Clone voice characteristics from reference audio samples
- **Multiple Voice Options**: Built-in male, female, and default voice presets
- **Custom Audio Upload**: Upload your own reference audio for voice cloning

### Multimodal Support
- **Audio + Image Input**: Process both audio and visual information simultaneously
- **Text + Audio Output**: Generate both speech and text responses
- **High-definition Video**: Support for HD video processing with advanced slicing

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Client App    │────│  FastAPI Server │────│ MiniCPM-o Model │
│                 │    │                 │    │                 │
│ • Audio Stream  │    │ • VAD Processing│    │ • Multimodal    │
│ • WebSocket/REST│    │ • Session Mgmt  │    │ • TTS/Voice     │
│ • UI Interface  │    │ • Audio Buffer  │    │ • Streaming Gen │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Local WebUI Demo
  
You can easily build your own local WebUI demo using the following commands.

Please ensure that `transformers==4.44.2` is installed, as other versions may have compatibility issues.

If you are using an older version of PyTorch, you might encounter this issue `"weight_norm_fwd_first_dim_kernel" not implemented for 'BFloat16'`, Please add `self.minicpmo_model.tts.float()` during the model initialization.

**For real-time voice/video call demo:**
1. launch model server:
```shell
pip install -r demo/web_demo/omni_stream/requirements_o2.6.txt

python demo/web_demo/omni_stream/omni_web_server/model_server.py
```

2. launch web server:

```shell
# Make sure Node and PNPM is installed.
sudo apt-get update
sudo apt-get install nodejs npm
npm install -g pnpm


cd demo/web_demo/omni_stream/omni_web_client
# create ssl cert for https, https is required to request camera and microphone permissions.
bash ./make_ssl_cert.sh  # output key.pem and cert.pem

pnpm install  # install requirements
pnpm run dev  # start server
```
Open `https://localhost:8088/` in browser and enjoy the real-time voice/video call.