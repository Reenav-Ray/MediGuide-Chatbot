import streamlit as st
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

st.title("🧠 MediGuide Chatbot")

# Load tokenizer and model from local files
@st.cache_resource
def load_model():
    tokenizer = AutoTokenizer.from_pretrained("gpt2") 
    model = AutoModelForCausalLM.from_pretrained(
        "gpt2",
        local_files_only=True,
        trust_remote_code=True,
    )
    return tokenizer, model

tokenizer, model = load_model()

user_input = st.text_input("Ask a medical question:")

if st.button("Get Answer") and user_input:
    inputs = tokenizer(user_input, return_tensors="pt")
    outputs = model.generate(**inputs, max_length=100, pad_token_id=tokenizer.eos_token_id)
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    st.text_area("MediGuide says:", value=answer, height=200)
