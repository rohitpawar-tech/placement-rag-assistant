from fastapi import APIRouter, UploadFile, File, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.core.database import get_db
# CHANGED: Import from models.models
from app.models.models import User, ChatHistory
from app.services.rag_service import rag_service
from app.api.auth import oauth2_scheme

router = APIRouter()

class ChatRequest(BaseModel):
    question: str

@router.post("/query")
def chat_query(
    request: ChatRequest, 
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    user_id = 1 

    response = rag_service.query(request.question)
    
    new_chat = ChatHistory(
        user_id=user_id,
        question=request.question,
        answer=response["answer"],
        source_documents=response["sources"]
    )
    db.add(new_chat)
    db.commit()

    return response