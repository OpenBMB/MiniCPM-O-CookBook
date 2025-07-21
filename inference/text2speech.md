# Text To Speech

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
  <source src="./assets/female_example.wav" type="audio/wav">
  example audio case
</audio>

```python
text_to_speak = """
男声以较低的音高，较低的音量，充满喜悦并感到深刻的幸福，表现得非常亲切与满足，“I have a dream, 世界会更好。”
"""

ref_audio_path = './assets/female_example.wav'
ref_audio, _ = librosa.load(ref_audio_path, sr=16000, mono=True)

msgs = [{'role': 'user', 'content': text_to_speak}]

tts_result = model.chat(
    msgs=msgs,
    image=None,
    tokenizer=tokenizer,
    sampling=True,
    temperature=0.3,
    max_new_tokens=4096,
    use_tts_template=True,
    generate_audio=True,
    output_audio_path='tts_output.wav',
    ref_audio=ref_audio
)
```

### Example Output

```
TTS result: 男声以较低的音高，较低的音量，充满喜悦并感到深刻的幸福，表现得非常亲切与满足，“I have a dream, 世界会更好。”
```
