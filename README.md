_# Streamlit Gemini Model Chatbot

This is a Streamlit web application that provides a chatbot interface for Google's Gemini API. It supports text and multimodal inputs (PDF, image, audio), output copying, and prompt editing.

## Features

- **Gemini API Integration:** Chat with the powerful Gemini models.
- **Multimodal Input:** Attach images, PDFs, and audio files to your prompts.
- **Prompt Editing:** Edit your previous prompts and resubmit them to get a new response.
- **Copy Output:** Easily copy the chatbot's responses.
- **Configurable:** Adjust model, temperature, and max output tokens.

## Setup and Installation

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd streamlit-gemini-chatbot
    ```

2.  **Install dependencies:**

    Make sure you have Python 3.9+ installed. Then, install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up your API Key:**

    -   Get your Gemini API key from [Google AI Studio](https://ai.google.dev/).
    -   Create a `.env` file in the project root by copying the `.env.example` file:

        ```bash
        cp .env.example .env
        ```

    -   Open the `.env` file and add your API key:

        ```
        GEMINI_API_KEY=your_api_key_here
        ```

## How to Run

Once you have completed the setup, you can run the Streamlit application:

```bash
streamlit run app.py
```

The application will be accessible at `http://localhost:8501` in your web browser.

## How to Use

1.  **Configure API Key:** If you haven't set up the `.env` file, you can enter your API key in the sidebar.
2.  **Select Model:** Choose a Gemini model from the dropdown in the sidebar.
3.  **Adjust Parameters:** Set the temperature and max output tokens as needed.
4.  **Chat:** Type your message in the chat input at the bottom of the page.
5.  **Attach Files:** Use the file uploader to attach images, PDFs, or audio files to your message.
6.  **Copy Response:** Click the "Copy" button below an assistant message to copy it to your clipboard.
7.  **Edit Prompt:** Click the "Edit" button below one of your messages to modify it and resend it.
