# AWQ

:::{Note}
**Support:** MiniCPM-V 4.5, MiniCPM-V 4.0
:::

## Method 1 (Use the pre-quantized model)

### 1.Download the Model
<!-- 下载量化模型
https://huggingface.co/openbmb/MiniCPM-V-4_5-AWQ
 -->

Download the 4-bit quantized MiniCPM-V-4_5 model with AutoAWQ from [HuggingFace](https://huggingface.co/openbmb/MiniCPM-V-4_5-AWQ)

```Bash
git clone https://huggingface.co/openbmb/MiniCPM-V-4_5-AWQ
```

### 2.Run with vLLM

```python
import os
from PIL import Image
from transformers import AutoTokenizer
from vllm import LLM, SamplingParams


# Quantized model name or path
MODEL_NAME = "openbmb/MiniCPM-V-4_5-AWQ"

# List of image file paths
IMAGES = [
    "image.png",
]

# Open and convert image
image = Image.open(IMAGES[0]).convert("RGB")

# Initialize tokenizer
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)

# Initialize LLM
llm = LLM(
    model=MODEL_NAME, 
    # gpu_memory_utilization=0.9,
    max_model_len=2048,
    trust_remote_code=True,
    # disable_mm_preprocessor_cache=True,
    # limit_mm_per_prompt={"image": 5}
)

# Build messages
messages = [{
    "role": "user",
    "content": "(<image>./</image>)\nPlease describe the content of this image",
    # "content": "(<image>./</image>)\n请描述这张图片的内容",
}]

# Apply chat template to the messages
prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)

# Set stop token IDs
stop_tokens = ['<|im_end|>', '</s>']
stop_token_ids = [tokenizer.convert_tokens_to_ids(i) for i in stop_tokens]

# Set generation parameters
sampling_params = SamplingParams(
    stop_token_ids=stop_token_ids,
    temperature=0.7,
    # detokenize=True,
    top_p=0.8,
    # top_k=100,
    # seed=3472,
    max_tokens=1024,
    # min_tokens=150,
)

# Get model output
outputs = llm.generate({
    "prompt": prompt,
    "multi_modal_data": {
        "image": image
    }
}, sampling_params=sampling_params)
print(outputs[0].outputs[0].text)
```


## Method 2 (Quantize the model yourself)

### 1.Download the Model
<!-- 下载模型
https://huggingface.co/openbmb/MiniCPM-V-4_5
 -->

Download the MiniCPM-V 4.5 model from [HuggingFace](https://huggingface.co/openbmb/MiniCPM-V-4_5)

```Bash
git clone https://huggingface.co/openbmb/MiniCPM-V-4_5
```

### 2.Download and build AutoAWQ
Since the official AutoAWQ repository is no longer maintained, please download and build our fork instead.
```Bash
git clone https://github.com/tc-mb/AutoAWQ.git
cd AutoAWQ
pip install -e .
```

### 3.Quantization Script

Run the following quantization script (replace model_path and quant_path with the paths to the original model and the quantized model, respectively).

```python
import os
from datasets import load_dataset, load_from_disk
from awq import AutoAWQForCausalLM
import torch
from transformers import AutoTokenizer
import shutil

# Set the path to the original model (can be a local path or model ID)
model_path = '/openbmb/MiniCPM-V-4_5'

# Path to save the quantized model
quant_path = '/model_quantized/minicpmv4_5_awq'

# Quantization configuration: 4-bit weights, group size 128, GEMM backend
quant_config = { "zero_point": True, "q_group_size": 128, "w_bit": 4, "version": "GEMM" } # "w_bit":4 or 8	


# Load the original model and tokenizer
model = AutoAWQForCausalLM.from_pretrained(model_path, trust_remote_code=True, torch_dtype=torch.bfloat16)
tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)

# Copy files that exist in model_path but not in quant_path (excluding weight files)
def copy_files_not_in_B(A_path, B_path):
    """
    Copies files from directory A to directory B if they exist in A but not in B.

    :param A_path: Path to the source directory (A).
    :param B_path: Path to the destination directory (B).
    """
    # Ensure source directory exists
    if not os.path.exists(A_path):
        raise FileNotFoundError(f"The directory {A_path} does not exist.")
    if not os.path.exists(B_path):
        os.makedirs(B_path)

    # List all files in directory A except weight files (e.g., .bin or safetensors)
    files_in_A = os.listdir(A_path)
    files_in_A = set([file for file in files_in_A if not (".bin" in file or "safetensors" in file )])
    # List all files in directory B
    files_in_B = set(os.listdir(B_path))

    # Determine which files need to be copied
    files_to_copy = files_in_A - files_in_B

    # Copy each missing file from A to B
    for file in files_to_copy:
        src_file = os.path.join(A_path, file)
        dst_file = os.path.join(B_path, file)
        if os.path.isfile(src_file):
            shutil.copy2(src_file, dst_file)

# Define data loading methods
# Load the Alpaca dataset
def load_alpaca():
    data = load_dataset("tatsu-lab/alpaca", split="train")

    # Convert each example into a chat-style prompt
    def concatenate_data(x):
        if x['input'] and x['instruction']:
            msgs = [
                    {"role": "system", "content": x['instruction']},
                    {"role": "user", "content": x['input']},
                    {"role": "assistant", "content": x['output']},
            ]
        elif x['input']:
            msgs = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": x['input']},
                {"role": "assistant", "content": x['output']}
            ]
        else:
            msgs = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": x['instruction']},
                {"role": "assistant", "content": x['output']}
            ]
        
        data = tokenizer.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)
        return {"text": data}
    
    concatenated = data.map(concatenate_data)
    return [text for text in concatenated["text"]][:1024]

# Load Wikitext dataset
def load_wikitext():
    data = load_dataset('wikitext', 'wikitext-2-raw-v1', split="train")
    return [text for text in data["text"] if text.strip() != '' and len(text.split(' ')) > 20]


# Load calibration data
calib_data = load_alpaca()
# Quantize
model.quantize(tokenizer, quant_config=quant_config, calib_data=calib_data)

# shutil.rmtree(quant_path, ignore_errors=True)

# Save the quantized model
model.save_quantized(quant_path)
tokenizer.save_pretrained(quant_path)

copy_files_not_in_B(model_path, quant_path)
print(f'Model is quantized and saved at "{quant_path}"')
```

