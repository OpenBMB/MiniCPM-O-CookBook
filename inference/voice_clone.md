# Voice Clone

### Initialize model

```python
import torch
import librosa
from transformers import AutoModel, AutoTokenizer

model_path = 'openbmb/MiniCPM-o-2_6'
model = AutoModel.from_pretrained(model_path, trust_remote_code=True,
                                  # sdpa or flash_attention_2, no eager
                                  attn_implementation='sdpa', torch_dtype=torch.bfloat16)
model = model.eval().cuda()
tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)

model.init_tts()
model.tts.float()
```

### Usage example

<audio controls>
  <source src="./assets/male_example.wav" type="audio/wav">
  example audio case
</audio>

```python
prompt = "Please repeat the user's speech, including voice style and speech content."
audio_input, _ = librosa.load('./assets/male_example.wav', sr=16000, mono=True)
msgs = [{'role': 'user', 'content': [prompt, audio_input]}]
res = model.chat(
    msgs=msgs,
    image=None,
    tokenizer=tokenizer,
    sampling=True,
    max_new_tokens=4096,
    use_tts_template=True,
    temperature=0.3,
    generate_audio=True,
    output_audio_path='./output.wav',
)
```
