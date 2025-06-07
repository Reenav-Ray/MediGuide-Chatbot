from flask import Flask, render_template, request, jsonify
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import logging
import traceback
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

Model_Path = os.environ.get("MODEL_PATH", os.path.join(os.path.dirname(os.path.abspath(__file__)), "model"))

def load_model():

    try:
        logger.info(f"Loading model from: {Model_Path}")
        if not os.path.exists(Model_Path):
            if "/" in Model_Path and not Model_Path.startswith("/"):
                logger.info(f"Loading model from Hugging Face: {Model_Path}")
                tokenizer = GPT2Tokenizer.from_pretrained(Model_Path)
                model = GPT2LMHeadModel.from_pretrained(Model_Path, use_safetensors=False)
            else:
                raise FileNotFoundError(f"Directory not found: {Model_Path}")
        else:
            tokenizer = GPT2Tokenizer.from_pretrained(Model_Path, local_files_only=True)
            model = GPT2LMHeadModel.from_pretrained(Model_Path, local_files_only=True, use_safetensors=False)

        logger.info("Model loaded successfully.")
        logger.info(f"Model configuration: {model.config}")

        model = model.cpu()

        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token

        return tokenizer, model

    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        logger.error(traceback.format_exc())
        raise

tokenizer, model = load_model()

@app.route('/')
def home():
    """Render the main HTML page."""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat API requests."""
    data = request.get_json()
    user_message = data.get('message', '').strip()

    if not user_message:
        return jsonify({'response': 'Please enter a message'})

    try:
        prompt = (
            "As a medical AI system, give a direct expert medical response to this question without "
            "creating a fictional conversation. Your answer should be factual, concise, and "
            "include appropriate medical disclaimers. Do not respond as if you are in a dialogue.\n\n"
            f"Question: {user_message}\n\nMedical Response:"
        )

        input_ids = tokenizer.encode(prompt, return_tensors="pt").cpu()
        attention_mask = torch.ones_like(input_ids)

        output = model.generate(
            input_ids=input_ids,
            attention_mask=attention_mask,
            max_length=120,
            num_return_sequences=1,
            pad_token_id=tokenizer.eos_token_id,
            temperature=0.2,
            top_p=0.5,
            do_sample=True,
            repetition_penalty=2.0,
            no_repeat_ngram_size=3,
            early_stopping=True
        )

        decoded = tokenizer.decode(output[0], skip_special_tokens=True)
        if "Medical Response:" in decoded:
            medical_response = decoded.split("Medical Response:", 1)[1].strip()
        else:
            medical_response = decoded.replace(prompt, "").strip()

        logger.info(f"User Input: {user_message}")
        logger.info(f"Generated Response: {medical_response}")

        return jsonify({'response': medical_response})

    except Exception as e:
        logger.error(f"Generation failed: {e}")
        logger.error(traceback.format_exc())
        return jsonify({'response': 'Sorry, I encountered an error processing your request.'})

port = int(os.environ.get("PORT", 5000))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=False)