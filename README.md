<h1>📘 InsightPDF</h1>

<p><strong>InsightPDF</strong> is a smart, AI-powered web app that lets you upload a PDF document and ask questions about it — just like you're chatting with an expert who read the whole document for you!</p>

<p>No need to search manually or scroll endlessly. Simply upload, ask, and get <strong>instant, meaningful answers</strong>.</p>

<hr>

<h2>🧠 What It Does</h2>

<p>InsightPDF transforms your static PDF files into interactive knowledge bases using Artificial Intelligence.</p>

<p>Here's what it can do:</p>

<ul>
<li>✅ Extracts text from your uploaded PDF</li>
<li>🔍 Breaks it into readable chunks and stores them</li>
<li>📦 Embeds that text into a "smart searchable format" using AI (vector embeddings)</li>
<li>🧠 Uses a local Language Model (LLM) to generate answers to your questions</li>
<li>📄 Shows you the exact passages used to generate each answer</li>
</ul>

<hr>

<h2>🎯 Why Use InsightPDF?</h2>

<ul>
<li>📚 Reading long documents is time-consuming</li>
<li>🤯 It's hard to remember everything inside a large PDF</li>
<li>🔍 Searching manually is annoying and often fails</li>
</ul>

<p>With InsightPDF:</p>

<ul>
<li>⚡ You get quick answers to your document-related questions</li>
<li>💬 You can interact with PDFs like chatting with a smart assistant</li>
<li>🔐 Works locally — no data is sent online</li>
</ul>

<hr>

<h2>🛠️ Tech Stack (Behind the Scenes)</h2>

<table>
<thead>
<tr>
<th>Layer</th>
<th>Technology</th>
</tr>
</thead>
<tbody>
<tr>
<td>Frontend</td>
<td>Streamlit (for UI)</td>
</tr>
<tr>
<td>PDF Reader</td>
<td>PyPDF2</td>
</tr>
<tr>
<td>Embeddings</td>
<td>ChromaDB (Default Embedding)</td>
</tr>
<tr>
<td>Local LLM</td>
<td>Ollama (e.g., LLaMA 3)</td>
</tr>
<tr>
<td>Styling</td>
<td>Google Fonts + Custom CSS</td>
</tr>
<tr>
<td>Storage</td>
<td>Vector Store (Chroma)</td>
</tr>
</tbody>
</table>

<hr>

<h2>🚀 Live Demo Experience (How It Looks)</h2>

<ul>
<li>🏠 <strong>Home Page</strong>: Clean, stylish UI with clear call to action</li>
<li>📘 <strong>About</strong>: Explains everything in plain English</li>
<li>⚙️ <strong>Model Config</strong>: Shows what AI model is being used</li>
<li>💬 <strong>Start</strong>: Upload your PDF and chat with it!</li>
</ul>

<hr>

<h2>🔧 Installation Guide (Step-by-Step)</h2>

<blockquote>
<p>🧑‍💻 You'll need <strong>Python 3.9+</strong>, <strong>pip</strong>, and <strong>Git</strong>. The app also uses <a href="https://ollama.com/">Ollama</a> to run a local LLM (like LLaMA 3).</p>
</blockquote>

<h3>1️⃣ Clone the Repository</h3>

<pre><code class="language-bash">git clone https://github.ibm.com/Sandesh-S-Sanshi/llm-learning.git
cd Rag-Systems
</code></pre>

<h3>2️⃣ Create Virtual Environment (Optional but Recommended)</h3>

<pre><code class="language-bash">python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
</code></pre>

<h3>3️⃣ Install Dependencies</h3>

<pre><code class="language-bash">pip install -r requirements.txt
</code></pre>

<h3>4️⃣ Install and Run Ollama</h3>

<p>Install Ollama and pull the LLaMA model:</p>

<pre><code class="language-bash">ollama pull llama3
</code></pre>

<p>Make sure your Ollama server is running on:</p>

<pre><code>http://localhost:11434
</code></pre>

<h3>5️⃣ Run the App</h3>

<pre><code class="language-bash">streamlit run app.py
</code></pre>

<p>It will open automatically in your browser at:</p>

<pre><code>http://localhost:8501
</code></pre>

<hr>

<h2>📥 How to Use It (For Everyone!)</h2>

<ol>
<li>🏠 Open the app in your browser</li>
<li>📄 Click "Start Now"</li>
<li>📎 Upload a PDF document</li>
<li>💬 Type your question (e.g., "What is this paper about?")</li>
<li>✅ See the answer and related passages from the PDF</li>
</ol>

<hr>

<h2>📁 Project Structure</h2>

<pre><code>Rag-Systems/
│
├── app.py                 → Main Streamlit App
├── requirements.txt       → Python dependencies
├── .env                   → For any environment secrets (optional)
├── chroma_db/             → Local database for embeddings
└── README.md              → You're reading it!
</code></pre>

<hr>

<h2>📌 Sample Use Cases</h2>

<table>
<thead>
<tr>
<th>Field</th>
<th>Use Case</th>
</tr>
</thead>
<tbody>
<tr>
<td>Students</td>
<td>Ask questions on research papers or textbooks</td>
</tr>
<tr>
<td>Lawyers</td>
<td>Understand contracts or legal docs quickly</td>
</tr>
<tr>
<td>HR Professionals</td>
<td>Review company policies efficiently</td>
</tr>
<tr>
<td>Writers/Editors</td>
<td>Explore drafts or manuscripts interactively</td>
</tr>
<tr>
<td>Anyone!</td>
<td>Make any PDF searchable and interactive</td>
</tr>
</tbody>
</table>

<hr>
<h3>Screen Shots : </h3>

![PHOTO-2025-04-10-13-52-29](https://github.com/user-attachments/assets/fbb3bd38-ded9-490c-9095-1a00334a8a1f)


<p>Landing Page </p>
![PHOTO-2025-04-10-14-00-27](https://github.com/user-attachments/assets/82d63768-28b3-4f54-a410-2f77f09d5db7)

<p>About Section</p>


![PHOTO-2025-04-10-14-01-05](https://github.com/user-attachments/assets/48312b55-414d-4655-98a5-ca79d61cece0)

<p>Model Section</p>

![PHOTO-2025-04-10-14-01-14](https://github.com/user-attachments/assets/bce66577-04b6-4207-8f7b-3ef50330442b)

<p>Query Interface</p>






<h2>🙋 Frequently Asked Questions (FAQ)</h2>

<p>❓ <strong>Do I need the internet to use InsightPDF?</strong><br>
➡️ No! Everything runs locally, including the AI model via Ollama.</p>

<p>❓ <strong>What if I upload a huge PDF?</strong><br>
➡️ The app breaks the file into manageable chunks, so even large documents work well.</p>

<p>❓ <strong>Is my data secure?</strong><br>
➡️ Yes. The app runs entirely on your computer, and your files are never uploaded online.</p>

<hr>

<h2>🤝 Contributing</h2>

<p>Feel free to fork the repo, submit issues, or pull requests! Contributions are welcome.</p>

<hr>

<h2>🧑‍💻 Author</h2>

<p>Made with 💙 by <a href="https://github.com/SANDESHSSANSHI">Sandesh S Sanshi</a></p>
