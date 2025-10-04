import streamlit as st
import google.generativeai as genai
import os
from PIL import Image
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure page
st.set_page_config(
    page_title="Gemini AI Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Title and description
st.title("🤖 Gemini AI Chatbot")
st.markdown("Chat with Google's Gemini AI model with support for text, images, PDFs, and audio files.")

# Sidebar for API key configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # API Key input
    api_key = st.text_input(
        "Enter your Gemini API Key",
        type="password",
        value=os.getenv("GEMINI_API_KEY", ""),
        help="Get your API key from https://ai.google.dev/"
    )
    
    if api_key:
        try:
            genai.configure(api_key=api_key)
            st.success("✅ API Key configured successfully!")
        except Exception as e:
            st.error(f"❌ Error configuring API key: {str(e)}")
    else:
        st.warning("⚠️ Please enter your Gemini API key to continue.")
    
    st.divider()
    
    # Model selection
    st.subheader("Model Selection")
    model_name = st.selectbox(
        "Choose a model",
        ["gemini-2.0-flash-exp", "gemini-1.5-flash", "gemini-1.5-pro"],
        help="Select the Gemini model to use for generation"
    )
    
    st.divider()
    
    # Generation parameters
    st.subheader("Generation Parameters")
    temperature = st.slider("Temperature", 0.0, 2.0, 1.0, 0.1, help="Controls randomness in generation")
    max_tokens = st.slider("Max Output Tokens", 100, 8192, 2048, 100, help="Maximum length of generated response")
    
    st.divider()
    
    # Clear chat button
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.session_state.uploaded_files = []
        st.rerun()

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []

if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = False

if "edit_index" not in st.session_state:
    st.session_state.edit_index = None

# Function to process uploaded files
def process_uploaded_file(uploaded_file):
    """Process different file types and return appropriate content for Gemini API."""
    file_type = uploaded_file.type
    
    if file_type.startswith("image/"):
        # Process image
        image = Image.open(uploaded_file)
        return {"type": "image", "content": image, "name": uploaded_file.name, "file_obj": uploaded_file}
    
    elif file_type == "application/pdf":
        # For PDFs, we'll pass the raw bytes to Gemini (native vision understanding)
        uploaded_file.seek(0)  # Reset file pointer
        pdf_bytes = uploaded_file.read()
        return {"type": "pdf", "content": pdf_bytes, "name": uploaded_file.name, "file_obj": uploaded_file}
    
    elif file_type.startswith("audio/"):
        # For audio files, we'll upload them to Gemini API
        uploaded_file.seek(0)  # Reset file pointer
        return {"type": "audio", "content": uploaded_file, "name": uploaded_file.name, "file_obj": uploaded_file}
    
    else:
        return {"type": "unknown", "content": None, "name": uploaded_file.name, "file_obj": None}

# Function to generate response from Gemini
def generate_response(prompt, files=None):
    """Generate response from Gemini API with optional file inputs."""
    if not api_key:
        return "❌ Please configure your API key in the sidebar."
    
    try:
        # Initialize the model
        model = genai.GenerativeModel(
            model_name=model_name,
            generation_config={
                "temperature": temperature,
                "max_output_tokens": max_tokens,
            }
        )
        
        # Prepare content for the API
        content_parts = []
        
        # Add file contents if available
        if files:
            for file_info in files:
                if file_info["type"] == "image":
                    # Images can be passed directly
                    content_parts.append(file_info["content"])
                    
                elif file_info["type"] == "pdf":
                    # For PDFs, use inline data with Part.from_bytes for small files
                    # or Files API for larger files (>20MB)
                    pdf_size_mb = len(file_info["content"]) / (1024 * 1024)
                    
                    if pdf_size_mb < 15:  # Use inline for files under 15MB to be safe
                        # Create a Part from bytes
                        from google.generativeai.types import content_types
                        pdf_part = content_types.to_part({
                            "inline_data": {
                                "mime_type": "application/pdf",
                                "data": file_info["content"]
                            }
                        })
                        content_parts.append(pdf_part)
                    else:
                        # Use Files API for larger PDFs
                        file_info["file_obj"].seek(0)
                        uploaded_file = genai.upload_file(file_info["file_obj"], mime_type="application/pdf")
                        content_parts.append(uploaded_file)
                        
                elif file_info["type"] == "audio":
                    # Upload audio file to Gemini API using Files API
                    file_info["file_obj"].seek(0)
                    
                    # Determine mime type from file extension or type
                    mime_type = file_info["file_obj"].type
                    uploaded_audio = genai.upload_file(file_info["file_obj"], mime_type=mime_type)
                    content_parts.append(uploaded_audio)
        
        # Add the text prompt
        content_parts.append(prompt)
        
        # Generate response
        response = model.generate_content(content_parts)
        return response.text
    
    except Exception as e:
        return f"❌ Error generating response: {str(e)}"

# Main chat interface
st.subheader("💬 Chat")

# Display chat messages
for idx, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        # Display attached files
        if "files" in message and message["files"]:
            with st.expander(f"📎 Attached files ({len(message['files'])})"):
                for file_info in message["files"]:
                    if file_info["type"] == "image":
                        st.image(file_info["content"], caption=file_info["name"], width=300)
                    else:
                        st.write(f"📄 {file_info['name']} ({file_info['type']})")
        
        # Add copy button and edit button for user messages
        if message["role"] == "user":
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button(f"✏️ Edit", key=f"edit_{idx}"):
                    st.session_state.edit_mode = True
                    st.session_state.edit_index = idx
                    st.rerun()
        
        # Add copy button for assistant messages
        if message["role"] == "assistant":
            col1, col2 = st.columns([1, 10])
            with col1:
                # Display copyable text in an expandable section
                with st.expander("📋 Copy"):
                    st.code(message["content"], language=None)

# File uploader
st.subheader("📎 Attach Files (Optional)")
uploaded_files = st.file_uploader(
    "Upload images, PDFs, or audio files",
    type=["png", "jpg", "jpeg", "gif", "pdf", "mp3", "wav", "m4a"],
    accept_multiple_files=True,
    help="You can attach multiple files to your message"
)

# Process uploaded files
processed_files = []
if uploaded_files:
    for uploaded_file in uploaded_files:
        file_info = process_uploaded_file(uploaded_file)
        processed_files.append(file_info)
        
        # Display preview
        if file_info["type"] == "image":
            st.image(file_info["content"], caption=file_info["name"], width=200)
        else:
            st.write(f"✅ {file_info['name']} ({file_info['type']})")

# Chat input or edit mode
if st.session_state.edit_mode and st.session_state.edit_index is not None:
    # Edit mode
    st.subheader("✏️ Edit Message")
    edited_message = st.session_state.messages[st.session_state.edit_index]
    
    edited_prompt = st.text_area(
        "Edit your message:",
        value=edited_message["content"],
        height=150
    )
    
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("💾 Save and Resend", use_container_width=True):
            if edited_prompt:
                # Remove messages after the edited one
                st.session_state.messages = st.session_state.messages[:st.session_state.edit_index]
                
                # Add edited message
                st.session_state.messages.append({
                    "role": "user",
                    "content": edited_prompt,
                    "files": edited_message.get("files", [])
                })
                
                # Generate new response
                with st.spinner("Generating response..."):
                    response = generate_response(edited_prompt, edited_message.get("files", []))
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response
                    })
                
                # Reset edit mode
                st.session_state.edit_mode = False
                st.session_state.edit_index = None
                st.rerun()
    
    with col2:
        if st.button("❌ Cancel", use_container_width=True):
            st.session_state.edit_mode = False
            st.session_state.edit_index = None
            st.rerun()

else:
    # Normal chat input
    prompt = st.chat_input("Type your message here...")

    if prompt:
        # Add user message to chat
        st.session_state.messages.append({
            "role": "user",
            "content": prompt,
            "files": processed_files
        })
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
            if processed_files:
                with st.expander(f"📎 Attached files ({len(processed_files)})"):
                    for file_info in processed_files:
                        if file_info["type"] == "image":
                            st.image(file_info["content"], caption=file_info["name"], width=300)
                        else:
                            st.write(f"📄 {file_info['name']} ({file_info['type']})")
        
        # Generate and display assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = generate_response(prompt, processed_files)
                st.markdown(response)
        
        # Add assistant message to chat
        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })
        
        st.rerun()

# Footer
st.divider()
st.markdown(
    """
    <div style='text-align: center; color: gray; font-size: 0.8em;'>
    Built with Streamlit and Google Gemini API | 
    <a href='https://ai.google.dev/gemini-api/docs' target='_blank'>API Documentation</a>
    </div>
    """,
    unsafe_allow_html=True
)
