"""
RPNews - Free News Intelligence Platform
Automatically collects and summarizes news from 60+ sources
Deploy to Railway, Render, or Fly.io for free hosting
"""

import asyncio
import aiohttp
import feedparser
import json
import logging
import sqlite3
import hashlib
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import time
from bs4 import BeautifulSoup
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import uvicorn

# Cloud deployment configuration
PORT = int(os.environ.get("PORT", 8000))
DATABASE_URL = os.environ.get("DATABASE_URL", "rpnews.db")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class NewsArticle:
    id: str
    title: str
    url: str
    source: str
    author: Optional[str]
    published_date: datetime
    content: str
    excerpt: str
    ai_summary: Optional[str]
    category: str
    priority: str
    tags: List[str]
    extracted_at: datetime

class RPNewsAI:
    """Smart rule-based news summarization for RPNews"""
    
    def __init__(self):
        self.ai_type = "enhanced_rules"
        logger.info("📝 Using enhanced rule-based analysis")
    
    def generate_summary(self, title: str, content: str, category: str) -> str:
        """Generate intelligent summary using enhanced rules"""
        return self._smart_rule_summary(title, content, category)
    
    def _smart_rule_summary(self, title: str, content: str, category: str) -> str:
        """Enhanced rule-based summary with intelligent parsing"""
        
        # Extract key sentences using importance indicators
        sentences = content.replace('\n', ' ').split('.')
        important_sentences = []
        
        # Key phrases that indicate important information
        key_indicators = [
            'announces', 'launches', 'reports', 'reveals', 'shows', 'increases', 'decreases',
            'plans', 'expects', 'breakthrough', 'develops', 'creates', 'discovers', 'raises',
            'investment', 'funding', 'regulation', 'policy', 'decision', 'statement'
        ]
        
        for sentence in sentences[:8]:  # Check first 8 sentences
            sentence = sentence.strip()
            if len(sentence) > 25 and any(indicator in sentence.lower() for indicator in key_indicators):
                important_sentences.append(sentence)
        
        # Fallback to first meaningful sentences
        if not important_sentences:
            important_sentences = [s.strip() for s in sentences[:3] if len(s.strip()) > 15]
        
        key_info = '. '.join(important_sentences[:2])
        
        # Category-specific formatting with clean structure
        category_config = {
            "ai": {
                "prefix": "AI Development:", 
                "impact": "Technology Impact: Significant advancement in artificial intelligence sector"
            },
            "finance": {
                "prefix": "Market Update:", 
                "impact": "Financial Impact: Important development affecting markets and investments"
            },
            "politics": {
                "prefix": "Policy Update:", 
                "impact": "Political Impact: Government development with broader implications"
            }
        }
        
        config = category_config.get(category, {
            "prefix": "News Update:", 
            "impact": "General Impact: Important development requiring attention"
        })
        
        return f"{config['prefix']} {title}. Details: {key_info}. {config['impact']}"

class RPNewsEngine:
    """Core news intelligence engine for RPNews"""
    
    def __init__(self, db_path: str = "rpnews.db"):
        self.db_path = db_path
        self.ai = RPNewsAI()
        self.session = None
        self.sources = self._initialize_sources()
        self._setup_database()
        self.background_task = None
        logger.info("📰 RPNews Engine initialized")
    
    def start_background_collection(self):
        """Start background collection task"""
        if self.background_task is None:
            self.background_task = asyncio.create_task(self.background_collection())
            logger.info("🔄 Background collection task started")
    
    def _initialize_sources(self) -> Dict[str, List[Dict]]:
        """Complete source list - 60+ premium sources"""
        return {
            "ai": [
                # TOP TIER - Most Important AI Sources
                {"name": "The Batch (Andrew Ng)", "rss": "https://www.deeplearning.ai/feed/", "priority": "high"},
                {"name": "OpenAI Blog", "rss": "https://openai.com/blog/rss.xml", "priority": "high"},
                {"name": "Anthropic Blog", "rss": "https://www.anthropic.com/news/feed", "priority": "high"},
                {"name": "Google AI Blog", "rss": "https://ai.googleblog.com/feeds/posts/default", "priority": "high"},
                {"name": "DeepMind Blog", "rss": "https://deepmind.com/blog/feed/basic/", "priority": "high"},
                
                # Research Papers
                {"name": "ArXiv AI Papers", "rss": "http://export.arxiv.org/rss/cs.AI", "priority": "high"},
                {"name": "ArXiv ML Papers", "rss": "http://export.arxiv.org/rss/cs.LG", "priority": "high"},
                {"name": "ArXiv Computer Vision", "rss": "http://export.arxiv.org/rss/cs.CV", "priority": "medium"},
                {"name": "ArXiv NLP Papers", "rss": "http://export.arxiv.org/rss/cs.CL", "priority": "medium"},
                
                # Industry News
                {"name": "MIT Technology Review", "rss": "https://www.technologyreview.com/feed/", "priority": "high"},
                {"name": "TechCrunch AI", "rss": "https://techcrunch.com/category/artificial-intelligence/feed/", "priority": "high"},
                {"name": "VentureBeat AI", "rss": "https://venturebeat.com/ai/feed/", "priority": "high"},
                {"name": "The Verge AI", "rss": "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml", "priority": "medium"},
                {"name": "Wired AI", "rss": "https://www.wired.com/feed/tag/ai/latest/rss", "priority": "medium"},
                
                # Specialized AI Publications
                {"name": "AI News", "rss": "https://www.artificialintelligence-news.com/feed/", "priority": "medium"},
                {"name": "Towards Data Science", "rss": "https://towardsdatascience.com/feed", "priority": "medium"},
                {"name": "Machine Learning Mastery", "rss": "https://machinelearningmastery.com/feed/", "priority": "medium"},
                
                # VC & Investment in AI
                {"name": "Andreessen Horowitz", "rss": "https://a16z.com/feed/", "priority": "medium"},
                {"name": "Sequoia Capital", "rss": "https://www.sequoiacap.com/feed/", "priority": "medium"},
                {"name": "First Round Review", "rss": "https://review.firstround.com/feed", "priority": "medium"},
                
                # Meta AI & Others
                {"name": "Meta AI Blog", "rss": "https://ai.facebook.com/blog/feed/", "priority": "medium"}
            ],
            
            "finance": [
                # Major Financial News
                {"name": "Bloomberg Markets", "rss": "https://feeds.bloomberg.com/markets/news.rss", "priority": "high"},
                {"name": "Reuters Business", "rss": "https://feeds.reuters.com/reuters/businessNews", "priority": "high"},
                {"name": "MarketWatch", "rss": "https://feeds.marketwatch.com/marketwatch/topstories/", "priority": "high"},
                {"name": "CNBC Markets", "rss": "https://www.cnbc.com/id/100003114/device/rss/rss.html", "priority": "high"},
                {"name": "Financial Times", "rss": "https://www.ft.com/rss", "priority": "high"},
                {"name": "Wall Street Journal", "rss": "https://feeds.a.dj.com/rss/RSSMarketsMain.xml", "priority": "high"},
                
                # Central Banks & Policy
                {"name": "Federal Reserve", "rss": "https://www.federalreserve.gov/feeds/press_all.xml", "priority": "high"},
                {"name": "The Economist Finance", "rss": "https://www.economist.com/finance-and-economics/rss.xml", "priority": "high"},
                {"name": "Bank of England", "rss": "https://www.bankofengland.co.uk/feeds/news.rss", "priority": "medium"},
                {"name": "European Central Bank", "rss": "https://www.ecb.europa.eu/rss/news.xml", "priority": "medium"},
                
                # Investment & Analysis
                {"name": "Seeking Alpha", "rss": "https://seekingalpha.com/feed.xml", "priority": "medium"},
                {"name": "Morningstar", "rss": "https://www.morningstar.com/rss", "priority": "medium"},
                {"name": "Barron's", "rss": "https://feeds.a.dj.com/rss/RSSLifestyle.xml", "priority": "medium"},
                
                # Cryptocurrency & Fintech
                {"name": "CoinDesk", "rss": "https://feeds.coindesk.com/coindesk-news", "priority": "medium"},
                {"name": "The Block Crypto", "rss": "https://www.theblockcrypto.com/rss.xml", "priority": "medium"},
                {"name": "Fintech News", "rss": "https://fintechnews.org/feed/", "priority": "medium"},
                
                # International Markets
                {"name": "Nikkei Asia Markets", "rss": "https://asia.nikkei.com/rss/feed/Markets", "priority": "medium"}
            ],
            
            "politics": [
                # US Politics - Core
                {"name": "Politico", "rss": "https://www.politico.com/rss/politicopicks.xml", "priority": "high"},
                {"name": "The Hill", "rss": "https://thehill.com/feed/", "priority": "high"},
                {"name": "Washington Post Politics", "rss": "https://feeds.washingtonpost.com/rss/politics", "priority": "high"},
                {"name": "New York Times Politics", "rss": "https://rss.nytimes.com/services/xml/rss/nyt/Politics.xml", "priority": "high"},
                {"name": "CNN Politics", "rss": "http://rss.cnn.com/rss/cnn_allpolitics.rss", "priority": "high"},
                
                # Congressional & Federal
                {"name": "Roll Call", "rss": "https://www.rollcall.com/feed/", "priority": "medium"},
                {"name": "Federal News Network", "rss": "https://federalnewsnetwork.com/feed/", "priority": "medium"},
                
                # International Politics
                {"name": "BBC Politics", "rss": "http://feeds.bbci.co.uk/news/politics/rss.xml", "priority": "high"},
                {"name": "Reuters Politics", "rss": "https://feeds.reuters.com/reuters/politicsNews", "priority": "high"},
                {"name": "Associated Press Politics", "rss": "https://apnews.com/Politics", "priority": "high"},
                
                # European & International
                {"name": "Euronews Politics", "rss": "https://www.euronews.com/rss?format=mrss&level=topic&name=politics", "priority": "medium"},
                {"name": "The Guardian Politics", "rss": "https://www.theguardian.com/politics/rss", "priority": "medium"},
                
                # Analysis & Foreign Policy
                {"name": "Foreign Affairs", "rss": "https://www.foreignaffairs.com/rss.xml", "priority": "medium"},
                {"name": "Foreign Policy", "rss": "https://foreignpolicy.com/feed/", "priority": "medium"},
                {"name": "Atlantic Politics", "rss": "https://www.theatlantic.com/feed/channel/politics/", "priority": "medium"},
                
                # Think Tanks
                {"name": "Brookings Institution", "rss": "https://www.brookings.edu/feed/", "priority": "low"},
                {"name": "American Enterprise Institute", "rss": "https://www.aei.org/feed/", "priority": "low"}
            ]
        }
    
    def _setup_database(self):
        """Setup SQLite database for article storage"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS articles (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    url TEXT UNIQUE NOT NULL,
                    source TEXT NOT NULL,
                    author TEXT,
                    published_date TIMESTAMP,
                    content TEXT,
                    excerpt TEXT,
                    ai_summary TEXT,
                    category TEXT,
                    priority TEXT,
                    tags TEXT,
                    extracted_at TIMESTAMP
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS collection_stats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category TEXT,
                    articles_collected INTEGER,
                    last_run TIMESTAMP,
                    status TEXT
                )
            """)
            
            # Performance indexes
            conn.execute("CREATE INDEX IF NOT EXISTS idx_category ON articles(category)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_published ON articles(published_date)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_priority ON articles(priority)")
    
    async def background_collection(self):
        """Continuous background news collection"""
        await asyncio.sleep(60)  # Wait for startup
        
        while True:
            try:
                logger.info("🔄 Background collection starting...")
                async with aiohttp.ClientSession(
                    timeout=aiohttp.ClientTimeout(total=30),
                    headers={'User-Agent': 'RPNews/1.0 (+https://rpnews.com)'}
                ) as session:
                    self.session = session
                    await self.collect_all_news()
                    self.session = None
                
                # Wait 1 hour before next collection
                logger.info("✅ Background collection complete. Next run in 1 hour.")
                await asyncio.sleep(3600)
                
            except Exception as e:
                logger.error(f"Background collection error: {str(e)}")
                await asyncio.sleep(600)  # Wait 10 minutes on error
    
    async def collect_all_news(self):
        """Collect news from all categories"""
        total_articles = 0
        
        for category in ['ai', 'finance', 'politics']:
            try:
                count = await self.collect_category(category)
                total_articles += count
                
                # Update stats
                with sqlite3.connect(self.db_path) as conn:
                    conn.execute("""
                        INSERT INTO collection_stats 
                        (category, articles_collected, last_run, status)
                        VALUES (?, ?, ?, ?)
                    """, (category, count, datetime.now(), 'success'))
                
            except Exception as e:
                logger.error(f"Error collecting {category}: {str(e)}")
        
        logger.info(f"✅ Total articles collected: {total_articles}")
        return total_articles
    
    async def collect_category(self, category: str) -> int:
        """Collect articles for one category"""
        sources = self.sources.get(category, [])
        total_articles = 0
        
        for source in sources:
            try:
                articles = await self.fetch_rss_feed(source, category)
                for article in articles:
                    self.save_article(article)
                    total_articles += 1
                
                # Rate limiting - be respectful
                await asyncio.sleep(2)
                
            except Exception as e:
                logger.warning(f"Error with {source['name']}: {str(e)}")
                continue
        
        logger.info(f"Collected {total_articles} {category} articles")
        return total_articles
    
    async def fetch_rss_feed(self, source: Dict[str, str], category: str) -> List[NewsArticle]:
        """Fetch and process RSS feed"""
        articles = []
        
        try:
            async with self.session.get(source['rss']) as response:
                if response.status != 200:
                    return articles
                
                content = await response.text()
                feed = feedparser.parse(content)
                
                for entry in feed.entries[:12]:  # Limit per source
                    try:
                        article_id = hashlib.md5(entry.link.encode()).hexdigest()
                        
                        # Skip if already exists
                        if self._article_exists(article_id):
                            continue
                        
                        # Parse published date
                        published_date = datetime.now()
                        if hasattr(entry, 'published_parsed') and entry.published_parsed:
                            published_date = datetime(*entry.published_parsed[:6])
                        
                        # Extract and clean content
                        content = getattr(entry, 'summary', '')
                        if hasattr(entry, 'content'):
                            content = entry.content[0].value if entry.content else content
                        
                        if content:
                            soup = BeautifulSoup(content, 'html.parser')
                            content = soup.get_text().strip()
                        
                        # Generate excerpt and AI summary
                        excerpt = content[:350] + "..." if len(content) > 350 else content
                        ai_summary = self.ai.generate_summary(entry.title, content[:1200], category)
                        
                        # Extract tags
                        tags = self._extract_tags(entry.title, content, category)
                        
                        article = NewsArticle(
                            id=article_id,
                            title=entry.title.strip(),
                            url=entry.link,
                            source=source['name'],
                            author=getattr(entry, 'author', None),
                            published_date=published_date,
                            content=content,
                            excerpt=excerpt,
                            ai_summary=ai_summary,
                            category=category,
                            priority=source['priority'],
                            tags=tags,
                            extracted_at=datetime.now()
                        )
                        
                        articles.append(article)
                        
                    except Exception as e:
                        continue
                        
        except Exception as e:
            logger.error(f"Error fetching {source['name']}: {str(e)}")
        
        return articles
    
    def _article_exists(self, article_id: str) -> bool:
        """Check if article already exists"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT 1 FROM articles WHERE id = ?", (article_id,))
            return cursor.fetchone() is not None
    
    def _extract_tags(self, title: str, content: str, category: str) -> List[str]:
        """Extract relevant tags from content"""
        text = f"{title} {content}".lower()
        tags = []
        
        # Category-specific tag extraction
        if category == "ai":
            ai_terms = {
                'gpt': ['gpt', 'chatgpt'],
                'llm': ['language model', 'llm', 'large language'],
                'ml': ['machine learning', 'deep learning'],
                'startup': ['startup', 'funding', 'investment'],
                'research': ['paper', 'research', 'arxiv', 'study']
            }
            
            for tag, keywords in ai_terms.items():
                if any(keyword in text for keyword in keywords):
                    tags.append(tag)
        
        elif category == "finance":
            finance_terms = {
                'crypto': ['bitcoin', 'cryptocurrency', 'crypto'],
                'stocks': ['stock', 'equity', 'shares'],
                'fed': ['federal reserve', 'fed', 'interest rate'],
                'market': ['market', 'trading']
            }
            
            for tag, keywords in finance_terms.items():
                if any(keyword in text for keyword in keywords):
                    tags.append(tag)
        
        elif category == "politics":
            politics_terms = {
                'congress': ['congress', 'senate', 'house'],
                'election': ['election', 'vote', 'campaign'],
                'policy': ['policy', 'legislation', 'bill']
            }
            
            for tag, keywords in politics_terms.items():
                if any(keyword in text for keyword in keywords):
                    tags.append(tag)
        
        return tags[:6]  # Limit to 6 tags
    
    def save_article(self, article: NewsArticle):
        """Save article to database"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO articles 
                (id, title, url, source, author, published_date, content, excerpt,
                 ai_summary, category, priority, tags, extracted_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                article.id, article.title, article.url, article.source, article.author,
                article.published_date, article.content, article.excerpt, article.ai_summary,
                article.category, article.priority, json.dumps(article.tags), article.extracted_at
            ))

# Initialize FastAPI application
app = FastAPI(title="RPNews - Free News Intelligence Platform", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the news engine
news_engine = RPNewsEngine()

@app.on_event("startup")
async def startup_event():
    """Start background tasks when FastAPI starts"""
    logger.info("🚀 FastAPI startup - starting background collection")
    news_engine.start_background_collection()

# Main professional news dashboard
@app.get("/", response_class=HTMLResponse)
async def dashboard():
    """Professional news intelligence dashboard"""
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RPNews - Professional News Intelligence</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', sans-serif;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            color: #2c3e50;
            line-height: 1.6;
        }
        
        .header {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            border-bottom: 1px solid rgba(0, 0, 0, 0.1);
            position: sticky;
            top: 0;
            z-index: 1000;
            box-shadow: 0 2px 20px rgba(0, 0, 0, 0.1);
        }
        
        .nav-container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 0 20px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            height: 70px;
        }
        
        .logo {
            font-size: 1.8em;
            font-weight: 800;
            background: linear-gradient(45deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .nav-tabs {
            display: flex;
            gap: 0;
            background: rgba(102, 126, 234, 0.1);
            border-radius: 12px;
            padding: 4px;
        }
        
        .nav-tab {
            padding: 12px 24px;
            border: none;
            background: transparent;
            color: #667eea;
            font-weight: 600;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-size: 0.95em;
        }
        
        .nav-tab:hover {
            background: rgba(102, 126, 234, 0.2);
            color: #5a67d8;
        }
        
        .nav-tab.active {
            background: #667eea;
            color: white;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        }
        
        .refresh-btn {
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            border: none;
            padding: 12px 20px;
            border-radius: 10px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .refresh-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 30px 20px;
        }
        
        .briefing-header {
            text-align: center;
            margin-bottom: 40px;
            background: rgba(255, 255, 255, 0.9);
            padding: 30px;
            border-radius: 20px;
            backdrop-filter: blur(10px);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        }
        
        .briefing-title {
            font-size: 2.5em;
            font-weight: 700;
            color: #2c3e50;
            margin-bottom: 10px;
        }
        
        .briefing-date {
            color: #667eea;
            font-size: 1.2em;
            font-weight: 500;
        }
        
        .stats-bar {
            display: flex;
            justify-content: center;
            gap: 30px;
            margin-top: 20px;
            flex-wrap: wrap;
        }
        
        .stat-item {
            text-align: center;
            padding: 10px 20px;
            background: rgba(102, 126, 234, 0.1);
            border-radius: 12px;
        }
        
        .stat-number {
            font-size: 1.5em;
            font-weight: 700;
            color: #667eea;
        }
        
        .stat-label {
            font-size: 0.9em;
            color: #7f8c8d;
        }
        
        .category-section {
            margin-bottom: 50px;
        }
        
        .category-header {
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 25px;
            padding: 20px 30px;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
        }
        
        .category-icon {
            font-size: 1.2em;
            font-weight: 700;
            color: #667eea;
            background: rgba(102, 126, 234, 0.1);
            padding: 8px 12px;
            border-radius: 8px;
            min-width: 40px;
            text-align: center;
        }
        
        .category-title {
            font-size: 1.8em;
            font-weight: 700;
            color: #2c3e50;
        }
        
        .category-count {
            background: #667eea;
            color: white;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: 600;
        }
        
        .articles-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 25px;
        }
        
        .article-card {
            background: white;
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
            border: 1px solid rgba(102, 126, 234, 0.1);
            position: relative;
        }
        
        .article-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(0, 0, 0, 0.15);
        }
        
        .article-header {
            padding: 20px 25px 15px;
            border-bottom: 1px solid #f8f9fa;
        }
        
        .article-meta {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 12px;
        }
        
        .article-source {
            font-weight: 600;
            color: #667eea;
            font-size: 0.9em;
        }
        
        .article-time {
            color: #95a5a6;
            font-size: 0.85em;
            display: flex;
            align-items: center;
            gap: 5px;
        }
        
        .time-icon {
            width: 12px;
            height: 12px;
            border: 1px solid #95a5a6;
            border-radius: 50%;
            position: relative;
        }
        
        .time-icon::after {
            content: '';
            position: absolute;
            top: 2px;
            left: 5px;
            width: 1px;
            height: 4px;
            background: #95a5a6;
        }
        
        .priority-badge {
            position: absolute;
            top: 15px;
            right: 15px;
            padding: 4px 8px;
            border-radius: 6px;
            font-size: 0.75em;
            font-weight: 600;
            text-transform: uppercase;
        }
        
        .priority-high {
            background: #ff6b6b;
            color: white;
        }
        
        .priority-medium {
            background: #feca57;
            color: white;
        }
        
        .priority-low {
            background: #48dbfb;
            color: white;
        }
        
        .article-title {
            font-size: 1.25em;
            font-weight: 700;
            color: #2c3e50;
            line-height: 1.4;
            margin-bottom: 15px;
        }
        
        .article-title a {
            color: inherit;
            text-decoration: none;
            transition: color 0.3s ease;
        }
        
        .article-title a:hover {
            color: #667eea;
        }
        
        .article-content {
            padding: 0 25px 20px;
        }
        
        .article-summary {
            background: linear-gradient(135deg, #f8f9ff, #f0f4ff);
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 15px;
            border-left: 4px solid #667eea;
            font-size: 0.95em;
            line-height: 1.5;
        }
        
        .article-excerpt {
            color: #5d6d7e;
            line-height: 1.6;
            margin-bottom: 15px;
        }
        
        .article-tags {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
        }
        
        .tag {
            background: rgba(102, 126, 234, 0.1);
            color: #667eea;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 0.8em;
            font-weight: 500;
        }
        
        .loading {
            text-align: center;
            padding: 60px 20px;
            color: #7f8c8d;
        }
        
        .loading-spinner {
            width: 50px;
            height: 50px;
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .empty-state {
            text-align: center;
            padding: 60px 20px;
            color: #7f8c8d;
        }
        
        .empty-state-icon {
            font-size: 3em;
            margin-bottom: 20px;
            color: #bdc3c7;
            font-weight: 300;
        }
        
        @media (max-width: 768px) {
            .nav-container {
                flex-direction: column;
                height: auto;
                padding: 15px 20px;
                gap: 15px;
            }
            
            .nav-tabs {
                width: 100%;
                justify-content: center;
            }
            
            .nav-tab {
                flex: 1;
                text-align: center;
                padding: 10px 16px;
                font-size: 0.9em;
            }
            
            .briefing-title {
                font-size: 2em;
            }
            
            .articles-grid {
                grid-template-columns: 1fr;
            }
            
            .stats-bar {
                gap: 15px;
            }
            
            .category-header {
                padding: 15px 20px;
            }
            
            .article-card {
                margin-bottom: 20px;
            }
        }
        
        .fade-in {
            animation: fadeIn 0.6s ease-in;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
    </style>
</head>
<body>
    <header class="header">
        <div class="nav-container">
            <div class="logo">RPNews</div>
            <div class="nav-tabs">
                <button class="nav-tab active" data-view="briefing">Morning Briefing</button>
                <button class="nav-tab" data-view="ai">AI & Technology</button>
                <button class="nav-tab" data-view="finance">Finance & Markets</button>
                <button class="nav-tab" data-view="politics">Politics & Policy</button>
            </div>
            <button class="refresh-btn" onclick="refreshNews()">
                <span id="refresh-icon">↻</span> Refresh
            </button>
        </div>
    </header>

    <div class="container">
        <div id="loading" class="loading">
            <div class="loading-spinner"></div>
            <h3>Loading your news intelligence...</h3>
            <p>Gathering the latest updates from 60+ premium sources</p>
        </div>

        <div id="content" style="display: none;">
            <div class="briefing-header">
                <h1 class="briefing-title">Your Daily Intelligence Briefing</h1>
                <p class="briefing-date" id="briefing-date"></p>
                <div class="stats-bar" id="stats-bar"></div>
            </div>

            <div id="news-content"></div>
        </div>
    </div>

    <script>
        let currentData = null;
        let currentView = 'briefing';

        // Initialize
        document.addEventListener('DOMContentLoaded', function() {
            loadBriefing();
            setupNavigation();
        });

        function setupNavigation() {
            document.querySelectorAll('.nav-tab').forEach(tab => {
                tab.addEventListener('click', function() {
                    // Update active tab
                    document.querySelectorAll('.nav-tab').forEach(t => t.classList.remove('active'));
                    this.classList.add('active');
                    
                    // Switch view
                    currentView = this.dataset.view;
                    if (currentData) {
                        displayContent();
                    }
                });
            });
        }

        async function loadBriefing() {
            try {
                showLoading();
                const response = await fetch('/api/morning-briefing');
                currentData = await response.json();
                displayContent();
            } catch (error) {
                console.error('Error loading briefing:', error);
                showError();
            }
        }

        async function refreshNews() {
            const refreshIcon = document.getElementById('refresh-icon');
            refreshIcon.style.animation = 'spin 1s linear infinite';
            
            try {
                // Trigger collection
                await fetch('/api/collect', { method: 'POST' });
                
                // Wait a moment then reload
                setTimeout(async () => {
                    await loadBriefing();
                    refreshIcon.style.animation = 'none';
                }, 3000);
            } catch (error) {
                console.error('Error refreshing:', error);
                refreshIcon.style.animation = 'none';
            }
        }

        function showLoading() {
            document.getElementById('loading').style.display = 'block';
            document.getElementById('content').style.display = 'none';
        }

        function hideLoading() {
            document.getElementById('loading').style.display = 'none';
            document.getElementById('content').style.display = 'block';
        }

        function showError() {
            hideLoading();
            document.getElementById('news-content').innerHTML = `
                <div class="empty-state">
                    <div class="empty-state-icon">!</div>
                    <h3>Unable to load news</h3>
                    <p>Please try refreshing or check back in a few minutes.</p>
                </div>
            `;
        }

        function displayContent() {
            hideLoading();
            
            if (!currentData || !currentData.briefing) {
                showError();
                return;
            }

            // Update header
            document.getElementById('briefing-date').textContent = currentData.date;
            
            // Update stats
            const statsBar = document.getElementById('stats-bar');
            if (currentView === 'briefing') {
                const totalArticles = currentData.total_articles || 0;
                const aiCount = currentData.briefing.ai?.length || 0;
                const financeCount = currentData.briefing.finance?.length || 0;
                const politicsCount = currentData.briefing.politics?.length || 0;
                
                statsBar.innerHTML = `
                    <div class="stat-item">
                        <div class="stat-number">${totalArticles}</div>
                        <div class="stat-label">Total Articles</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number">${aiCount}</div>
                        <div class="stat-label">AI & Tech</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number">${financeCount}</div>
                        <div class="stat-label">Finance</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number">${politicsCount}</div>
                        <div class="stat-label">Politics</div>
                    </div>
                `;
            } else {
                const categoryData = currentData.briefing[currentView] || [];
                statsBar.innerHTML = `
                    <div class="stat-item">
                        <div class="stat-number">${categoryData.length}</div>
                        <div class="stat-label">Articles Found</div>
                    </div>
                `;
            }

            // Display articles
            const contentDiv = document.getElementById('news-content');
            contentDiv.className = 'fade-in';
            
            if (currentView === 'briefing') {
                contentDiv.innerHTML = displayAllCategories();
            } else {
                contentDiv.innerHTML = displaySingleCategory(currentView);
            }
        }

        function displayAllCategories() {
            let html = '';
            
            const categories = [
                { key: 'ai', title: 'AI & Technology', icon: 'AI' },
                { key: 'finance', title: 'Finance & Markets', icon: 'FIN' },
                { key: 'politics', title: 'Politics & Policy', icon: 'POL' }
            ];

            categories.forEach(category => {
                const articles = currentData.briefing[category.key] || [];
                if (articles.length > 0) {
                    html += `
                        <div class="category-section">
                            <div class="category-header">
                                <span class="category-icon">${category.icon}</span>
                                <h2 class="category-title">${category.title}</h2>
                                <span class="category-count">${articles.length} articles</span>
                            </div>
                            <div class="articles-grid">
                                ${articles.map(article => createArticleCard(article)).join('')}
                            </div>
                        </div>
                    `;
                }
            });

            return html || '<div class="empty-state"><div class="empty-state-icon">∅</div><h3>No articles available</h3><p>Try refreshing to collect the latest news.</p></div>';
        }

        function displaySingleCategory(categoryKey) {
            const articles = currentData.briefing[categoryKey] || [];
            
            if (articles.length === 0) {
                return '<div class="empty-state"><div class="empty-state-icon">∅</div><h3>No articles available</h3><p>Try refreshing to collect the latest news.</p></div>';
            }

            return `
                <div class="articles-grid">
                    ${articles.map(article => createArticleCard(article)).join('')}
                </div>
            `;
        }

        function createArticleCard(article) {
            const tags = article.tags || [];
            const tagsHtml = tags.map(tag => `<span class="tag">${tag}</span>`).join('');
            
            return `
                <article class="article-card">
                    <div class="priority-badge priority-${article.priority || 'medium'}">${article.priority || 'medium'}</div>
                    <div class="article-header">
                        <div class="article-meta">
                            <span class="article-source">${article.source}</span>
                            <span class="article-time"><span class="time-icon"></span> ${article.timeAgo}</span>
                        </div>
                        <h3 class="article-title">
                            <a href="${article.url}" target="_blank" rel="noopener noreferrer">
                                ${article.title}
                            </a>
                        </h3>
                    </div>
                    <div class="article-content">
                        ${article.aiSummary ? `<div class="article-summary">${article.aiSummary}</div>` : ''}
                        <p class="article-excerpt">${article.excerpt}</p>
                        ${tagsHtml ? `<div class="article-tags">${tagsHtml}</div>` : ''}
                    </div>
                </article>
            `;
        }
    </script>
</body>
</html>"""
    return html_content

# API Endpoints
@app.get("/api/morning-briefing")
async def get_morning_briefing():
    """Generate comprehensive morning briefing"""
    try:
        with sqlite3.connect(news_engine.db_path) as conn:
            briefing = {}
            
            for category in ['ai', 'finance', 'politics']:
                cursor = conn.execute("""
                    SELECT id, title, url, source, author, published_date, excerpt,
                           ai_summary, priority, tags
                    FROM articles 
                    WHERE category = ? AND published_date >= datetime('now', '-24 hours')
                    ORDER BY 
                        CASE priority 
                            WHEN 'high' THEN 3 
                            WHEN 'medium' THEN 2 
                            ELSE 1 
                        END DESC,
                        published_date DESC
                    LIMIT 10
                """, (category,))
                
                articles = []
                for row in cursor.fetchall():
                    # Calculate time ago
                    try:
                        pub_date = datetime.fromisoformat(row[5])
                        hours_ago = int((datetime.now() - pub_date).total_seconds() / 3600)
                        time_str = f"{hours_ago}h ago" if hours_ago < 24 else f"{hours_ago//24}d ago"
                    except:
                        time_str = "Recently"
                    
                    articles.append({
                        'id': row[0],
                        'title': row[1],
                        'url': row[2],
                        'source': row[3],
                        'author': row[4] or 'Unknown',
                        'publishedDate': row[5],
                        'excerpt': row[6],
                        'aiSummary': row[7],
                        'priority': row[8],
                        'tags': json.loads(row[9] or '[]'),
                        'category': category,
                        'timeAgo': time_str
                    })
                
                briefing[category] = articles
            
            return {
                'platform': 'RPNews',
                'date': datetime.now().strftime('%B %d, %Y'),
                'briefing': briefing,
                'generated_at': datetime.now().isoformat(),
                'total_articles': sum(len(articles) for articles in briefing.values()),
                'message': 'Your AI-powered morning briefing is ready!'
            }
            
    except Exception as e:
        logger.error(f"Error generating briefing: {str(e)}")
        return {
            'platform': 'RPNews',
            'date': datetime.now().strftime('%B %d, %Y'),
            'briefing': {'ai': [], 'finance': [], 'politics': []},
            'error': 'Briefing generation failed - this may be the first run',
            'generated_at': datetime.now().isoformat(),
            'suggestion': 'Try clicking "Collect Latest News" on the main dashboard'
        }

@app.get("/api/articles/{category}")
async def get_articles(category: str, limit: int = 50, priority: str = "all"):
    """Get articles for a specific category"""
    if category not in ['ai', 'finance', 'politics']:
        raise HTTPException(status_code=400, detail="Category must be ai, finance, or politics")
    
    try:
        with sqlite3.connect(news_engine.db_path) as conn:
            query = """
                SELECT id, title, url, source, author, published_date, excerpt,
                       ai_summary, priority, tags
                FROM articles 
                WHERE category = ?
            """
            params = [category]
            
            if priority != "all":
                query += " AND priority = ?"
                params.append(priority)
            
            query += " ORDER BY published_date DESC LIMIT ?"
            params.append(limit)
            
            cursor = conn.execute(query, params)
            
            articles = []
            for row in cursor.fetchall():
                # Calculate time ago
                try:
                    pub_date = datetime.fromisoformat(row[5])
                    hours_ago = int((datetime.now() - pub_date).total_seconds() / 3600)
                    time_str = f"{hours_ago}h ago" if hours_ago < 24 else f"{hours_ago//24}d ago"
                except:
                    time_str = "Recently"
                
                articles.append({
                    'id': row[0],
                    'title': row[1],
                    'url': row[2],
                    'source': row[3],
                    'author': row[4] or 'Unknown',
                    'publishedDate': row[5],
                    'excerpt': row[6],
                    'aiSummary': row[7],
                    'priority': row[8],
                    'tags': json.loads(row[9] or '[]'),
                    'category': category,
                    'timeAgo': time_str
                })
            
            category_names = {
                'ai': 'AI & Technology',
                'finance': 'Finance & Markets', 
                'politics': 'Politics & Policy'
            }
            
            return {
                'category': category,
                'category_name': category_names[category],
                'articles': articles,
                'count': len(articles),
                'generated_at': datetime.now().isoformat()
            }
            
    except Exception as e:
        logger.error(f"Error getting {category} articles: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get {category} articles")

@app.get("/api/stats")
async def get_stats():
    """Platform statistics and health metrics"""
    try:
        with sqlite3.connect(news_engine.db_path) as conn:
            stats = {}
            
            for category in ['ai', 'finance', 'politics']:
                # Total articles
                cursor = conn.execute("SELECT COUNT(*) FROM articles WHERE category = ?", (category,))
                stats[f'{category}_total'] = cursor.fetchone()[0]
                
                # Today's articles
                cursor = conn.execute("""
                    SELECT COUNT(*) FROM articles 
                    WHERE category = ? AND published_date >= date('now')
                """, (category,))
                stats[f'{category}_today'] = cursor.fetchone()[0]
            
            # Source counts
            stats['sources'] = {
                'ai': len(news_engine.sources['ai']),
                'finance': len(news_engine.sources['finance']),
                'politics': len(news_engine.sources['politics'])
            }
            
            # AI type
            stats['ai_type'] = news_engine.ai.ai_type
            
            return stats
            
    except Exception as e:
        logger.error(f"Error getting stats: {str(e)}")
        return {
            'error': 'Stats temporarily unavailable',
            'ai_type': 'enhanced_rules',
            'sources': {
                'ai': len(news_engine.sources['ai']),
                'finance': len(news_engine.sources['finance']),
                'politics': len(news_engine.sources['politics'])
            },
            'ai_today': 0,
            'finance_today': 0,
            'politics_today': 0
        }

@app.post("/api/collect")
async def trigger_collection(background_tasks: BackgroundTasks):
    """Manually trigger news collection"""
    
    async def run_collection():
        try:
            logger.info("Manual collection triggered")
            async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=30),
                headers={'User-Agent': 'RPNews/1.0'}
            ) as session:
                news_engine.session = session
                total_collected = await news_engine.collect_all_news()
                news_engine.session = None
                logger.info(f"Manual collection completed: {total_collected} articles")
        except Exception as e:
            logger.error(f"Manual collection error: {str(e)}")
    
    background_tasks.add_task(run_collection)
    
    return {
        'message': 'News collection started',
        'timestamp': datetime.now().isoformat(),
        'status': 'Background collection initiated',
        'note': 'Articles will appear in a few minutes'
    }

@app.get("/api/health")
async def health_check():
    """Health check endpoint for deployment platforms"""
    try:
        # Test database connectivity
        with sqlite3.connect(news_engine.db_path) as conn:
            cursor = conn.execute("SELECT COUNT(*) FROM articles")
            article_count = cursor.fetchone()[0]
        
        return {
            'status': 'healthy',
            'platform': 'RPNews',
            'timestamp': datetime.now().isoformat(),
            'ai_type': news_engine.ai.ai_type,
            'article_count': article_count,
            'sources_count': sum(len(sources) for sources in news_engine.sources.values()),
            'database': 'connected'
        }
    except Exception as e:
        return {
            'status': 'unhealthy',
            'platform': 'RPNews', 
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }

if __name__ == "__main__":
    logger.info("🚀 Starting RPNews Platform")
    logger.info(f"🌐 Port: {PORT}")
    logger.info(f"🤖 AI Engine: enhanced_rules")
    logger.info(f"📊 Total Sources: {sum(len(sources) for sources in news_engine.sources.values())}")
    logger.info("📰 Features: Morning briefings, smart summaries, 24/7 collection")
    
    uvicorn.run(app, host="0.0.0.0", port=PORT)
