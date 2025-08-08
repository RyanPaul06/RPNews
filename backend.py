"""
RPNews - Main Backend Server
Coordinates all components and serves the application
"""

import os
import logging
import asyncio
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn

from news_engine import RPNewsEngine
from api_routes import APIRoutes

# Cloud deployment configuration
PORT = int(os.environ.get("PORT", 8000))
DATABASE_URL = os.environ.get("DATABASE_URL", "rpnews.db")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI application
app = FastAPI(title="RPNews - Enhanced AI News Intelligence", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the enhanced news engine and API routes
news_engine = RPNewsEngine(DATABASE_URL)
api_routes = APIRoutes(news_engine)

# Serve static files (frontend)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.on_event("startup")
async def startup_event():
    """Start background tasks when FastAPI starts"""
    logger.info("🚀 Enhanced FastAPI startup - starting background collection")
    news_engine.start_background_collection()

# Root endpoint - serve the main HTML page
@app.get("/")
async def root():
    """Serve the main frontend page"""
    return FileResponse('static/index.html')

# API Endpoints - delegate to APIRoutes class
@app.get("/api/morning-briefing")
async def get_morning_briefing():
    """Generate comprehensive morning briefing with daily overview"""
    return await api_routes.get_morning_briefing()

@app.post("/api/articles/{article_id}/read")
async def mark_article_read(article_id: str):
    """Mark an article as read"""
    return await api_routes.mark_article_read(article_id)

@app.post("/api/articles/{article_id}/star")
async def star_article(article_id: str, request: dict):
    """Star or unstar an article"""
    return await api_routes.star_article(article_id, request)

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
    logger.info("🚀 Starting Enhanced RPNews Platform")
    logger.info(f"🌐 Port: {PORT}")
    logger.info(f"🤖 AI Engine: {news_engine.ai.ai_type}")
    logger.info(f"🎯 AI Model Available: {news_engine.ai.ai_available}")
    logger.info(f"📊 Total Sources: {sum(len(sources) for sources in news_engine.sources.values())}")
    logger.info("✨ Enhanced Features: AI summaries, priority detection, article management")
    logger.info("📂 Serving frontend from: static/")
    
    uvicorn.run(app, host="0.0.0.0", port=PORT)
