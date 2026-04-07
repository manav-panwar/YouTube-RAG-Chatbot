from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
import re

load_dotenv()

def extract_video_id(url):
    match = re.search(r"(?:v=|youtu\.be/)([0-9A-Za-z_-]{11})", url)
    if match:
        return match.group(1)
    else:
        raise ValueError("Invalid YouTube URL")
    
ytt_api = YouTubeTranscriptApi()

def process_video(url):
    video_id = extract_video_id(url)
    try:
        fetched_transcript = ytt_api.fetch(video_id, languages=['en'])
        transcript = ' '.join(snippet.text for snippet in fetched_transcript)
    except TranscriptsDisabled:
        print('No captions available for this video.')

    # Split
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    docs = splitter.create_documents([transcript])

    # Embeddings
    embeddings = HuggingFaceEndpointEmbeddings(
        repo_id="sentence-transformers/all-MiniLM-L6-v2",
        task="feature-extraction"
    )

    vector_store = FAISS.from_documents(docs, embeddings)

    return vector_store


def ask_question(vector_store, query):
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4}
    )

    docs = retriever.invoke(query)

    context = "\n\n".join([doc.page_content for doc in docs])

    prompt = PromptTemplate(
        template="""
            You are a helpful assistant.
            Answer ONLY from the context below.
            If not found, say "I don't know".

            Context:
            {context}

            Question:
            {question}
            """,
        input_variables=["context", "question"]
    )

    final_prompt = prompt.format(context=context, question=query)

    llm = ChatGoogleGenerativeAI(
        model="gemini-3.1-flash-lite-preview",
        temperature=0.2
    )

    response = llm.invoke(final_prompt)

    return response.content if isinstance(response.content, str) else response.content[0]["text"]