# 🎥 YouTube RAG Chatbot

A Streamlit-based chatbot that allows users to ask questions about YouTube videos using **Retrieval-Augmented Generation (RAG)**.

---

##  Features

*  Extracts transcripts from YouTube videos
*  Semantic search using vector embeddings
*  LLM-powered question answering (Google Gemini)
*  Interactive chat interface
*  Fast retrieval using FAISS
*  Video preview inside the app

---

##  How It Works

1. User provides a YouTube video URL
2. Transcript is extracted using `youtube-transcript-api`
3. Text is split into chunks
4. Chunks are converted into embeddings
5. Stored in a FAISS vector database
6. User query → relevant chunks retrieved
7. LLM generates answer based on context

---

##  Tech Stack

* **Frontend:** Streamlit
* **LLM:** Google Gemini (via LangChain)
* **Embeddings:** HuggingFace (BGE model)
* **Vector Store:** FAISS
* **Backend:** Python

---

##  Installation

```bash
git clone https://github.com/manav-panwar/YouTube-Rag-Chatbot.git
cd YouTube-Rag-Chatbot
pip install -r requirements.txt
```

---

##  Environment Variables

Create a `.env` file:

```env
GOOGLE_API_KEY='your_google_api_key'
HF_TOKEN='your-key'
```

---

##  Run the App

```bash
streamlit run app.py
```

---

##  Future Improvements

* Add timestamp-based source citations
* Multi-video support
* Chat memory
* Streaming responses
* Better reranking for retrieval

---

##  Limitations

* Requires videos with available captions
* Performance depends on transcript quality

