# 📝 Async Meeting Intelligence

An enterprise-grade, asynchronous microservice that leverages Large Language Models (LLMs) to automatically extract key decisions, timelines, and action items from raw meeting transcripts. Engineered for high availability and system stability, this application utilizes a background task queue to handle long-running LLM inference without blocking the main web thread. It demonstrates a highly scalable, fault-tolerant architecture suitable for modern business utility systems.

---

## 🏗️ System Architecture

This project implements a decoupled, multi-tier microservice architecture to cleanly separate the presentation layer, API routing, background processing, and data persistence:

*   **Frontend Interface (Streamlit):** A lightweight, interactive web application that allows users to input transcripts, poll the backend for task status, view historical records, and export generated minutes to `.txt`.
*   **API Gateway (FastAPI):** A high-performance, ASGI-based REST API that validates incoming requests, dispatches background jobs to the queue, and serves historical data.
*   **Asynchronous Task Queue (Celery):** Manages the heavy computational load. LLM generation can take several minutes for extensive transcripts; Celery isolates this workload into background worker processes to prevent HTTP timeouts.
*   **Message Broker (Upstash Redis):** A cloud-hosted Redis instance acting as the message broker and result backend, facilitating communication between the FastAPI router and the Celery workers.
*   **Database & ORM (SQLite + SQLAlchemy):** Provides persistent local storage for original transcripts, generated minutes, and timestamp metadata.
*   **LLM Provider (Groq API):** OpenAI-compatible SDK integration handling the core natural language processing and data extraction.

---

## ✨ Key Technical Features

*   **Non-Blocking I/O:** Utilizes a decoupled request-response cycle. The API returns a `task_id` instantly (HTTP 202 Accepted paradigm) while the background worker processes the transcript.
*   **State Management & Persistence:** All generated minutes are permanently stored and dynamically retrievable via the frontend History tab, ensuring reliable data tracking.
*   **Fault Tolerance:** Celery handles API rate limits, network drops, and retry logic gracefully without crashing the main application.
*   **UI Export:** One-click download generation allowing users to save formatted Markdown/Text files directly to their local machines.

---

## 🚀 Quick Start & Installation

### 1. Set Up Your Environment

Clone the repository and install the required Python packages:

```bash
git clone https://github.com/YOUR_USERNAME/AsyncMeetingIntelligence.git
cd AsyncMeetingIntelligence

# Create and activate the virtual environment
python -m venv venv
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate

pip install -r requirements.txt
```

### 2. Add Your API Keys

Create a file named `.env` in the root directory and add your connection keys:

```env
LLM_PROVIDER=groq
GROQ_API_KEY=your_groq_api_key_here
LLM_MODEL=openai/gpt-oss-120b
REDIS_URL=rediss://default:your_token@your_endpoint.upstash.io:6379?ssl_cert_reqs=CERT_NONE
```

### 3. Start the Microservices

Because this app performs background processing, open **three separate terminal windows** (ensuring the virtual environment is activated in each) and run the following commands:

#### Terminal 1: Start the API Gateway
```bash
uvicorn app.main:app --reload
```

#### Terminal 2: Start the Background Worker
```bash
celery -A app.worker worker --pool=solo --loglevel=info
```

#### Terminal 3: Start the Web Interface
```bash
streamlit run app/frontend.py
```

### 4. Generate Minutes

Once all services are running:
1. Open your web browser and navigate to the Streamlit URL provided in Terminal 3.
2. Paste your meeting transcript into the text box.
3. Click **Generate Minutes**.
4. Download your final structured text file once the AI complete its analysis.
