import streamlit as st
import chromadb
from chromadb.utils import embedding_functions
import os
from dotenv import load_dotenv
import PyPDF2
import uuid
import requests

# Load environment variables
load_dotenv()

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# --------- Session State Init ---------
for key in ["show_main", "show_about", "show_config"]:
    if key not in st.session_state:
        st.session_state[key] = False

# --------- CSS ---------
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

    html, body, .stApp {
        font-family: 'Poppins', sans-serif;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        color: #2d3436;
    }

    .main-nav {
        position: fixed;
        top: 0;
        width: 100%;
        background-color: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        display: flex;
        justify-content: center;
        gap: 1rem;
        z-index: 1000;
        padding: 1rem;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
        border-bottom: 1px solid rgba(255, 255, 255, 0.3);
    }

    .main-nav .nav-button {
        font-weight: 600;
        font-size: 1rem;
        padding: 0.6rem 1.5rem;
        border: none;
        border-radius: 12px;
        background: linear-gradient(135deg, #74ebd5 0%, #ACB6E5 100%);
        color: #2d3436;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        cursor: pointer;
    }

    .main-nav .nav-button:hover {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }

    .landing-container {
        margin-top: 100px;
        text-align: center;
        padding: 3rem 1rem;
    }

    .landing-container h1 {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1.5rem;
        line-height: 1.2;
    }

    .landing-container p {
        font-size: 1.25rem;
        color: #636e72;
        max-width: 700px;
        margin: 0 auto 2.5rem;
        line-height: 1.6;
    }

    .start-button {
        font-size: 1.25rem;
        font-weight: 600;
        padding: 1rem 2.5rem;
        border-radius: 12px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
        margin: 1rem auto;
        display: inline-block;
    }

    .start-button:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 12px 30px rgba(102, 126, 234, 0.6);
    }

    @media (max-width: 768px) {
        .landing-container h1 {
            font-size: 2.5rem;
        }

        .landing-container p {
            font-size: 1.1rem;
        }

        .main-nav {
            flex-direction: column;
            gap: 0.5rem;
            padding: 0.75rem;
        }

        .main-nav .nav-button {
            width: 100%;
            text-align: center;
        }
    }
    </style>
""", unsafe_allow_html=True)

# --------- Utils ---------
def _reset_nav():
    st.session_state.show_about = False
    st.session_state.show_config = False
    st.session_state.show_main = False

# --------- Navigation Bar ---------
def nav_bar():
    st.markdown('<div class="main-nav">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🏠 Home", key="nav_home", use_container_width=True):
            _reset_nav()
    with col2:
        if st.button("📘 About", key="nav_about", use_container_width=True):
            _reset_nav()
            st.session_state.show_about = True
    with col3:
        if st.button("⚙️ Model", key="nav_config", use_container_width=True):
            _reset_nav()
            st.session_state.show_config = True
    st.markdown('</div>', unsafe_allow_html=True)

# --------- PDF Processor ---------
class SimplePDFProcessor:
    def __init__(self, chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def read_pdf(self, pdf_file):
        reader = PyPDF2.PdfReader(pdf_file)
        return "\n".join(page.extract_text() for page in reader.pages)

    def create_chunks(self, text, pdf_file):
        chunks = []
        start = 0
        while start < len(text):
            end = start + self.chunk_size
            if start > 0:
                start -= self.chunk_overlap
            chunk = text[start:end]
            if end < len(text):
                last_period = chunk.rfind(".")
                if last_period != -1:
                    chunk = chunk[:last_period + 1]
                    end = start + last_period + 1
            chunks.append({
                "id": str(uuid.uuid4()),
                "text": chunk,
                "metadata": {"source": pdf_file.name},
            })
            start = end
        return chunks

# --------- RAG System ---------
class SimpleRAGSystem:
    def __init__(self, embedding_model="chroma", llm_model="ollama"):
        self.db = chromadb.PersistentClient(path="./chroma_db")
        self.embedding_fn = embedding_functions.DefaultEmbeddingFunction()
        self.collection = self._get_or_create_collection()

    def _get_or_create_collection(self):
        name = "documents_chroma"
        try:
            return self.db.get_collection(name=name, embedding_function=self.embedding_fn)
        except:
            return self.db.create_collection(name=name, embedding_function=self.embedding_fn)

    def add_documents(self, chunks):
        self.collection.add(
            ids=[c["id"] for c in chunks],
            documents=[c["text"] for c in chunks],
            metadatas=[c["metadata"] for c in chunks]
        )

    def query_documents(self, query, n_results=3):
        return self.collection.query(query_texts=[query], n_results=n_results)

    def generate_response(self, query, context):
        prompt = f"Based on the following context, answer the question:\nContext: {context}\nQuestion: {query}\nAnswer:"
        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "llama3.2",
                    "prompt": prompt,
                    "stream": False
                }
            )
            return response.json()["response"]
        except Exception as e:
            st.error(f"Error generating response: {str(e)}")
            return "I couldn't generate a response. Please check if the Ollama server is running."

    def get_embedding_info(self):
        return {
            "name": "Chroma Default",
            "dimensions": 384,
            "model": "chroma",
            "llm": "ollama"
        }

# --------- Pages ---------
def landing_page():
    st.markdown("""
        <div class="landing-container">
            <h1>📘 InsightPDF</h1>
            <p>Transform your PDF documents into interactive knowledge bases. Ask questions and get instant answers powered by AI.</p>
            <div style="margin-top: 3rem;">
    """, unsafe_allow_html=True)

    if st.button("🚀 Start Now", key="start_landing", use_container_width=True, 
                help="Click to start interacting with your PDFs"):
        _reset_nav()
        st.session_state.show_main = True
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

def about_page():
    st.title("📘 About InsightPDF")
    st.markdown("""
    <div style="background: rgba(255,255,255,0.7); padding: 2rem; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
        <p>InsightPDF is an AI-powered Streamlit application designed to transform static PDF documents into dynamic, interactive knowledge bases. It enables users to upload PDF files, ask questions, and receive contextual answers—just like chatting with a subject matter expert.</p>
        <h3>🎯 Aim</h3>
        <p>The primary goal of InsightPDF is to enhance how users interact with documents by making PDF content searchable and conversational using the latest AI techniques.</p>
        <h3>🧠 What It Does</h3>
        <ul>
            <li>📄 Processes PDFs to extract text accurately</li>
            <li>🔍 Chunks and stores content using vector embeddings</li>
            <li>🧠 Embeds text into a vector space using ChromaDB for efficient retrieval</li>
            <li>🤖 Generates answers using a local Ollama LLM (like LLaMA 3) based on queried content</li>
            <li>🧾 Displays source passages to maintain transparency and reference</li>
        </ul>       
        <h3>💡 Why Use InsightPDF?</h3>
        <p>Traditional PDFs are static and hard to navigate. InsightPDF solves this by:</p>
        <ul>
            <li>Providing instant, accurate answers from lengthy documents</li>
            <li>Making document review faster and smarter</li>
            <li>Supporting AI-assisted learning and comprehension</li>
            <li>Offering a private, offline-friendly solution with local LLM and embedding</li>
        </ul>
        <h3>🛠️ Tech Stack</h3>
        <ul>
            <li>Frontend: Streamlit with responsive design & modern UI (custom CSS, animations)</li>
            <li>PDF Parsing: PyPDF2</li>
            <li>Embeddings: ChromaDB with default embedding functions</li>
            <li>LLM: Local Ollama server (e.g., LLaMA 3)</li>
            <li>Data Handling: UUIDs for chunk tracking, session state for multi-page navigation</li>
            <li>Styling: Google Fonts (Poppins), mobile-first responsive CSS</li>
        </ul>
        <h3>🚀 Get Started</h3>
        <p>Upload your PDF and click "Start Now". Ask any question about the document, and get answers backed by AI-powered context understanding. No need to scroll endlessly—InsightPDF does the thinking for you!</p>
    </div>
    """, unsafe_allow_html=True)
    


def config_page():
    st.title("⚙️ Model")
    info = SimpleRAGSystem().get_embedding_info()
    st.markdown(f"""
    <div style="background: rgba(255,255,255,0.7); padding: 2rem; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
        <h3>Embedding :</h3>
        <ul>
            <li>Name: {info['name']}</li>
            <li>Dimensions: {info['dimensions']}</li>
            <li>Model: {info['model']}</li>
        </ul>
        <h3>LLM :</h3>
        <ul>
            <li>Type: {info['llm']}</li>
            <li>Endpoint: Local Ollama server</li>
        </ul>
        <h3>Processing Parameters :</h3>
        <ul>
            <li>Chunk Size: {CHUNK_SIZE} characters</li>
            <li>Chunk Overlap: {CHUNK_OVERLAP} characters</li>
        </ul>
        
        
        
    </div>
    """, unsafe_allow_html=True)

def run_insight_pdf():
    st.title("📄💬 InsightPDF Chat")
    st.markdown("""
    <div style="margin-bottom: 2rem; color: #636e72;">
        Upload your PDF document and ask questions about its content.
    </div>
    """, unsafe_allow_html=True)
    
    if "processed_files" not in st.session_state:
        st.session_state.processed_files = set()
    if "rag_system" not in st.session_state:
        st.session_state.rag_system = SimpleRAGSystem()

    with st.container():
        pdf_file = st.file_uploader("📥 Upload your PDF", type="pdf", 
                                  help="Select a PDF file to analyze")
        if pdf_file and pdf_file.name not in st.session_state.processed_files:
            processor = SimplePDFProcessor()
            with st.spinner("Processing your document..."):
                text = processor.read_pdf(pdf_file)
                chunks = processor.create_chunks(text, pdf_file)
                st.session_state.rag_system.add_documents(chunks)
                st.session_state.processed_files.add(pdf_file.name)
                st.success(f"✅ Processed: {pdf_file.name}")

    if st.session_state.processed_files:
        st.divider()
        query = st.text_input("💬 Ask a question about your document", 
                             placeholder="Type your question here...")
        if query:
            with st.spinner("Analyzing document and generating response..."):
                results = st.session_state.rag_system.query_documents(query)
                context = " ".join(results["documents"][0])
                answer = st.session_state.rag_system.generate_response(query, context)
                
                st.markdown(f"""
                <div style="background: rgba(255,255,255,0.7); padding: 1.5rem; border-radius: 12px; margin-top: 1rem; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
                    <h4 style="margin-top: 0;">Answer</h4>
                    <p>{answer}</p>
                </div>
                """, unsafe_allow_html=True)
                
                with st.expander("📚 View Source Passages", expanded=False):
                    seen = set()
                    for i, doc in enumerate(results["documents"][0]):
                        if doc not in seen:
                            seen.add(doc)
                            st.markdown(f"**Passage {i+1}:**")
                            st.markdown(f"""
                            <div style="background: rgba(255,255,255,0.5); padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
                                {doc}
                            </div>
                            """, unsafe_allow_html=True)


# --------- Main ---------
def main():
    nav_bar()
    if st.session_state.show_about:
        about_page()
    elif st.session_state.show_config:
        config_page()
    elif st.session_state.show_main:
        run_insight_pdf()
    else:
        landing_page()

if __name__ == "__main__":
    main()