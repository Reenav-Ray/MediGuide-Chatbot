from huggingface_hub import HfApi
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MODEL_PATH = "/home/shree/code/Mediguide/Mediguide/mediguide_checkpoint_epoch2"
HF_USERNAME = "ShreeR4M"
REPO_NAME = "mediguide-model"  
REPO_ID = f"{HF_USERNAME}/{REPO_NAME}"

def upload_model():
    try:
        logger.info(f"Starting upload of model from {MODEL_PATH} to {REPO_ID}...")
        
        api = HfApi()
        
        api.create_repo(repo_id=REPO_ID, repo_type="model", exist_ok=True)
        
        logger.info(f"Repository {REPO_ID} created/confirmed. Beginning file upload...")
        logger.info("This may take some time depending on the model size and your internet speed...")
        
        api.upload_folder(
            folder_path=MODEL_PATH,
            repo_id=REPO_ID,
            repo_type="model"
        )
        
        logger.info(f"Model successfully uploaded to: https://huggingface.co/{REPO_ID}")
        logger.info(f"Use this as your MODEL_PATH environment variable in Render: {REPO_ID}")
        
    except Exception as e:
        logger.error(f"Error uploading model: {e}")
        raise

if __name__ == "__main__":
    upload_model()
