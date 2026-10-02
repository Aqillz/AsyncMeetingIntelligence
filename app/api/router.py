# app/api/router.py
import os
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from openai import AsyncOpenAI
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Meeting

load_dotenv()
router = APIRouter()

class TranscriptRequest(BaseModel):
    transcript: str

client = AsyncOpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)

@router.post("/generate")
async def generate_minutes(request: TranscriptRequest, db: Session = Depends(get_db)):
    try:
        response = await client.chat.completions.create(
            model=os.getenv("LLM_MODEL"),
            messages=[
                {
                    "role": "system", 
                    "content": "You are an assistant. Extract a bulleted list of action items from this meeting transcript."
                },
                {"role": "user", "content": request.transcript}
            ]
        )
        minutes_result = response.choices[0].message.content
        
        # --- NEW: Save to Database ---
        new_meeting = Meeting(transcript=request.transcript, minutes=minutes_result)
        db.add(new_meeting)
        db.commit()
        db.refresh(new_meeting)
        
        return {"id": new_meeting.id, "minutes": minutes_result}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- NEW: Endpoint to fetch history ---
@router.get("/history")
def get_history(db: Session = Depends(get_db)):
    meetings = db.query(Meeting).order_by(Meeting.created_at.desc()).limit(10).all()
    return meetings