import os
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer, AutoModelForCausalLM, AutoTokenizer
import logging
import shutil

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def download_model():
    MODEL_DIR = "/home/shree/code/Mediguide/Mediguide/mediguide_checkpoint_epoch2"
    BACKUP_DIR = "/home/shree/code/Mediguide/Mediguide/mediguide_backup"
    
    if os.path.exists(MODEL_DIR):
        logger.info(f"Creating backup of existing model files at {BACKUP_DIR}")
        if os.path.exists(BACKUP_DIR):
            shutil.rmtree(BACKUP_DIR)
        shutil.copytree(MODEL_DIR, BACKUP_DIR)
        
    try:
        logger.info("Downloading GPT-2 Medium model...")
        model_name = "gpt2-medium" 
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name)
        
        os.makedirs(MODEL_DIR, exist_ok=True)
        
        logger.info(f"Saving model to {MODEL_DIR}")
        model.save_pretrained(MODEL_DIR, safe_serialization=False)  # Don't use safetensors
        tokenizer.save_pretrained(MODEL_DIR)
        logger.info("Model and tokenizer saved successfully!")
        return True
    except Exception as e:
        logger.error(f"Error downloading model: {e}")
        return False

if __name__ == "__main__":
    success = download_model()
    