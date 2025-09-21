import streamlit as st
import os
import json
from PIL import Image
import numpy as np

# --- Paths ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
answer_key_path = os.path.join(BASE_DIR, "data", "answer_key.json")

# --- Load answer key ---
if os.path.exists(answer_key_path):
    with open(answer_key_path, "r") as f:
        ANSWER_KEY = json.load(f)
    st.success(f"Answer key loaded with {len(ANSWER_KEY)} questions.")
else:
    st.error("Answer key not found at data/answer_key.json")
    st.stop()

# --- Streamlit UI ---
st.title("Automated OMR Evaluation System (Demo)")

uploaded_file = st.file_uploader(
    "Upload OMR sheet image", type=["png", "jpg", "jpeg"]
)

# --- Dummy Bubble Detection ---
def extract_answers_dummy():
    # Generates random or placeholder answers
    detected_answers = {}
    for i in range(1, 101):
        detected_answers[str(i)] = 'a'  # placeholder, assumes all 'a'
    return detected_answers

# --- Process Uploaded File ---
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded OMR Sheet", use_column_width=True)

    detected_answers = extract_answers_dummy()

    # --- Calculate Scores ---
    subject_scores = {}
    total_score = 0
    questions_per_subject = 20

    for i in range(5):
        score = 0
        for q in range(i*questions_per_subject+1, (i+1)*questions_per_subject+1):
            if detected_answers.get(str(q)) == ANSWER_KEY.get(str(q)):
                score += 1
        subject_scores[f"Subject {i+1}"] = score
        total_score += score

    # --- Display Results ---
    st.subheader("Results")
    for sub, score in subject_scores.items():
        st.write(f"{sub}: {score}/20")
    st.write(f"**Total Score: {total_score}/100**")
