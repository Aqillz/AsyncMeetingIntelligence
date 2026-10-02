# 📝 Automated Meeting Minutes Engine

This AI-powered app automatically turns your raw meeting transcripts into a clean, organized list of key decisions, deadlines, and action items. 

Under the hood, it uses a background task system. This means even if you upload a massive 2-hour transcript, the web page will never freeze or crash while the AI thinks. It securely saves all your past meetings and lets you download the final notes with a single click.

## ✨ What It Does

* **Fast & Smooth:** Hand off transcripts to the AI without your screen freezing.
* **Automatic Saving:** Every generated summary is saved to a local database so you can view it later in the "History" tab.
* **Export Ready:** Download your action items as a text file instantly.
* **Reliable:** Built to handle API limits and network drops without breaking.

## 🚀 How to Use It

### 1. Set Up Your Environment
First, install the required Python packages:
```bash
pip install -r requirements.txt

2. Add Your API Keys
Create a file named .env in the main folder and add your connection keys (do not share these online):

Plaintext
LLM_PROVIDER=groq
GROQ_API_KEY=your_groq_api_key_here
LLM_MODEL=openai/gpt-oss-120b
REDIS_URL=rediss://default:your_token@your_endpoint.upstash.io:6379?ssl_cert_reqs=CERT_NONE

3. Start the App
Because this app does heavy background processing, you need to open three separate terminal windows and run one command in each:

Terminal 1: Start the API Engine

Bash
uvicorn app.main:app --reload
Terminal 2: Start the Background Worker
(This handles the heavy AI tasks)

Bash
celery -A app.worker worker --pool=solo --loglevel=info
Terminal 3: Start the Web Interface

Bash
streamlit run app/frontend.py

4. Generate Minutes
Once all three are running, open your web browser to the Streamlit link provided in Terminal 3 (usually http://localhost:8501). Paste your meeting transcript into the text box, click Generate Minutes, and download your final text file once the AI finishes.


Once you commit those changes, your GitHub page will immediately update with the proper formatting, bullet points, and code blocks. Let me know how it looks!
