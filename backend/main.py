from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import auth, resume, interview, career, learning
from core.config import settings


app = FastAPI(
    title=settings.app_name,
    description="Backend services for AI-driven learning and career assistance.",
    version="0.1.0",
)

origins = [
    settings.frontend_origin,
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(resume.router, prefix="/api/resume", tags=["resume"])
app.include_router(interview.router, prefix="/api/interview", tags=["interview"])
app.include_router(career.router, prefix="/api/career", tags=["career"])
app.include_router(learning.router, prefix="/api/learning", tags=["learning"])


@app.get("/api/health", tags=["system"])
def health_check() -> dict:
    return {"status": "ok", "service": settings.app_name}
