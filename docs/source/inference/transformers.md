# Transformers

Transformers is a library of pretrained natural language processing for inference and training. Developers can use Transformers to train models on their data, build inference applications, and generate texts with large language models.

## Environment Setup

- `transformers>=4.53.0`
- `torch>=2.6` is recommended
- GPU is recommended

## Basic Usage
```python
import torch
from transformers import AutoModel, AutoTokenizer

# Load the model
model = AutoModel.from_pretrained('openbmb/MiniCPM-V-4', trust_remote_code=True)
tokenizer = AutoTokenizer.from_pretrained('openbmb/MiniCPM-V-4', trust_remote_code=True)

# Upload your image
image = Image.open('xx.jpg').convert('RGB')
question = 'What is in the image?'
msgs = [{'role': 'user', 'content': [image, question]}]

res = model.chat(
    image=None,
    msgs=msgs,
    tokenizer=tokenizer
)
print(res)

## if you want to use streaming, please make sure sampling=True and stream=True
## the model.chat will return a generator
res = model.chat(
    image=None,
    msgs=msgs,
    tokenizer=tokenizer,
    sampling=True,
    stream=True
)

generated_text = ""
for new_text in res:
    generated_text += new_text
    print(new_text, flush=True, end='')
```