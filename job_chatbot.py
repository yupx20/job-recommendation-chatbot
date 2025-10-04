import streamlit as st
import pymupdf
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage, AIMessage

def extract_text_from_pdf(uploaded_file): # Untuk mengekstrak teks dari PDF
    try:
        pdf_document = pymupdf.open(stream=uploaded_file.getvalue(), filetype="pdf")
        text = ""
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            text += page.get_text()
        pdf_document.close()
        return text
    except Exception as e:
        st.error(f"Error saat membaca file PDF: {e}")
        return None

st.set_page_config(
    page_title="AI Job Recommender",
    page_icon="🤖",
    layout="wide"
)
st.title("🤖 AI Job Recommender & Chatbot")
st.markdown("Unggah CV Anda untuk mendapatkan rekomendasi pekerjaan, atau gunakan chatbot untuk pertanyaan umum.")

with st.sidebar:
    st.header("⚙️ Konfigurasi")
    
    google_api_key = st.text_input(
        "Enter your Gemini API Key", # Input Google API di sidebar
        type="password",
        help="Dapatkan API key Anda dari https://ai.google.dev/"
    )

    st.divider()

    st.subheader("Pemilihan Model")
    model_name = st.selectbox(
        "Pilih model",
        ["gemini-2.5-flash", "gemini-2.0-flash"], # Default model menggunakan gemini-2.5-flash
        key="model_name"
    )

    st.subheader("Parameter Generasi") # Temperature dan max output token dapat disesuaikan sebelum memulai chat
    temperature = st.slider("Temperature", 0.0, 1.0, 0.4, 0.05, key="temperature")
    max_tokens = st.slider("Max Output Tokens", 500, 8192, 2048, 100, key="max_tokens")

    st.divider()
    
    # Upload CV
    st.header("📄 Rekomendasi Pekerjaan")
    uploaded_cv = st.file_uploader(
        "Upload CV Anda (PDF)",
        type=["pdf"],
        accept_multiple_files=False,
        help="Unggah satu file PDF CV Anda untuk dianalisis."
    )

    # Tombol analisis CV untuk rekomendasi pekerjaan
    recommend_button = st.button("Dapatkan Rekomendasi Pekerjaan", use_container_width=True, type="primary")

    st.divider()

    if st.button("🗑️ Hapus Riwayat Obrolan", use_container_width=True):
        st.session_state.pop("agent", None)
        st.session_state.pop("messages", None)
        st.rerun()

agent_settings = {
    "api_key": google_api_key,
    "model": model_name,
    "temp": temperature,
    "max_tokens": max_tokens
}
if "agent" not in st.session_state or st.session_state.get("agent_settings") != agent_settings:
    if google_api_key:
        try:
            llm = ChatGoogleGenerativeAI(
                model=model_name,
                google_api_key=google_api_key,
                temperature=temperature,
                max_output_tokens=max_tokens,
                convert_system_message_to_human=True
            )
            
            st.session_state.agent = create_react_agent(model=llm, tools=[])
            st.session_state.agent_settings = agent_settings
            st.session_state.pop("messages", None) # Hapus history jika agent di-reset
        except Exception as e:
            st.error(f"Error saat inisialisasi: {e}")
            if 'API key' in str(e):
                st.stop()

# Inisialisasi riwayat pesan jika belum ada
if "messages" not in st.session_state:
    st.session_state.messages = []

# Menampilkan semua pesan dalam riwayat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Cek API Key sebelum melanjutkan
if not google_api_key or "agent" not in st.session_state:
    st.info("Harap masukkan Google API Key yang valid di sidebar untuk memulai.", icon="🗝️")
    st.stop()

# Logika untuk Tombol Rekomendasi
if recommend_button:
    if uploaded_cv:
        with st.spinner("Menganalisis CV Anda dan mencari pekerjaan..."):
            cv_text = extract_text_from_pdf(uploaded_cv)
            if cv_text:
                # Prompt rekayasa (prompt engineering) yang sangat penting
                # untuk mendapatkan hasil yang berkualitas tinggi.
                recommendation_prompt = f"""
                Anda adalah seorang perekrut ahli dan penasihat karier dengan pengalaman 15 tahun di pasar kerja Indonesia.
                Tugas Anda adalah menganalisis konten CV berikut secara mendalam.

                **Konten CV:**
                ---
                {cv_text}
                ---

                **Instruksi:**
                Berdasarkan CV di atas, berikan analisis komprehensif dalam format Markdown:
                1.  **Ringkasan Profesional:** Buat ringkasan profil kandidat dalam 2-3 kalimat kuat.
                2.  **Rekomendasi Posisi (Top 3):**
                    * Sebutkan 3 nama posisi pekerjaan spesifik yang paling cocok.
                    * Untuk setiap posisi, jelaskan dalam poin-poin **mengapa** kandidat ini sangat cocok, dengan merujuk langsung pada **pengalaman, skill, atau pendidikan** yang tertera di CV.
                3.  **Analisis Skill & Peluang:**
                    * Sebutkan 3 skill terkuat yang dimiliki kandidat ini.
                    * Sebutkan 1-2 area atau skill yang bisa dikembangkan untuk memperluas peluang kariernya.
                4.  **Saran Kata Kunci untuk CV:** Berikan 5-7 kata kunci (keywords) penting yang harus ditambahkan kandidat ke dalam CV-nya agar lebih mudah ditemukan oleh sistem pelacakan pelamar (ATS) untuk posisi yang direkomendasikan.
                """
                
                try:
                    # Memanggil agent dengan prompt khusus rekomendasi
                    response = st.session_state.agent.invoke(
                        {"messages": [HumanMessage(content=recommendation_prompt)]}
                    )
                    answer = response["messages"][-1].content
                    
                    st.session_state.messages.append({"role": "user", "content": f"Tolong berikan rekomendasi pekerjaan berdasarkan CV ({uploaded_cv.name}) yang saya unggah."})
                    st.session_state.messages.append({"role": "assistant", "content": answer})

                    st.rerun()

                except Exception as e:
                    st.error(f"Gagal mendapatkan rekomendasi: {e}")
            else:
                st.error("Tidak dapat mengekstrak teks dari PDF yang diunggah.")
    else:
        st.warning("Harap unggah file CV (PDF) terlebih dahulu.")

# Logika untuk Chatbot
prompt = st.chat_input("Tanya apa saja...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Konversi history untuk LangChain
    history_for_agent = [AIMessage(content=msg["content"]) if msg["role"] == "assistant" else HumanMessage(content=msg["content"]) for msg in st.session_state.messages]

    # Panggil agent
    try:
        response = st.session_state.agent.invoke({"messages": history_for_agent})
        answer = response["messages"][-1].content
        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.rerun() # Rerun untuk menampilkan pesan baru
    except Exception as e:
        st.session_state.messages.append({"role": "assistant", "content": f"Maaf, terjadi error: {e}"})
        st.rerun()