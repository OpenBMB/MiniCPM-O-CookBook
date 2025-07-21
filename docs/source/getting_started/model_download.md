# Model Download

This guide provides instructions for downloading the MiniCPM-V 4.0 model from Hugging Face Hub and ModelScope.

## Available Model

**MiniCPM-V 4.0**: Vision Understanding model for image and video processing (~8GB)

## Hugging Face Hub Download

Hugging Face Hub is the primary platform for accessing MiniCPM-V 4.0, offering excellent global accessibility and integration with the transformers library.

### Prerequisites

```bash
pip install huggingface-hub
```

### Method 1: Using huggingface-cli (Recommended)

```bash
# Download to specific directory
huggingface-cli download openbmb/MiniCPM-V-4 --local-dir ./MiniCPM-V-4

# Download with resume capability
huggingface-cli download openbmb/MiniCPM-V-4 --local-dir ./MiniCPM-V-4 --resume-download
```

### Method 2: Using Git LFS

```bash
# Install git-lfs if not already installed
git lfs install

# Clone the repository
git clone https://huggingface.co/openbmb/MiniCPM-V-4
```

### Method 3: Direct Integration

```python
from transformers import AutoModel, AutoTokenizer

# This will automatically download and cache the model
model = AutoModel.from_pretrained('openbmb/MiniCPM-V-4', trust_remote_code=True)
tokenizer = AutoTokenizer.from_pretrained('openbmb/MiniCPM-V-4', trust_remote_code=True)
```

## ModelScope Download

ModelScope provides an alternative platform with optimized access for users in China and other regions. For detailed information, refer to the [ModelScope Download Documentation](https://modelscope.cn/docs/models/download).

### Prerequisites

```bash
pip install modelscope
```

### Method 1: Using Modelscope SDK

```bash
# Install dependencies
pip install modelscope[cv] -f https://modelscope.oss-cn-beijing.aliyuncs.com/releases/repo.html

# Download using Python
python -c "
from modelscope import snapshot_download
model_dir = snapshot_download('openbmb/MiniCPM-V-4', cache_dir='./models')
print(f'Model downloaded to: {model_dir}')
"
```

### Method 2: Using Git

```bash
# Clone from ModelScope
git clone https://www.modelscope.cn/openbmb/MiniCPM-V-4.git

# Or with specific depth for faster clone
git clone --depth 1 https://www.modelscope.cn/openbmb/MiniCPM-V-4.git
```

### Method 3: Direct Integration

```python
from modelscope import AutoModel, AutoTokenizer

# Load model directly from ModelScope
model = AutoModel.from_pretrained('openbmb/MiniCPM-V-4', trust_remote_code=True)
tokenizer = AutoTokenizer.from_pretrained('openbmb/MiniCPM-V-4', trust_remote_code=True)
```

### Method 4: Using Modelscope CLI

```bash
# Install Modelscope CLI
pip install modelscope

# Download using CLI
modelscope download --model openbmb/MiniCPM-V-4 --local_dir ./MiniCPM-V-4
```

## Platform Comparison

| Feature | Hugging Face Hub | ModelScope |
|---------|------------------|------------|
| **Global Access** | Excellent | Good |
| **China Access** | May be slow | Optimized |
| **Integration** | transformers | modelscope + transformers |
| **Documentation** | Extensive | [Official Docs](https://modelscope.cn/docs/models/download) |
| **Download Speed** | Varies by region | Fast in China |

## Storage Requirements

- **Disk Space**: Approximately 8GB of storage
- **Memory**: At least 8GB RAM recommended for inference  
- **GPU Memory**: 6-18GB VRAM depending on quantization and batch size

## Verification

After downloading, verify your model installation:

```python
import torch
from transformers import AutoModel, AutoTokenizer

# Load the model (adjust path as needed)
model_path = "./MiniCPM-V-4"  # or your download path
model = AutoModel.from_pretrained(model_path, trust_remote_code=True)
tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)

print(f"Model loaded successfully!")
print(f"Model parameters: {sum(p.numel() for p in model.parameters()) / 1e9:.1f}B")
```

## Troubleshooting

### Hugging Face Issues
- **Slow download**: Try using a VPN or mirror sites
- **Download interruption**: Use `--resume-download` flag
- **Authentication**: Login with `huggingface-cli login` if needed

### ModelScope Issues  
- **Network errors**: Check [ModelScope](https://modelscope.cn/docs/models/download) status
- **Permission issues**: Ensure proper access credentials
- **Installation problems**: Try `pip install modelscope --upgrade`

## Next Steps

After successfully downloading the model:

1. **Setup Environment**: Install required dependencies from `requirements.txt`
2. **Run Examples**: Try the notebooks in the `inference/` directory  
3. **Customize**: Explore fine-tuning options in the `finetune/` directory

For more detailed usage instructions, see our [Quick Start Guide](./quickstart.md).
