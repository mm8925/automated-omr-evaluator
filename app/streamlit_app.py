import streamlit as st
import os
import json
from PIL import Image

# --- Paths ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
answer_key_path = os.path.join(BASE_DIR, "data", "answer_key.json")

# --- Load answer key ---
with open(answer_key_path, "r") as f:
    ANSWER_KEY = json.load(f)

# --- Streamlit UI ---
st.title("Automated OMR Evaluation System")

uploaded_file = st.file_uploader(
    "Upload OMR sheet image", type=["png", "jpg", "jpeg"]
)

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded OMR Sheet", use_column_width=True)
    st.write("Processing... (bubble detection coming next)")
