from fastapi import FastAPI, Depends, HTTPException, status, File, UploadFile
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import uvicorn
from datetime import datetime, timedelta
from typing import Optional
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

from auth import AuthHandler
from models import User, UserCreate, UserLogin, ReportRequest
from database import get_db, create_tables
from pdf_generator import PDFGenerator
from ai_service import AIService

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    create_tables()
    # Create reports directory if it doesn't exist
    os.makedirs("reports", exist_ok=True)
    yield
    # Shutdown (if needed)

app = FastAPI(title="GenAI Report Generator", version="1.0.0", lifespan=lifespan)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React app URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

auth_handler = AuthHandler()
security = HTTPBearer()
pdf_generator = PDFGenerator()
ai_service = AIService()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    user_id = auth_handler.decode_token(token)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    return user_id

@app.post("/auth/signup")
async def signup(user: UserCreate, db=Depends(get_db)):
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Hash password and create user
    hashed_password = auth_handler.get_password_hash(user.password)
    db_user = User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Generate token
    token = auth_handler.encode_token(getattr(db_user, 'id'))
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": db_user.id,
            "email": db_user.email,
            "username": db_user.username
        }
    }

@app.post("/auth/login")
async def login(user: UserLogin, db=Depends(get_db)):
    # Find user by email
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not auth_handler.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    # Generate token
    token = auth_handler.encode_token(getattr(db_user, 'id'))
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": db_user.id,
            "email": db_user.email,
            "username": db_user.username
        }
    }

@app.get("/auth/me")
async def get_current_user_info(user_id: int = Depends(get_current_user), db=Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return {
        "id": user.id,
        "email": user.email,
        "username": user.username
    }

@app.post("/generate-report")
async def generate_report(
    request: ReportRequest,
    user_id: int = Depends(get_current_user),
    db=Depends(get_db)
):
    try:
        # Get user info
        user = db.query(User).filter(User.id == user_id).first()
        
        # Generate AI content
        ai_content = await ai_service.generate_report_content(request.topic)
        
        # Generate PDF
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"report_{user.username}_{timestamp}.pdf"
        file_path = f"reports/{filename}"
        
        pdf_generator.create_report(
            topic=request.topic,
            content=ai_content,
            author=user.username,
            file_path=file_path
        )
        
        return {
            "message": "Report generated successfully",
            "filename": filename,
            "download_url": f"/download/{filename}"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating report: {str(e)}"
        )

@app.get("/download/{filename}")
async def download_report(filename: str, user_id: int = Depends(get_current_user)):
    file_path = f"reports/{filename}"
    
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type='application/pdf'
    )

@app.get("/")
async def root():
    return {"message": "GenAI Report Generator API is running!"}

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {"status": "healthy", "message": "API is running"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 