import os
from datasets import load_dataset, load_from_disk
from awq import AutoAWQForCausalLM
import torch
from transformers import AutoTokenizer
import shutil

# Set the path to the original model (can be a local path or model ID)
model_path = '/openbmb/MiniCPM-o-4_5'

# Path to save the quantized model
quant_path = '/model_quantized/minicpmo4_5_awq'

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