"""
RPNews - Main Backend Server (Updated with Article Detail & Chat)
Coordinates all components and serves the application with open source LLMs
"""

import os
import logging
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel

from news_engine import RPNewsEngine
from api_routes import APIRoutes

# Cloud deployment configuration
PORT = int(os.environ.get("PORT", 8000))
DATABASE_URL = os.environ.get("DATABASE_URL", "rpnews.db")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Pydantic model for chat requests
class ChatRequest(BaseModel):
    articleId: str
    message: str
    articleTitle: str
    articleContent: str
    aiSummary: str = None

# Initialize the enhanced news engine and API routes
news_engine = RPNewsEngine(DATABASE_URL)
api_routes = APIRoutes(news_engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("🚀 Enhanced FastAPI startup - starting background collection")
    news_engine.start_background_collection()
    yield
    # Shutdown (if needed)
    pass

# Initialize FastAPI application with lifespan
app = FastAPI(
    title="RPNews - Enhanced AI News Intelligence with Open Source LLMs", 
    version="2.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files (frontend)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Root endpoint - serve the main HTML page
@app.get("/")
async def root():
    """Serve the main frontend page"""
    return FileResponse('static/index.html')

# Article detail page
@app.get("/article")
async def article_detail():
    """Serve the article detail page"""
    try:
        return FileResponse('article-detail.html')
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Article detail page not found")

# API Endpoints - delegate to APIRoutes class
@app.get("/api/morning-briefing")
async def get_morning_briefing():
    """Generate comprehensive morning briefing with daily overview"""
    return await api_routes.get_morning_briefing()

@app.get("/api/articles/detail/{article_id}")
async def get_article_detail(article_id: str):
    """Get detailed article information for the article detail page"""
    return await api_routes.get_article_detail(article_id)

@app.post("/api/articles/chat")
async def chat_about_article(chat_request: ChatRequest):
    """Handle AI chat about a specific article"""
    return await api_routes.chat_about_article(chat_request)

@app.post("/api/articles/{article_id}/read")
async def mark_article_read(article_id: str):
    """Toggle article read status"""
    return await api_routes.mark_article_read(article_id)

@app.post("/api/articles/{article_id}/star")
async def star_article(article_id: str, request: dict):
    """Star or unstar an article"""
    return await api_routes.star_article(article_id, request)

@app.post("/api/articles/{article_id}/pass")
async def pass_article(article_id: str):
    """Pass/dismiss an article"""
    return await api_routes.pass_article(article_id)

@app.get("/api/reading-list")
async def get_reading_list():
    """Get unread articles (reading list)"""
    return await api_routes.get_reading_list()

@app.get("/api/articles/starred")
async def get_starred_articles():
    """Get all starred articles"""
    return await api_routes.get_starred_articles()

@app.get("/api/articles/{category}")
async def get_articles(category: str, limit: int = 50, priority: str = "all"):
    """Get articles for a specific category with enhanced features"""
    return await api_routes.get_articles(category, limit, priority)

@app.get("/api/stats")
async def get_stats():
    """Enhanced platform statistics"""
    return await api_routes.get_stats()

@app.post("/api/collect")
async def trigger_collection(background_tasks: BackgroundTasks):
    """Enhanced manual collection trigger"""
    return await api_routes.trigger_collection(background_tasks)

@app.get("/api/health")
async def health_check():
    """Enhanced health check with AI status"""
    return await api_routes.health_check()

if __name__ == "__main__":
    logger.info("🚀 Starting Enhanced RPNews Platform with Open Source LLMs")
    logger.info(f"🌐 Port: {PORT}")
    logger.info(f"🤖 AI Engine: {news_engine.ai.ai_type}")
    logger.info(f"🎯 AI Available: {news_engine.ai.ai_available}")
    logger.info(f"📊 Total Sources: {sum(len(sources) for sources in news_engine.sources.values())}")
    logger.info("✨ Features: Open source LLM summaries, article management, pass system, AI chat")
    logger.info("📂 Serving frontend from: static/")
    
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)