# AI Job Recommender & Chatbot

AI-powered career assistant built with **Streamlit**, **LangChain**, and **Google Gemini API**.  
This app helps job seekers get **personalized job recommendations** based on their CVs (PDF upload) and also provides an **interactive chatbot** for general career-related questions.

---

## Features

- **Upload CV (PDF)** → Extracts your CV content and analyzes it.  
- **Job Recommendations** → Provides top 3 job roles suited to your profile with reasoning.  
- **Skill Analysis** → Highlights strong skills and areas for improvement.  
- **ATS Optimization** → Suggests keywords to improve CV visibility in Applicant Tracking Systems (ATS).  
- **AI Chatbot** → Ask anything about jobs, skills, or career advice.  
- **Customizable Settings** → Choose Gemini model, set temperature, and max output tokens.  

---

## Tech Stack

- [Streamlit](https://streamlit.io/) → Frontend UI  
- [PyMuPDF](https://pymupdf.readthedocs.io/) → Extract text from PDF CV  
- [LangChain](https://www.langchain.com/) → Orchestrates prompts and conversation memory  
- [LangGraph](https://github.com/langchain-ai/langgraph) → React-style agent workflow  
- [Google Gemini API](https://ai.google.dev/) → LLM backend (Gemini 2.5 / 2.0 Flash models)  

---

## Installation

Clone the repo and set up environment:

```bash
git clone https://github.com/yupx20/job-recommendation-chatbot.git
cd job-recommendation-chatbot
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## API Key Setup

This app uses **Google Gemini API**.  

1. Get your API key from [Google AI Studio](https://ai.google.dev/).  
2. Enter it in the sidebar of the app when running:

---

## Usage

Run the app:

```bash
streamlit run job_chatbot.py
```

Open browser at `http://localhost:8501`  

1. Enter your **Google API Key** in the sidebar.  
2. Choose **Gemini model** and adjust parameters (temperature, max tokens).  
3. Upload your **CV (PDF)** → Get job recommendations.  
4. Use the **chat input** at the bottom for Q&A.  

---

## Example Output

After uploading a CV, you’ll get:

- **Professional Summary**: 2–3 sentences describing your profile.  
- **Top 3 Job Roles**: With detailed reasoning why you’re a match.  
- **Skills Analysis**: Strong skills + suggested improvements.  
- **ATS Keywords**: 5–7 suggested keywords to improve visibility.  


## Notes

- Only **PDF CVs** are supported (other formats may cause errors).  
- The **recommendations** are AI-generated and should be cross-verified with career experts.  
- Longer CVs may take more time to process.  

---

## License

MIT License © 2025 Yud

---

## Acknowledgements

- [LangChain](https://www.langchain.com/)  
- [Streamlit](https://streamlit.io/)  
- [Google Gemini API](https://ai.google.dev/)  
- [PyMuPDF](https://pymupdf.readthedocs.io/)  