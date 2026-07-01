import streamlit as st
import requests
import json

# Replace with your API key
API_KEY = "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"
API_URL = "https://api.x.ai/v1/chat/completions"  # Grok example; adjust for OpenAI

def generate_questions(mode, input_text, num_questions=10):
    if mode == "Topic":
        prompt = f"""You are an expert QA/BA interviewer specializing in Telecom, OSS/BSS, Software Testing.
Generate {num_questions} high-quality interview questions for the topic: {input_text}.
Include a mix of technical, behavioral, and scenario-based questions.
Format as numbered list with brief category (e.g., Technical, Behavioral)."""
    else:  # JD
        prompt = f"""Analyze this Job Description and generate {num_questions} tailored interview questions.
JD: {input_text}

Focus on key skills, responsibilities, and tools mentioned. Categorize questions (Technical, Experience, Behavioral, Scenario).
Make them relevant for QA/Testing/BA roles."""

    payload = {
        "model": "grok-3",  # or gpt-4o-mini etc.
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 1500
    }
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(API_URL, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.text}"

# Streamlit UI
st.title("📋 Interview Question Vault")
st.write("Powered by AI • Great for QA/Telecom Coaching")

tab1, tab2 = st.tabs(["By Topic", "From JD"])

with tab1:
    topic = st.text_input("Enter Topic (e.g., OSS/BSS Testing, Postman Automation)")
    if st.button("Generate Questions"):
        if topic:
            with st.spinner("Generating..."):
                questions = generate_questions("Topic", topic)
                st.markdown(questions)

with tab2:
    jd = st.text_area("Paste Job Description here", height=300)
    if st.button("Generate JD-Specific Questions"):
        if jd:
            with st.spinner("Analyzing JD..."):
                questions = generate_questions("JD", jd)
                st.markdown(questions)

st.caption("Tip: Save as PDF or share for coaching sessions!")
