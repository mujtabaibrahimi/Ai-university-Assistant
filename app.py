import streamlit as st
from pathlib import Path
from brain import UniversityAI

st.set_page_config(page_title="Uni-AI Assistant", layout="wide")
st.title("🎓 University AI Study Assistant")

# Initialize the AI Brain
if "ai" not in st.session_state:
    st.session_state.ai = UniversityAI()

# Sidebar for Uploads
with st.sidebar:
    st.header("Upload Materials")
    uploaded_file = st.file_uploader("Upload Syllabus or Notes (PDF)", type="pdf")
    if uploaded_file:
        try:
            # Ensure data directory exists
            Path("data").mkdir(exist_ok=True)
            file_path = f"data/{uploaded_file.name}"
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            with st.spinner("Processing PDF..."):
                st.session_state.ai.ingest_notes(file_path)
            st.success("✅ Notes Indexed Successfully!")
        except Exception as e:
            st.error(f"❌ Error processing PDF: {str(e)}")

# Main Interaction Area
mode = st.radio("Choose your Assistant Mode:", ["General", "Teacher", "Exam Prep"])
user_query = st.text_input("What would you like to learn today?")

if user_query:
    with st.spinner("Consulting your notes..."):
        response = st.session_state.ai.get_response(user_query, mode=mode)
        st.markdown(f"### Assistant Response ({mode} Mode)")
        st.write(response)

# Auto-Quiz Generator (Bonus Button)
if st.button("Generate a Quiz from my Notes"):
    quiz = st.session_state.ai.get_response("Generate 3 multiple choice questions based on these notes.", mode="General")
    st.info(quiz)