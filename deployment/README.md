# Model Deployment Guide

Multiple deployment solutions for efficient MiniCPM-o model deployment across different environments.

📖 [中文版本](./README_zh.md) | [Back to Main](../)

## Deployment Framework Comparison

| Framework | Performance | Ease of Use | Scalability | Hardware | Best For |
|-----------|-------------|-------------|-------------|----------|----------|
| [**vLLM**](./vllm/) | High | Medium | High | GPU | Large-scale production services |
| [**SGLang**](./sglang/) | High | Medium | High | GPU | Structured generation tasks |
| [**Ollama**](./ollama/) | Medium | Excellent | Medium | CPU/GPU | Personal use, rapid prototyping |
| [**Llama.cpp**](./llama.cpp/) | Medium | High | Medium | CPU | Edge devices, lightweight deployment |

## Framework Details

### [vLLM](./vllm/) (Very Large Language Model)
- High-throughput inference engine with PagedAttention memory management
- Dynamic batching support, OpenAI-compatible API
- Ideal for production API services and large-scale batch inference
- Recommended hardware: GPU with more than 18GB of VRAM

### [SGLang](./sglang/) (Structured Generation Language)
- Structured generation optimization with efficient KV cache management
- Complex control flow and function calling optimization support
- Suitable for complex reasoning chains and structured text generation
- Recommended hardware: GPU with more than 18GB of VRAM

### [Ollama](./ollama/)
- One-click model management with simple command-line interface
- Automatic quantization support, REST API interface
- Perfect for personal development environments and research prototyping
- Hardware requirements: 8GB+ RAM, supports CPU/GPU

### [Llama.cpp](./llama.cpp/)
- Pure C++ implementation with CPU-optimized inference
- Multiple quantization support, lightweight deployment
- Ideal for mobile devices and edge computing
- Hardware requirements: 4GB+ RAM, various CPU architectures

## Selection Guide

- **Production Environment (High Concurrency)**: vLLM - Best performance, optimal scalability
- **Complex Reasoning Tasks**: SGLang - Structured generation, function calling optimization
- **Personal Development**: Ollama - Simple to use, quick setup
- **Edge Deployment**: Llama.cpp - Lightweight, low power consumption

## MiniCPM-o 4.5 Framework Support Matrix
<table>
  <thead>
    <tr>
      <th>Category</th>
      <th>Framework</th>
      <th>Cookbook Link</th>
      <th>Upstream PR</th>
      <th>Supported since(branch)</th>
      <th>Supported since(release)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td rowspan="2">Edge(On-device)</td>
      <td>Llama.cpp</td>
      <td><a href="https://github.com/OpenSQZ/MiniCPM-o-CookBook/blob/main/deployment/llama.cpp/minicpm-o4_5_llamacpp.md">Llama.cpp Doc</a></td>
      <td><a href="https://github.com/ggml-org/llama.cpp/pull/19211">#19211</a>(2026-01-30)</td>
      <td>master(2026-01-30)</td>
      <td><a href="https://github.com/ggml-org/llama.cpp/releases/tag/b7895">b7895</a></td>
    </tr>
    <tr>
      <td>Ollama</td>
      <td><a href="https://github.com/OpenSQZ/MiniCPM-o-CookBook/blob/main/deployment/ollama/minicpm-o4_5_ollama.md">Ollama Doc</a></td>
      <td><a href="https://github.com/ollama/ollama/pull/12078">#12078</a>(2025-08-26)</td>
      <td>Merging</td>
      <td>Waiting for official release</td>
    </tr>
    <tr>
      <td rowspan="2">Serving(Cloud)</td>
      <td>vLLM</td>
      <td><a href="https://github.com/OpenSQZ/MiniCPM-o-CookBook/blob/main/deployment/vllm/minicpm-o4_5_vllm.md">vLLM Doc</a></td>
      <td><a href="https://github.com/vllm-project/vllm/pull/33431">#33431</a>(2026-01-30)</td>
      <td>Merging</td>
      <td>Waiting for official release</td>
    </tr>
    <tr>
      <td>SGLang</td>
      <td><a href="https://github.com/OpenSQZ/MiniCPM-o-CookBook/blob/main/deployment/sglang/MiniCPM-o4_5_sglang.md">SGLang Doc</a></td>
      <td><a href="https://github.com/sgl-project/sglang/pull/9610">#9610</a>(2025-08-26)</td>
      <td>Merging</td>
      <td>Waiting for official release</td>
    </tr>
    <tr>
      <td>Finetuning</td>
      <td>LLaMA-Factory</td>
      <td><a href="https://github.com/OpenSQZ/MiniCPM-o-CookBook/blob/main/finetune/finetune_llamafactory.md">LLaMA-Factory Doc</a></td>
      <td><a href="https://github.com/hiyouga/LLaMA-Factory/pull/9022">#9022</a>(2025-08-26)</td>
      <td>main(2025-08-26)</td>
      <td>Waiting for official release</td>
    </tr>
    <tr>
      <td rowspan="2">Quantization</td>
      <td>GGUF</td>
      <td><a href="https://github.com/OpenSQZ/MiniCPM-o-CookBook/blob/main/quantization/gguf/minicpm-o4_5_gguf_quantize.md">GGUF Doc</a></td>
      <td>—</td>
      <td>—</td>
      <td>—</td>
    </tr>
    <tr>
      <td>AWQ</td>
      <td><a href="https://github.com/OpenSQZ/MiniCPM-o-CookBook/blob/main/quantization/awq/minicpm-o4_5_awq_quantize.md">AWQ Doc</a></td>
      <td><a href="https://github.com/tc-mb/AutoAWQ">tc-mb/AutoAWQ</a></td>
      <td>—</td>
      <td>—</td>
    </tr>
    <tr>
      <td>Demos</td>
      <td>Gradio Demo</td>
      <td><a href="https://github.com/OpenSQZ/MiniCPM-o-CookBook/blob/main/demo/web_demo/gradio/README_o45.md">Gradio Demo Doc</a></td>
      <td>—</td>
      <td>—</td>
      <td>—</td>
    </tr>
  </tbody>
 </table>


If you'd like us to prioritize support for another open-source framework, please let us know via this
[short form](https://docs.google.com/forms/d/e/1FAIpQLSdyTUrOPBgWqPexs3ORrg47ZcZ1r4vFQaA4ve2iA7L9sMfMWw/viewform).
