import streamlit as st
from backend import process_video, ask_question

st.set_page_config(page_title="YouTube RAG Chatbot", layout="wide")

st.title("🎥 YouTube RAG Chatbot")

# session state
if "vectordb" not in st.session_state:
    st.session_state.vectordb = None

# Sidebar for processing video
with st.sidebar:
    st.header("📥 Input Video")

    url = st.text_input("Enter YouTube URL").strip()

    if url:
        st.video(url)

    if st.button("Process Video", key="process_btn"):
        if not url:
            st.warning("Please enter a URL")
        else:
            with st.spinner("Processing video..."):
                try:
                    st.session_state.vectordb = process_video(url)
                    st.success("Video processed successfully!")
                except Exception as e:
                    st.error(str(e))

# Chat section
st.subheader("💬 Chat with Video")

query = st.text_input("Ask a question about the video")

if st.button("Ask"):
    if st.session_state.vectordb is None:
        st.error("Please process a video first")
    elif not query:
        st.warning("Enter a question")
    else:
        with st.spinner("Thinking..."):
            answer = ask_question(st.session_state.vectordb, query)

        st.markdown("### Answer:")
        st.write(answer)