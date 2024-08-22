
import torch
from flask import Flask, request, jsonify
import transformers
from transformers import AutoTokenizer, AutoModelForCausalLM, LlamaForCausalLM


MIN_TRANSFORMERS_VERSION = '4.25.1'

# check transformers version
assert transformers.__version__ >= MIN_TRANSFORMERS_VERSION, f'Please upgrade transformers to version {MIN_TRANSFORMERS_VERSION} or higher.'

app = Flask(__name__)

# Load the Hermes-3-Llama-3.1-8B model and tokenizer
model_name = "nvidia/Minitron-4B-Base"
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
model = LlamaForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16,
    device_map="auto",
    load_in_8bit=False,
    load_in_4bit=False,
    use_flash_attention_2=False
)
model = model.to('cuda:0')
@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    prompt = data.get('prompt', '')
    max_length = data.get('max_length', 8000)
    print(prompt)
    inputs = tokenizer.encode(prompt, return_tensors='pt').to(model.device)
    # Generate the output
    outputs = model.generate(inputs, max_length=8000)
    # Decode and print the output
    output_text = tokenizer.decode(outputs[0])
    print(output_text)
    return jsonify({'response': output_text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)


