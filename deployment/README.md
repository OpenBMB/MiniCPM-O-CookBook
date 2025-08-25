# Model Deployment Guide

Multiple deployment solutions for efficient MiniCPM-o model deployment across different environments.

📖 [中文版本](./README_zh.md) | [Back to Main](../)

## Deployment Framework Comparison

| Framework | Performance | Ease of Use | Scalability | Hardware | Best For |
|-----------|-------------|-------------|-------------|----------|----------|
| **vLLM** | High | Medium | High | GPU | Large-scale production services |
| **SGLang** | High | Medium | High | GPU | Structured generation tasks |
| **Ollama** | Medium | Excellent | Medium | CPU/GPU | Personal use, rapid prototyping |
| **Llama.cpp** | Medium | High | Medium | CPU | Edge devices, lightweight deployment |

## Framework Details

### vLLM (Very Large Language Model)
- High-throughput inference engine with PagedAttention memory management
- Dynamic batching support, OpenAI-compatible API
- Ideal for production API services and large-scale batch inference
- Recommended hardware: GPU with more than 18GB of VRAM

### SGLang (Structured Generation Language)
- Structured generation optimization with efficient KV cache management
- Complex control flow and function calling optimization support
- Suitable for complex reasoning chains and structured text generation
- Recommended hardware: GPU with more than 18GB of VRAM

### Ollama
- One-click model management with simple command-line interface
- Automatic quantization support, REST API interface
- Perfect for personal development environments and research prototyping
- Hardware requirements: 8GB+ RAM, supports CPU/GPU

### Llama.cpp
- Pure C++ implementation with CPU-optimized inference
- Multiple quantization support, lightweight deployment
- Ideal for mobile devices and edge computing
- Hardware requirements: 4GB+ RAM, various CPU architectures

## Selection Guide

- **Production Environment (High Concurrency)**: vLLM - Best performance, optimal scalability
- **Complex Reasoning Tasks**: SGLang - Structured generation, function calling optimization
- **Personal Development**: Ollama - Simple to use, quick setup
- **Edge Deployment**: Llama.cpp - Lightweight, low power consumption
