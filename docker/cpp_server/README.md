# MiniCPM-o C++ HTTP 服务器

基于 C++ llama.cpp-omni 后端的 MiniCPM-o 语音对话服务，对外提供 HTTP API 接口。

## 支持平台

| 平台 | GPU 加速 | 状态 |
|------|----------|------|
| macOS (Apple Silicon) | Metal | ✅ 已测试 |
| Linux (NVIDIA GPU) | CUDA | ✅ 支持 |

---

## 快速开始 (macOS)

### 1. 前置要求

- macOS 14+ (Apple Silicon M1/M2/M3/M4)
- Python 3.10+
- 已编译的 llama.cpp-omni

### 2. 安装 Python 依赖

```bash
pip install fastapi uvicorn httpx librosa soundfile numpy pillow pydantic
```

### 3. 编译 llama-server

```bash
cd /path/to/llama.cpp-omni

# 配置
cmake -B build -DCMAKE_BUILD_TYPE=Release

# 编译
cmake --build build --target llama-server -j
```

### 4. 准备模型文件

模型目录结构：

```
MiniCPM-o-4_5-gguf/
├── MiniCPM-o-4_5-Q4_K_M.gguf      # LLM 模型
├── audio/
│   └── MiniCPM-o-4_5-audio-F16.gguf
├── tts/
│   ├── MiniCPM-o-4_5-tts-F16.gguf
│   └── MiniCPM-o-4_5-projector-F16.gguf
├── token2wav-gguf/
│   ├── encoder.gguf
│   ├── flow_matching.gguf
│   ├── flow_extra.gguf
│   ├── hifigan2.gguf
│   └── prompt_cache.gguf
└── vision/
    └── MiniCPM-o-4_5-vision-F16.gguf
```

### 5. 启动服务

**必须参数**：`--llamacpp-root` 和 `--model-dir`

⚠️ **推荐使用端口 9060**（避免与 Cursor IDE 端口冲突）

```bash
cd /path/to/llama.cpp-omni/tools/omni/release_cpp

# 启动服务（必须指定两个路径）
python minicpmo_cpp_http_server.py \
    --llamacpp-root /path/to/llama.cpp-omni \
    --model-dir /path/to/MiniCPM-o-4_5-gguf \
    --port 9060    # ⚠️ 推荐使用 9060

# LLM 模型会自动从 model-dir 检测（按 Q4_K_M > Q8_0 > F16 优先级）
# 也可以手动指定
python minicpmo_cpp_http_server.py \
    --llamacpp-root /path/to/llama.cpp-omni \
    --model-dir /path/to/MiniCPM-o-4_5-gguf \
    --llm-model MiniCPM-o-4_5-Q8_0.gguf \
    --port 9060
```

**启动后等待 2-3 分钟**（模型加载需要时间），看到以下日志表示启动完成：
```
MiniCPMO C++ HTTP 服务器初始化完成
Application startup complete
```

### 6. 环境变量配置

也可以通过环境变量指定必须参数：

```bash
# 设置必须参数
export LLAMACPP_ROOT=/path/to/llama.cpp-omni
export MODEL_DIR=/path/to/MiniCPM-o-4_5-gguf

# 可选：手动指定 LLM 模型（默认自动检测）
export LLM_MODEL=MiniCPM-o-4_5-Q4_K_M.gguf

# 可选：设置参考音频
export REF_AUDIO=/path/to/ref_audio.wav

# 启动（推荐端口 9060）
python minicpmo_cpp_http_server.py --port 9060
```

---

## 快速开始 (Linux + CUDA)

### 1. 编译

```bash
cd /path/to/llama.cpp-omni
cmake -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build --target llama-server -j
```

### 2. 启动

```bash
export CUDA_VISIBLE_DEVICES=0

python minicpmo_cpp_http_server.py \
    --llamacpp-root /path/to/llama.cpp-omni \
    --model-dir /path/to/MiniCPM-o-4_5-gguf \
    --port 8060
```

---

## 命令行参数

| 参数 | 必须 | 默认值 | 说明 |
|------|------|--------|------|
| `--llamacpp-root` | ✅ | - | llama.cpp-omni 根目录 |
| `--model-dir` | ✅ | - | GGUF 模型目录 |
| `--llm-model` | - | 自动检测 | LLM 模型文件名 |
| `--host` | - | 0.0.0.0 | 服务器监听地址 |
| `--port` | - | 8060 | HTTP 服务端口（⚠️ 推荐 **9060**） |
| `--gpu-devices` | - | 空 | GPU 设备（Linux CUDA） |
| `--duplex` | - | - | 启用双工模式 |
| `--simplex` | - | 默认 | 启用单工模式 |
| `--output-dir` | - | 基于端口 | 输出目录 |

**端口说明**：
- Python HTTP API 端口 = `--port` 指定的值
- 健康检查端口 = `--port` + 1
- C++ llama-server 端口 = `--port` + 10000

---

## API 接口

### 1. 健康检查

```bash
# 主端口
curl http://localhost:8060/health

# 独立健康检查端口（推理期间也可用）
curl http://localhost:8061/health
```

### 2. 初始化会话

```bash
curl -X POST http://localhost:8060/omni/init_sys_prompt \
    -H "Content-Type: application/json" \
    -d '{"media_type": "audio"}'
```

**参数**:
| 字段 | 类型 | 说明 |
|------|------|------|
| `media_type` | string | `"audio"` 或 `"omni"` |
| `duplex_mode` | bool | 是否启用双工模式 |
| `language` | string | `"zh"` 或 `"en"` |

### 3. 流式预填充

```bash
# 音频需要 base64 编码
AUDIO_BASE64=$(base64 < user_audio.wav)

curl -X POST http://localhost:8060/omni/streaming_prefill \
    -H "Content-Type: application/json" \
    -d "{\"audio\": \"${AUDIO_BASE64}\"}"
```

### 4. 流式生成

```bash
curl -X POST http://localhost:8060/omni/streaming_generate \
    -H "Accept: text/event-stream"
```

**响应** (SSE 格式):
```
data: {"chunk_idx": 0, "chunk_data": {"wav": "BASE64...", "sample_rate": 24000}}
data: {"chunk_idx": 1, "chunk_data": {"wav": "BASE64...", "sample_rate": 24000, "text": "你好"}}
data: {"done": true}
```

### 5. 停止/打断

```bash
# 停止会话
curl -X POST http://localhost:8060/omni/stop

# 打断当前轮（保留会话）
curl -X POST http://localhost:8060/omni/break
```

---

## Python 调用示例

```python
import requests
import base64
import json

SERVER_URL = "http://localhost:8060"

# 1. 初始化会话
resp = requests.post(f"{SERVER_URL}/omni/init_sys_prompt", json={
    "media_type": "audio",
    "language": "zh"
})
print("Init:", resp.json())

# 2. 发送用户音频
with open("user_question.wav", "rb") as f:
    audio_base64 = base64.b64encode(f.read()).decode()

resp = requests.post(f"{SERVER_URL}/omni/streaming_prefill", json={
    "audio": audio_base64
})
print("Prefill:", resp.json())

# 3. 获取语音响应 (流式)
resp = requests.post(
    f"{SERVER_URL}/omni/streaming_generate",
    stream=True,
    headers={"Accept": "text/event-stream"}
)

audio_chunks = []
for line in resp.iter_lines():
    if line:
        line = line.decode('utf-8')
        if line.startswith('data: '):
            data = json.loads(line[6:])
            if 'chunk_data' in data:
                wav_bytes = base64.b64decode(data['chunk_data']['wav'])
                audio_chunks.append(wav_bytes)
                text = data['chunk_data'].get('text', '')
                print(f"Chunk {data['chunk_idx']}: {len(wav_bytes)} bytes, text='{text}'")
            elif data.get('done'):
                print("Generation complete")
                break

# 4. 合并音频
import wave
with wave.open("response.wav", "wb") as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(24000)
    for chunk in audio_chunks:
        wf.writeframes(chunk)
print("Audio saved to response.wav")
```

---

## 性能参考

### macOS (Apple M4 Max, Metal)

| 指标 | Q4_K_M | Q8_0 | F16 |
|------|--------|------|-----|
| 模型内存 | ~8.5 GB | ~12 GB | ~19 GB |
| 音频首响 | ~650ms | ~700ms | ~800ms |
| Token2Wav RTF | ~0.47x | ~0.47x | ~0.47x |

### Linux (NVIDIA 4090, CUDA)

| 指标 | Q4_K_M | Q8_0 | F16 |
|------|--------|------|-----|
| 显存占用 | ~6 GB | ~9 GB | ~16 GB |
| 音频首响 | ~400ms | ~450ms | ~500ms |
| Token2Wav RTF | ~0.3x | ~0.3x | ~0.3x |

---

## 故障排查

### 1. ⚠️ 端口冲突问题（重要）

**Cursor IDE 会占用某些端口**，导致服务无法正常响应。已知被占用的端口包括：

```
8060, 8070, 8091, 8100-8109, 18060, 18088, 18090, 18100-18108
```

**解决方案**：使用不冲突的端口，推荐 **9060**：

```bash
# 推荐使用 9060 端口
python minicpmo_cpp_http_server.py \
    --llamacpp-root /path/to/llama.cpp-omni \
    --model-dir /path/to/MiniCPM-o-4_5-gguf \
    --port 9060   # 推荐！

# 检查端口是否被占用
lsof -i :9060
lsof -i :19060  # C++ 端口 = Python 端口 + 10000
```

**端口对应关系**：
| 服务 | 端口 | 说明 |
|------|------|------|
| Python HTTP API | 9060 | 主服务端口 |
| 健康检查（独立） | 9061 | 推理期间也可用 |
| C++ llama-server | 19060 | 内部服务 |

### 2. 服务无法启动

```bash
# 检查 llama-server 是否存在
ls -la $LLAMACPP_ROOT/build/bin/llama-server

# 检查模型文件
ls -la $MODEL_DIR/
```

### 3. 模型加载超时

模型加载需要 **2-3 分钟**，如果健康检查超时，增加等待时间：

```bash
# 查看启动日志
tail -f /tmp/cpp_server.log

# 等待看到以下日志才表示启动完成：
# "MiniCPMO C++ HTTP 服务器初始化完成"
# "Application startup complete"
```

### 4. 模型加载失败

检查模型目录结构是否正确，确保所有必需的 GGUF 文件存在。

### 5. macOS Metal 相关

使用标准 CMake 编译即可：

```bash
cmake -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build --target llama-server -j
```

---

## 与后端对接（Docker 部署）

### 服务注册参数

当与后端 Docker 服务对接时，服务会自动注册到后端。注册参数说明：

| 参数 | 值 | 说明 |
|------|------|------|
| `model_type` | `simplex` / `duplex` | 根据启动模式自动设置 |
| `session_type` | `release` | **固定值**，兼容模式 |
| `service_name` | `o45-cpp` | 服务标识 |

**注意**：前端请求时 `modelType` 必须与注册的 `model_type` 匹配：
- 单工模式启动 (`--simplex`) → 前端请求 `modelType: "simplex"`
- 双工模式启动 (`--duplex`) → 前端请求 `modelType: "duplex"`

### 手动注册服务

如果自动注册失败，可以手动调用：

```bash
LOCAL_IP=$(ifconfig | grep "inet " | grep -v 127.0.0.1 | head -1 | awk '{print $2}')

curl -X POST "http://localhost:8021/api/inference/register" \
  -H "Content-Type: application/json" \
  -d "{
    \"ip\": \"$LOCAL_IP\",
    \"port\": 9060,
    \"model_port\": 9060,
    \"model_type\": \"simplex\",
    \"session_type\": \"release\",
    \"service_name\": \"o45-cpp\"
  }"
```

---

## 日志位置

- HTTP Server 日志: 直接输出到终端（或重定向到 `/tmp/cpp_server.log`）
- C++ Server 日志: `[CPP] ` 前缀的行
- WAV 时序日志: `tools/omni/release_cpp/wav_timing.log`

---

## 常见问题 FAQ

### Q: 启动后显示 "体验人数已满" 或 "没有可用的推理服务"

**A**: 服务注册参数不匹配。检查：
1. 服务是否成功注册（查看启动日志）
2. `model_type` 是否与前端请求匹配
3. 使用推荐端口 9060 避免冲突

### Q: 健康检查一直超时

**A**: 
1. 检查端口是否被 Cursor IDE 占用（使用 `lsof -i :端口号`）
2. 使用推荐端口 9060
3. 模型加载需要 2-3 分钟，请耐心等待

### Q: 服务注册成功但前端无法使用

**A**: 检查：
1. Docker 网络是否正常（`docker compose ps`）
2. 推理服务 IP 是否正确（应为本机局域网 IP，不是 127.0.0.1）
3. LiveKit 配置中的 `node_ip` 是否正确
