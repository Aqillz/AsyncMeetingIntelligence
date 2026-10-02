# app/worker.py
import os
from celery import Celery
from openai import OpenAI
from dotenv import load_dotenv
from app.database import SessionLocal
from app.models import Meeting

# Load environment variables from your .env file
load_dotenv()

# Fetch the Upstash Redis URL
redis_url = os.getenv("REDIS_URL")

# Initialize Celery with the cloud Redis broker and backend
celery_app = Celery(
    "meeting_tasks",
    broker=redis_url,
    backend=redis_url
)

# Initialize the OpenAI client pointing to Groq
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)

@celery_app.task(name="process_transcript")
def process_transcript_task(transcript: str):
    # 1. Call the LLM
    response = client.chat.completions.create(
        model=os.getenv("LLM_MODEL"),
        messages=[
            {
                "role": "system", 
                "content": "You are an expert executive assistant. Extract the core decisions, key discussion points, and a bulleted list of action items from this meeting transcript."
            },
            {
                "role": "user", 
                "content": transcript
            }
        ]
    )
    minutes_result = response.choices[0].message.content
    
    # 2. Save directly to the Database
    db = SessionLocal()
    try:
        new_meeting = Meeting(transcript=transcript, minutes=minutes_result)
        db.add(new_meeting)
        db.commit()
        db.refresh(new_meeting)
        
        # 3. Return the result to Redis so the frontend can retrieve it
        return {
            "status": "completed", 
            "meeting_id": new_meeting.id, 
            "minutes": minutes_result
        }
    except Exception as e:
        return {
            "status": "failed",
            "error": str(e)
        }
    finally:
        db.close()