import streamlit as st
import os
import json
from PIL import Image
import cv2
import numpy as np

# --- Paths ---
# Get absolute path to project root
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

# --- Bubble Detection Functions ---
def detect_bubbles(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    bubble_contours = []
    for c in contours:
        area = cv2.contourArea(c)
        if 100 < area < 1000:  # adjust threshold for bubble size
            bubble_contours.append(c)

    # Sort contours top-to-bottom, left-to-right
    bubble_contours = sorted(bubble_contours, key=lambda c: (cv2.boundingRect(c)[1], cv2.boundingRect(c)[0]))
    return bubble_contours, thresh

def extract_answers(bubble_contours, thresh):
    detected_answers = {}
    for idx, c in enumerate(bubble_contours):
        x, y, w, h = cv2.boundingRect(c)
        roi = thresh[y:y+h, x:x+w]
        filled = cv2.countNonZero(roi) > 50  # threshold for marked bubble
        detected_answers[str(idx+1)] = 'a' if filled else ''  # placeholder: assumes 'a'
    return detected_answers

# --- Process Uploaded File ---
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded OMR Sheet", use_column_width=True)

    # Save temporary file for OpenCV processing
    temp_file = os.path.join(BASE_DIR, "temp.jpg")
    image.save(temp_file)

    # Detect bubbles and extract answers
    bubble_contours, thresh = detect_bubbles(temp_file)
    detected_answers = extract_answers(bubble_contours, thresh)

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
