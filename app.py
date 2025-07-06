                                         #####---------------- AI Resume Scanner ------------------#####
# pip install -r requirements.txt
# python -m spacy download en_core_web_sm

# Step 1: Import Required Libraries

import streamlit as st
from pdfminer.high_level import extract_text
import spacy

# Load English NLP model
nlp = spacy.load("en_core_web_sm")

# Step 2: Function to extract text from uploaded resume PDF
def extract_resume_text(uploaded_file):
    with open("resume.pdf", "wb") as f:
        f.write(uploaded_file.read())
    return extract_text("resume.pdf")

# Step 3: Function to extract skills
def extract_skills(text):
    doc = nlp(text.lower())data analyst with skills like python ,data visualization ,excel ,etc required 
    # stopwords = {"job", "skills", "required", "experience", "like", "with", "and", "etc"} this method give only limited stopwords 
    tokens = [
        token.text for token in doc
        if token.pos_ in ["NOUN", "PROPN"]
        and token.text not in STOP_WORDS # use this for lots of stopwords
        and len(token.text) > 2
        and token.is_alpha  # only alphabetic words, no punctuation/numbers
    ]
    return list(set(tokens))


# Step 4: Function to match resume skills with job description skills
def match_score(resume_skills, jd_skills):
    resume_set = set(resume_skills)
    jd_set = set(jd_skills)
    matched = resume_set & jd_set
    missing = jd_set - resume_set
    score = (len(matched) / len(jd_set)) * 100 if jd_set else 0
    return round(score, 2), matched, missing

# Step 5: Streamlit UI
st.title("🤖 AI Resume Scanner")

# Upload Resume
txt = "Upload your resume in PDF format. We'll extract skills and compare with the job description."
st.markdown(txt)
resume = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

# Paste Job Description
jd_text = st.text_area("Paste Job Description Here")

# Step 6: When both files are provided, process them
if resume and jd_text:
    # Extract text and skills
    resume_text = extract_resume_text(resume)
    res_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)
    
    # Get score and feedback
    score, matched, missing = match_score(res_skills, jd_skills)

    # Display Results
    st.subheader(f"Match Score: {score}%")
    st.success(f"✅ Matched Skills: {', '.join(matched)}")
    st.warning(f"❌ Missing Skills: {', '.join(missing)}")
st.write("App Loaded Successfully!") 

# Run 'streamlit run app.py' in Terminal
