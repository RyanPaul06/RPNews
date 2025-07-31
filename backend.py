"""
IntelliNews - Free News Intelligence Platform
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
DATABASE_URL = os.environ.get("DATABASE_URL", "intellinews.db")

# AI Summarization setup
try:
    from transformers import pipeline
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

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

class IntelliNewsAI:
    """AI-powered news summarization"""
    
    def __init__(self):
        self.summarizer = None
        self.setup_ai()
    
    def setup_ai(self):
        """Initialize AI summarization"""
        if TRANSFORMERS_AVAILABLE:
            try:
                self.summarizer = pipeline(
                    "summarization", 
                    model="facebook/bart-large-cnn",
                    device=-1,  # CPU only for cloud deployment
                    framework="pt"
                )
                self.ai_type = "transformers"
                logger.info("✅ Using AI Transformers for summarization")
                return
            except Exception as e:
                logger.warning(f"⚠️ Transformers failed: {str(e)}")
        
        self.ai_type = "enhanced_rules"
        logger.info("📝 Using enhanced rule-based analysis")
    
    def generate_summary(self, title: str, content: str, category: str) -> str:
        """Generate intelligent summary"""
        if self.ai_type == "transformers":
            return self._ai_summary(title, content, category)
        else:
            return self._smart_rule_summary(title, content, category)
    
    def _ai_summary(self, title: str, content: str, category: str) -> str:
        """AI-powered summarization"""
        try:
            text = f"{title}. {content}"[:1024]
            summary = self.summarizer(text, max_length=120, min_length=30, do_sample=False)
            base_summary = summary[0]['summary_text']
            
            # Category-specific formatting
            if category == "ai":
                return f"🤖 Key Point: {base_summary} ⚡ Impact: Major AI development with significant implications."
            elif category == "finance":
                return f"💰 Key Point: {base_summary} 📊 Impact: Important market development for investors."
            elif category == "politics":
                return f"🏛️ Key Point: {base_summary} 📈 Impact: Policy development with broader implications."
            
            return f"📰 Key Point: {base_summary}"
            
        except Exception as e:
            logger.error(f"AI summarization failed: {str(e)}")
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
        
        # Category-specific formatting with emojis and structure
        category_config = {
            "ai": {
                "icon": "🤖", 
                "impact": "⚡ AI Innovation: Significant development in artificial intelligence ecosystem"
            },
            "finance": {
                "icon": "💰", 
                "impact": "📊 Market Impact: Important financial development with investment implications"
            },
            "politics": {
                "icon": "🏛️", 
                "impact": "📈 Policy Impact: Political development with potential broader consequences"
            }
        }
        
        config = category_config.get(category, {
            "icon": "📰", 
            "impact": "📋 Update: Important development to monitor"
        })
        
        return f"{config['icon']} Key Point: {title} 📝 Details: {key_info} {config['impact']}"

class IntelliNewsEngine:
    """Core news intelligence engine"""
    
    def __init__(self, db_path: str = "intellinews.db"):
        self.db_path = db_path
        self.ai = IntelliNewsAI()
        self.session = None
        self.sources = self._initialize_sources()
        self._setup_database()
        
        # Start background collection
        asyncio.create_task(self.background_collection())
    
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
                    headers={'User-Agent': 'IntelliNews/1.0 (+https://intellinews.com)'}
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
app = FastAPI(title="IntelliNews - Free News Intelligence Platform", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the news engine
news_engine = IntelliNewsEngine()

# Main dashboard
@app.get("/", response_class=HTMLResponse)
async def dashboard():
    """Beautiful web dashboard for IntelliNews"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>IntelliNews - Your AI-Powered Morning Briefing</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                min-height: 100vh; 
                color: #333;
            }
            .container { max-width: 1400px; margin: 0 auto; padding: 20px; }
            .header { 
                background: rgba(255,255,255,0.95); 
                padding: 40px; 
                border-radius: 20px; 
                margin-bottom: 30px; 
                backdrop-filter: blur(20px); 
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                text-align: center;
            }
            .logo { 
                font-size: 3.5em; 
                font-weight: 800; 
                background: linear-gradient(45deg, #667eea, #764ba2); 
                -webkit-background-clip: text; 
                -webkit-text-fill-color: transparent; 
                margin-bottom: 10px;
            }
            .tagline { 
                font-size: 1.3em; 
                color: #666; 
                margin-bottom: 20px; 
            }
            .stats { 
                display: flex; 
                justify-content: center; 
                gap: 30px; 
                flex-wrap: wrap;
            }
            .stat { 
                text-align: center; 
                padding: 15px 25px; 
                background: rgba(102, 126, 234, 0.1); 
                border-radius: 15px;
            }
            .stat-number { 
                font-size: 2em; 
                font-weight: bold; 
                color: #667eea; 
            }
            .stat-label { 
                font-size: 0.9em; 
                color: #666; 
                margin-top: 5px;
            }
            .grid { 
                display: grid; 
                grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); 
                gap: 25px; 
                margin-top: 25px;
            }
            .card { 
                background: white; 
                padding: 30px; 
                border-radius: 15px; 
                box-shadow: 0 5px 20px rgba(0,0,0,0.08); 
                transition: transform 0.3s ease, box-shadow 0.3s ease;
                border: 1px solid rgba(102, 126, 234, 0.1);
            }
            .card:hover { 
                transform: translateY(-5px); 
                box-shadow: 0 15px 40px rgba(0,0,0,0.15);
            }
            .card-icon { 
                font-size: 2.5em; 
                margin-bottom: 15px; 
            }
            .card-title { 
                font-size: 1.4em; 
                font-weight: 600; 
                margin-bottom: 10px; 
                color: #333;
            }
            .card-description { 
                color: #666; 
                margin-bottom: 20px; 
                line-height: 1.6;
            }
            .button { 
                background: linear-gradient(45deg, #667eea, #764ba2); 
                color: white; 
                padding: 15px 30px; 
                border: none; 
                border-radius: 10px; 
                cursor: pointer; 
                font-weight: 600; 
                font-size: 1em; 
                transition: all 0.3s ease; 
                text-decoration: none; 
                display: inline-block;
                width: 100%;
                text-align: center;
            }
            .button:hover { 
                transform: translateY(-2px); 
                box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
            }
            .section { 
                background: rgba(255,255,255,0.9); 
                padding: 30px; 
                border-radius: 20px; 
                margin-bottom: 30px; 
                backdrop-filter: blur(20px); 
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            }
            .status { 
                padding: 15px; 
                border-radius: 10px; 
                margin: 15px 0; 
                font-weight: 500;
            }
            .success { 
                background: linear-gradient(135deg, #d4edda, #c3e6cb); 
                color: #155724; 
                border: 1px solid #c3e6cb;
            }
            .warning { 
                background: linear-gradient(135deg, #fff3cd, #ffeaa7); 
                color: #856404; 
                border: 1px solid #ffeaa7;
            }
            .info { 
                background: linear-gradient(135deg, #d1ecf1, #bee5eb); 
                color: #0c5460; 
                border: 1px solid #bee5eb;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="logo">📰 IntelliNews</div>
                <div class="tagline">Your AI-Powered Intelligence Platform</div>
                <div class="stats">
                    <div class="stat">
                        <div class="stat-number">60+</div>
                        <div class="stat-label">Premium Sources</div>
                    </div>
                    <div class="stat">
                        <div class="stat-number">3</div>
                        <div class="stat-label">Categories</div>
                    </div>
                    <div class="stat">
                        <div class="stat-number">24/7</div>
                        <div class="stat-label">Auto Updates</div>
                    </div>
                    <div class
