# Finetune

:::{note}
We provide official scripts for easily fine-tuning the pretrained models **MiniCPM-V 4.5**, **MiniCPM-V 4.0**, **MiniCPM-o 2.6**, **MiniCPM-V 2.6**, **MiniCPM-Llama3-V 2.5**, and **MiniCPM-V 2.0** on downstream tasks. The fine-tuning scripts use `transformers Trainer` and `DeepSpeed` by default.

This section takes **MiniCPM-o 2.6** as an example.
:::


## Download Code

Before the fine-tuning, please go to our Cookbook repository to download the relevant code.

## Data preparation

Prepare your data in a JSON file. Each entry should be a dictionary with `id`, `image` (a path, or a dictionary of paths for multiple images), and `conversations`.

In `conversations`, use `<image>` or `<image_XX>` placeholders to position images. Without placeholders, the image is placed at the beginning. For multi-image supervised fine-tuning (SFT), it's recommended to set `MODEL_MAX_LENGTH=4096` in your script for better performance.

<details>
  <summary>
    <b>Single image example (vl_finetune_data.json) with 1 samples.</b>
  </summary>

```
  [
    {
      "id": "0",
      "image": 'path/to/image_0.jpg',
      "conversations": [
            {
              'role': 'user', 
              'content': '<image>\\nHow many desserts are on the white plate?'
            }, 
            {
                'role': 'assistant', 
                'content': 'There are three desserts on the white plate.'
            },   
            {
                'role': 'user', 
                'content': 'What type of desserts are they?'
            },
            {
                'role': 'assistant', 
                'content': 'The desserts are cakes with bananas and pecans on top. They share similarities with donuts, but the presence of bananas and pecans differentiates them.'
            }, 
            {
                'role': 'user', 
                'content': 'What is the setting of the image?'}, 
            {
                'role': 'assistant', 
                'content': 'The image is set on a table top with a plate containing the three desserts.'
            },
        ]
    },
  ]
```

</details>


<details>
  <summary>
    <b>Multiple images example (vl_finetune_data.json) with 1 samples.</b>
  </summary>

```
  [
    {
      "id": "0",
      "image": {
        "<image_00>": "path/to/image_0.jpg",
        "<image_01>": "path/to/image_1.jpg",
        "<image_02>": "path/to/image_2.jpg",
        "<image_03>": "path/to/image_3.jpg"
      },
      "conversations": [
        {
          "role": "user", 
          "content": "How to create such text-only videos using CapCut?\\n<image_00>\\n<image_01>\\n<image_02>\\n<image_03>\\n"
        }, 
        {
          "role": "assistant", 
          "content": "To create a text-only video as shown in the images, follow these steps in CapCut..."
        }
      ]
    }
  ]
```
</details>

## Full-parameter finetuning

This method updates all model parameters. Specify your model and data paths in the script:

```shell
MODEL="MiniCPM-o-2_6" # or "openbmb/MiniCPM-V-2_6", "openbmb/MiniCPM-Llama3-V-2_5", "openbmb/MiniCPM-V-2"
DATA="path/to/training_data.json"
EVAL_DATA="path/to/test_data.json"
LLM_TYPE="qwen" # llama for MiniCPM-V-4, minicpm for MiniCPM-V-2, llama3 for MiniCPM-Llama3-V-2_5, qwen for MiniCPM-o-2_6/MiniCPM-V-2_6
```

To launch your training, run:
```shell
sh finetune_ds.sh
```


## LoRA finetuning

LoRA is a lightweight method that updates only a small subset of parameters. To launch your training, run:
```shell
sh finetune_lora.sh
```

After training, load the LoRA adapter. Use an absolute path for the base model.

```python
from peft import PeftModel
from transformers import AutoModel

model_type = "openbmb/MiniCPM-o-2_6" # or "openbmb/MiniCPM-V-2_6", "openbmb/MiniCPM-Llama3-V-2_5", "openbmb/MiniCPM-V-2"
path_to_adapter = "path_to_your_fine_tuned_checkpoint"

model = AutoModel.from_pretrained(
    model_type,
    trust_remote_code=True
)

lora_model = PeftModel.from_pretrained(
    model,
    path_to_adapter,
    device_map="auto",
    trust_remote_code=True
).eval().cuda()
```


## Model Fine-tuning Memory Usage Statistics

The following table shows memory usage for fine-tuning on NVIDIA A100 (80GiB) GPUs with DeepSpeed Zero-3, a max length of 2048, and a batch size of 1.

| Fine-tuning Method | GPUs: 2 | GPUs: 4 | GPUs: 8 |
|--------------------|---------|---------|---------|
| LoRA Fine-tuning   | 14.4 GiB| 13.6 GiB| 13.1 GiB|
| Full Parameters Fine-tuning | 16.0 GiB | 15.8 GiB | 15.63GiB |

## Tips & Troubleshooting

<details>
  <summary><b>How to handle Out of Memory (OOM) errors?</b></summary>
  
  - **Adjust Hyperparameters**: 
    - Reduce `--model_max_length` (e.g., to 1200).
    - Lower `--batch_size` (e.g., to 1) and increase `gradient_accumulation_steps` to compensate.
    - For high-resolution images, reduce `--max_slice_nums` to lower token usage per image.
  - **Reduce Model Parameters**:
    - Freeze the vision module with `--tune_vision false`.
    - Use LoRA finetuning instead of full-parameter tuning.
  - **Use DeepSpeed Optimization**:
    - Configure DeepSpeed Zero Stage 2 or 3 to offload optimizer and model parameters to the CPU. See the [Hugging Face DeepSpeed docs](https://huggingface.co/docs/transformers/deepspeed) for details.
</details>

<details>
  <summary><b>How to fix errors when loading a LoRA checkpoint?</b></summary>
  
  An error like `NotImplementedError` when using `AutoPeftModelForCausalLM` (see [issue #168](https://github.com/OpenBMB/MiniCPM-V/issues/168)) can occur if the model lacks `get_input_embeddings` and `set_input_embeddings` methods.
  
  **Solution**:
  1.  Load the model using `PeftModel` as shown in the LoRA section.
  2.  Ensure your `model_minicpmv.py` file is up-to-date from the model's Hugging Face repository (e.g., [MiniCPM-Llama3-V-2_5](https://huggingface.co/openbmb/MiniCPM-Llama3-V-2_5/tree/main) or [MiniCPM-V-2](https://huggingface.co/openbmb/MiniCPM-V-2)).
</details>

<details>
  <summary><b>Other common questions.</b></summary>
  
  - **How to use `flash_attention_2`?**
    - If your environment supports it, add `_attn_implementation="flash_attention_2"` when loading the model: `AutoModel.from_pretrained('model_name', _attn_implementation="flash_attention_2")`.
  - **Can I use original image sizes?**
    - Yes. The model supports up to 1344x1344 resolution, so you can use original sizes instead of resizing to 512.
  - **How to determine `max_length` for training data?**
    - Use [this function](https://github.com/OpenBMB/MiniCPM-V/blob/main/finetune/dataset.py#L220) to sample your data's length, then set `--model_max_length` in your command.
  - **Where to find LoRA hyperparameter documentation?**
    - Refer to the [LoRA documentation](https://huggingface.co/docs/peft/en/package_reference/lora#peft.LoraConfig) for guidance. For general training arguments, see the [Transformers documentation](https://huggingface.co/docs/transformers/main_classes/trainer#transformers.TrainingArguments).
</details>
