# MiniCPM-o 完整部署指南

本文档包含 Docker 服务（前端、后端、LiveKit、Redis）和 C++ 推理服务的完整部署流程。

---

## ⚠️ 必须修改的配置

在开始部署之前，请确认以下路径配置：

| 变量          | 说明                          | 示例值                      |
| ------------- | ----------------------------- | --------------------------- |
| `CPP_DIR`   | llama.cpp-omni 编译后的根目录 | `/path/to/llama.cpp-omni` |
| `MODEL_DIR` | GGUF 模型文件目录             | `/path/to/gguf`           |

> **注意**: `PYTHON_BIN` 和 `LiveKit node_ip` 会自动检测，通常不需要手动修改。

---

## 目录结构

### 本部署包（已包含，无需修改）

```
./                                                # 部署包根目录
├── deploy_all.sh                                 # ✅ 一键部署脚本
├── DEPLOY.md                                     # ✅ 本文档
├── docker-compose.yml                            # ✅ Docker 编排文件
├── nginx.conf                                    # ✅ 前端 Nginx 配置
├── o45-frontend.tar                              # ✅ 前端 Docker 镜像
├── cpp_server/                                   # ✅ Python HTTP 服务（已包含）
│   ├── minicpmo_cpp_http_server.py              # Python 封装脚本
│   ├── requirements.txt                          # Python 依赖
│   └── assets/
│       └── default_ref_audio.wav                # 默认参考音频
└── omini_backend_code/
    ├── config/
    │   └── livekit.yaml                         # LiveKit 配置（自动更新 IP）
    └── omni_backend.tar                         # 后端 Docker 镜像
```

### 用户需要准备

```
<CPP_DIR>/                                        # ⚠️ llama.cpp-omni 编译后的目录
└── build/bin/llama-server                        # 编译后的 C++ 服务端

<MODEL_DIR>/                                      # ⚠️ GGUF 模型目录
├── MiniCPM-o-4_5-Q4_K_M.gguf                    # LLM 主模型 (~5GB)
├── audio/                                        # 音频编码器
├── vision/                                       # 视觉编码器
├── tts/                                          # TTS 模型
└── token2wav-gguf/                              # Token2Wav 模型
```

---

## 一、前置条件

### 1. 安装 Docker Desktop (macOS)

```bash
# 使用 Homebrew 安装
brew install --cask docker

# 或从官网下载：https://www.docker.com/products/docker-desktop

# 安装后启动 Docker Desktop，确保 Docker 正在运行
docker --version
```

### 2. 编译 C++ 推理服务

```bash
# ⚠️ 替换为你的 llama.cpp-omni 项目路径
cd /path/to/llama.cpp-omni

# 标准编译（自动启用 Metal 加速）
cmake -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build --target llama-server -j

# 验证编译结果
ls -la build/bin/llama-server
```

### 3. 安装 Python 依赖

```bash
# ⚠️ 替换为你的 llama.cpp-omni 项目路径
cd /path/to/llama.cpp-omni

# 使用你的 Python 环境（系统 Python 或 conda）
pip install fastapi uvicorn httpx numpy Pillow librosa soundfile requests pydantic
```

---

## 二、Docker 服务部署

### 1. 进入 Docker 部署目录

```bash
# 进入本文档所在目录
cd /path/to/docker  # ⚠️ 替换为实际路径
```

### 2. 修改 LiveKit 配置中的 IP 地址 ⚠️ 必须修改

```bash
# 获取本机 IP
LOCAL_IP=$(ifconfig | grep "inet " | grep -v 127.0.0.1 | head -1 | awk '{print $2}')
echo "本机 IP: $LOCAL_IP"

# ⚠️ 编辑 livekit.yaml，将 node_ip 和 domain 改为本机 IP
# 文件路径: omini_backend_code/config/livekit.yaml
# 修改以下两行：
#   node_ip: "YOUR_LOCAL_IP"   # 例如 "192.168.1.100"
#   domain: "YOUR_LOCAL_IP"    # 例如 "192.168.1.100"
```

### 3. 加载 Docker 镜像（如果使用 .tar 文件）

```bash
# 加载前端镜像
docker load -i o45-frontend.tar

# 加载后端镜像（如果有）
docker load -i omini_backend_code/omni_backend.tar
```

### 4. 启动 Docker 服务

```bash
# 启动所有服务（前端、后端、LiveKit、Redis）
docker compose up -d

# 查看服务状态
docker compose ps

# 查看日志
docker compose logs -f
```

### 5. 验证 Docker 服务

```bash
# 检查后端健康状态
curl http://localhost:8021/health

# 检查 LiveKit
curl http://localhost:7880

# 访问前端
open http://localhost:3000
```

---

## 三、C++ 推理服务部署

### 1. 设置环境变量 ⚠️ 必须配置

```bash
# ⚠️ 请根据实际路径修改以下变量
export CPP_DIR="/path/to/llama.cpp-omni"     # llama.cpp-omni 项目目录
export MODEL_DIR="/path/to/gguf"             # GGUF 模型目录（或 $CPP_DIR/tools/omni/gguf）
export PYTHON_BIN="/usr/bin/python3"         # Python 解释器（或 conda python 路径）

cd "$CPP_DIR"
```

### 2. 启动单工模式

⚠️ **推荐使用端口 9060**（避免与 Cursor IDE 等工具的端口冲突）

```bash
$PYTHON_BIN tools/omni/release_cpp/minicpmo_cpp_http_server.py \
    --llamacpp-root "$CPP_DIR" \
    --model-dir "$MODEL_DIR" \
    --port 9060 \
    --simplex
```

### 3. 启动双工模式

```bash
$PYTHON_BIN tools/omni/release_cpp/minicpmo_cpp_http_server.py \
    --llamacpp-root "$CPP_DIR" \
    --model-dir "$MODEL_DIR" \
    --port 9060 \
    --duplex
```

### 4. 后台运行（推荐）

```bash
# 单工模式后台运行
nohup $PYTHON_BIN tools/omni/release_cpp/minicpmo_cpp_http_server.py \
    --llamacpp-root "$CPP_DIR" \
    --model-dir "$MODEL_DIR" \
    --port 9060 \
    --simplex > /tmp/cpp_server.log 2>&1 &

# 双工模式后台运行
nohup $PYTHON_BIN tools/omni/release_cpp/minicpmo_cpp_http_server.py \
    --llamacpp-root "$CPP_DIR" \
    --model-dir "$MODEL_DIR" \
    --port 9060 \
    --duplex > /tmp/cpp_server.log 2>&1 &

# ⚠️ 服务启动需要 2-3 分钟（模型加载），查看日志确认：
tail -f /tmp/cpp_server.log
# 看到 "Application startup complete" 表示启动成功
```

### 5. 注册推理服务到后端

```bash
# 获取本机 IP
LOCAL_IP=$(ifconfig | grep "inet " | grep -v 127.0.0.1 | head -1 | awk '{print $2}')

# 注册服务（simplex 模式 + release 类型）
curl -X POST "http://localhost:8021/api/inference/register" \
  -H "Content-Type: application/json" \
  -d "{\"ip\": \"$LOCAL_IP\", \"port\": 9060, \"model_port\": 9060, \"model_type\": \"simplex\", \"session_type\": \"release\", \"service_name\": \"o45-cpp\"}"
```

**注册参数说明**：

| 参数             | 值                       | 说明                       |
| ---------------- | ------------------------ | -------------------------- |
| `model_type`   | `simplex` / `duplex` | 根据启动模式设置           |
| `session_type` | `release`              | **固定值**，兼容模式 |

### 6. 验证推理服务

```bash
# 检查健康状态
curl http://localhost:9060/health

# 检查独立健康检查端口（推理期间也可用）
curl http://localhost:9061/health
```

---

## 四、一键部署（推荐）

### 使用 deploy_all.sh

```bash
# 查看帮助
./deploy_all.sh --help

# ⚠️ 只需指定两个路径
./deploy_all.sh \
    --cpp-dir /path/to/llama.cpp-omni \
    --model-dir /path/to/gguf

# 使用双工模式
./deploy_all.sh \
    --cpp-dir /path/to/llama.cpp-omni \
    --model-dir /path/to/gguf \
    --duplex

# 或者通过环境变量配置
export CPP_DIR="/path/to/llama.cpp-omni"
export MODEL_DIR="/path/to/gguf"
./deploy_all.sh
```

### 脚本参数说明

| 参数                 | 说明                          | 必须                     |
| -------------------- | ----------------------------- | ------------------------ |
| `--cpp-dir PATH`   | llama.cpp-omni 编译后的根目录 | ✅ 是                    |
| `--model-dir PATH` | GGUF 模型目录                 | ✅ 是                    |
| `--python PATH`    | Python 解释器路径             | 否（自动检测）           |
| `--simplex`        | 单工模式                      | 否（默认）               |
| `--duplex`         | 双工模式                      | 否                       |
| `--port PORT`      | 推理服务端口                  | 否（默认**9060**） |

**端口说明**：

- Python HTTP API 端口 = `--port` 值（默认 9060）
- 健康检查端口 = `--port` + 1（默认 9061）
- C++ llama-server 端口 = `--port` + 10000（默认 19060）

### 脚本自动完成的任务

1. ✅ 检查 Docker 环境
2. ✅ 自动更新 LiveKit 配置中的 IP 地址
3. ✅ 启动 Docker 服务（前端、后端、LiveKit、Redis）
4. ✅ 安装 Python 依赖
5. ✅ 启动 C++ 推理服务
6. ✅ 注册推理服务到后端

---

## 五、常用命令

### Docker 管理

```bash
# 进入 Docker 部署目录
cd <DOCKER_DIR>  # 替换为实际路径

# 启动
docker compose up -d

# 停止
docker compose down

# 重启
docker compose restart

# 查看日志
docker compose logs -f backend
docker compose logs -f livekit
docker compose logs -f frontend

# 查看状态
docker compose ps
```

### C++ 推理服务管理

```bash
# 查看进程
ps aux | grep minicpmo

# 停止服务
pkill -f "minicpmo_cpp_http_server"

# 查看日志
tail -f /tmp/cpp_server.log

# 切换单工/双工模式
# 1. 先停止服务
pkill -f "minicpmo_cpp_http_server"
# 2. 重新启动（使用 --simplex 或 --duplex）
```

### 故障排查

#### ⚠️ 端口冲突问题（重要）

**Cursor IDE 会占用某些端口**，导致推理服务无法正常响应。已知被占用的端口：

```
8060, 8070, 8091, 8100-8109, 18060, 18088, 18090, 18100-18108
```

**解决方案**：使用推荐端口 **9060**：

```bash
# 检查端口是否被 Cursor 占用
lsof -i :8060 | grep Cursor
lsof -i :9060 | grep Cursor  # 通常不会被占用

# 使用 9060 端口启动
python minicpmo_cpp_http_server.py --port 9060 ...
```

#### 常用检查命令

```bash
# 检查端口占用
lsof -i :3000   # 前端
lsof -i :8021   # 后端
lsof -i :9060   # 推理服务（推荐端口）
lsof -i :9061   # 健康检查
lsof -i :19060  # C++ llama-server
lsof -i :7880   # LiveKit

# 检查 Docker 网络
docker network inspect docker_minicpmo-net

# 检查 Redis
docker exec minicpmo-redis redis-cli ping

# 检查服务注册
docker exec minicpmo-redis redis-cli HGETALL "app:inference:services"
```

#### 常见问题

| 问题             | 原因                       | 解决方案                                |
| ---------------- | -------------------------- | --------------------------------------- |
| "体验人数已满"   | 推理服务未注册或参数不匹配 | 检查 `model_type` 和 `session_type` |
| 健康检查超时     | 端口被 Cursor 占用         | 使用端口 9060                           |
| 模型加载超时     | 模型较大需要时间           | 等待 2-3 分钟                           |
| 无法连接 LiveKit | `node_ip` 配置错误       | 修改 livekit.yaml 中的 IP               |

---

## 六、配置文件说明

### docker-compose.yml 服务端口

| 服务             | 端口                  | 说明            |
| ---------------- | --------------------- | --------------- |
| frontend         | 3000                  | Web UI          |
| backend          | 8021, 8022            | 后端 API        |
| livekit          | 7880, 7881, 7882      | 实时通信        |
| redis            | 6379                  | 缓存服务        |
| 推理服务         | **9060** (推荐) | Python HTTP API |
| 健康检查         | 9061                  | 独立健康检查    |
| C++ llama-server | 19060                 | 内部服务        |

### 模型文件结构

```
<MODEL_DIR>/                          # ⚠️ 替换为实际 GGUF 模型目录
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
