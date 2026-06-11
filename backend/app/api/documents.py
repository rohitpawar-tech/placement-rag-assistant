from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import aiofiles
import os

from app.core.database import get_db
from app.models.models import User, Document
from app.services.rag_service import rag_service
from app.core.config import settings
from app.api.auth import oauth2_scheme

router = APIRouter()

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...), 
    db: AsyncSession = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    # Simple token validation (In prod, decode and verify user)
    # For demo, assume user_id 1
    user_id = 1 

    file_location = f"{settings.UPLOAD_DIR}/{file.filename}"
    
    # Save file
    async with aiofiles.open(file_location, 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)
    
    # Process with RAG
    success = rag_service.ingest_document(file_location, file.filename)
    
    if success:
        # Save Metadata
        new_doc = Document(
            filename=file.filename,
            document_type=file.filename.split('.')[-1],
            uploaded_by=user_id
        )
        db.add(new_doc)
        await db.commit()
        
        return {"info": f"File '{file.filename}' indexed successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to process document")