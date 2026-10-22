import streamlit as st
import google.generativeai as genai
import os

# Page Configuration
st.set_page_config(
    page_title="Smart Study & Quiz Generator",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Smart Study & Quiz Generator")
st.write("Transform your study notes into structured summary bullets, interactive flashcards, and a practice quiz in seconds!")

# Sidebar Configuration
st.sidebar.header("⚙️ Configuration")
api_key = st.sidebar.text_input("Enter your Gemini API Key:", type="password")

if not api_key:
    api_key = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY", "")

if api_key:
    genai.configure(api_key=api_key)

# Input Section
st.subheader("📝 Enter Study Notes")
study_material = st.text_area(
    "Paste your notes, textbook text, or lecture summary below:",
    height=200,
    placeholder="Paste your study content here (e.g., notes on Photosynthesis, World War II history, Machine Learning basics)..."
)

uploaded_file = st.file_uploader("Or upload a text file (.txt):", type=["txt"])
if uploaded_file is not None:
    study_material = uploaded_file.read().decode("utf-8")
    st.info("Loaded text from uploaded file.")

num_questions = st.sidebar.slider("Number of Quiz Questions", min_value=3, max_value=10, value=5)
num_flashcards = st.sidebar.slider("Number of Flashcards", min_value=3, max_value=10, value=5)

# Process Notes Button
if st.button("Generate Study Materials", type="primary"):
    if not api_key:
        st.error("Please provide your Gemini API Key in the sidebar or via Streamlit secrets.")
    elif not study_material.strip():
        st.warning("Please paste or upload some study text before generating materials.")
    else:
        with st.spinner("Analyzing study notes with Gemini 2.5 Flash..."):
            try:
                model = genai.GenerativeModel("gemini-2.5-flash")

                prompt = f"""
                You are an expert tutor and educational designer. 
                Based on the study material provided below, generate a complete set of study materials.

                STUDY MATERIAL:
                \"\"\"{study_material}\"\"\"

                Provide your response in Markdown using the following exact structure:

                ## 📌 Key Summary Bullets
                * Highlighting 5-7 core takeaways, concepts, and key facts.

                ## 🪪 Flashcards
                Generate exactly {num_flashcards} flashcards in this format:
                * **Card 1 | Front:** [Question or Concept]
                  * **Back:** [Answer or Definition]

                ## ❓ Multiple-Choice Quiz
                Generate exactly {num_questions} multiple-choice questions with options (A, B, C, D) and an expandable answer key at the bottom.
                Format each question like this:
                1. **[Question]**
                   - A) [Option]
                   - B) [Option]
                   - C) [Option]
                   - D) [Option]

                <details>
                <summary><b>Click to View Answer Key</b></summary>

                1. **Correct Option:** [Option Letter & Explanation]
                </details>
                """

                response = model.generate_content(prompt)

                st.success("Study kit generated successfully!")
                st.markdown("---")
                st.markdown(response.text)

            except Exception as e:
                st.error(f"An error occurred: {e}")
