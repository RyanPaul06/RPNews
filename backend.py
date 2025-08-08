"""
RPNews - Complete AI-Powered News Intelligence Platform
Full frontend included with all UI components
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
import re
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
    reading_time: int
    extracted_at: datetime

class RPNewsAI:
    """Enhanced AI news analysis with proper summarization"""
    
    def __init__(self):
        self.ai_type = "enhanced_rules"
        self.ai_available = False
        logger.info("🤖 Initializing AI analysis system...")
        self.summarizer = None
    
    def generate_summary(self, title: str, content: str, category: str) -> str:
        """Generate intelligent summary using enhanced rules"""
        return self._smart_rule_summary(title, content, category)
    
    def _smart_rule_summary(self, title: str, content: str, category: str) -> str:
        """Enhanced rule-based summary with intelligent parsing"""
        
        # Extract key sentences using importance indicators
        sentences = content.replace('\n', ' ').split('.')
        important_sentences = []
        
        # Enhanced key phrases by category
        key_indicators = {
            'ai': ['announces', 'launches', 'breakthrough', 'develops', 'ai', 'model', 'algorithm', 'machine learning', 'neural', 'artificial intelligence', 'released', 'update'],
            'finance': ['reports', 'earnings', 'revenue', 'profit', 'investment', 'funding', 'market', 'stock', 'financial', 'economic', 'fed', 'rate', 'inflation', 'growth'],
            'politics': ['policy', 'legislation', 'congress', 'senate', 'president', 'governor', 'election', 'vote', 'political', 'government', 'bill', 'law']
        }
        
        category_indicators = key_indicators.get(category, [
            'announces', 'launches', 'reports', 'reveals', 'shows', 'increases', 'decreases',
            'plans', 'expects', 'breakthrough', 'develops', 'creates', 'discovers'
        ])
        
        for sentence in sentences[:10]:  # Check first 10 sentences
            sentence = sentence.strip()
            if len(sentence) > 30:
                # Score sentence based on keywords and position
                score = 0
                sentence_lower = sentence.lower()
                
                for indicator in category_indicators:
                    if indicator in sentence_lower:
                        score += 2
                
                # Boost for numbers, percentages, quotes
                if re.search(r'\d+%|\$\d+|"\w+', sentence):
                    score += 1
                
                if score >= 2:
                    important_sentences.append(sentence)
        
        # Fallback to first meaningful sentences
        if not important_sentences:
            important_sentences = [s.strip() for s in sentences[:3] if len(s.strip()) > 20]
        
        # Create summary from top 2 sentences
        key_info = '. '.join(important_sentences[:2])
        
        # Category-specific formatting
        category_config = {
            "ai": "🤖 AI Development",
            "finance": "💰 Market Update",
            "politics": "🏛️ Policy Update"
        }
        
        prefix = category_config.get(category, "📰 News Update")
        
        return f"{prefix}: {key_info}."
    
    def generate_daily_overview(self, articles_by_category: Dict[str, List]) -> str:
        """Generate comprehensive daily overview"""
        overview_parts = []
        
        category_summaries = {
            'ai': "📱 Technology developments",
            'finance': "💰 Market movements", 
            'politics': "🏛️ Policy updates"
        }
        
        for category, articles in articles_by_category.items():
            if not articles:
                continue
                
            high_priority_count = len([a for a in articles if a.get('priority') == 'high'])
            total_count = len(articles)
            
            category_name = category_summaries.get(category, f"{category} updates")
            
            if high_priority_count > 0:
                overview_parts.append(f"{category_name}: {high_priority_count} major developments, {total_count} total articles")
            else:
                overview_parts.append(f"{category_name}: {total_count} articles to review")
        
        if not overview_parts:
            return "📰 Your daily briefing is being prepared. Fresh articles are being collected automatically."
        
        overview = "🌅 Today's Intelligence Overview: " + "; ".join(overview_parts)
        overview += f". Total articles for review: {sum(len(articles) for articles in articles_by_category.values())}."
        
        return overview

class RPNewsEngine:
    """Enhanced news intelligence engine with working RSS feeds"""
    
    def __init__(self, db_path: str = "rpnews.db"):
        self.db_path = db_path
        self.ai = RPNewsAI()
        self.session = None
        self.sources = self._initialize_sources()
        self._setup_database()
        self.background_task = None
        self.is_collecting = False
        logger.info("📰 Enhanced RPNews Engine initialized")
    
    def start_background_collection(self):
        """Start background collection task"""
        if self.background_task is None:
            self.background_task = asyncio.create_task(self.background_collection())
            logger.info("🔄 Background collection task started")
    
    def _initialize_sources(self) -> Dict[str, List[Dict]]:
        """Working RSS feeds - tested and verified"""
        return {
            "ai": [
                # Technology News
                {"name": "TechCrunch", "rss": "https://techcrunch.com/feed/", "priority": "high"},
                {"name": "The Verge", "rss": "https://www.theverge.com/rss/index.xml", "priority": "high"},
                {"name": "Ars Technica", "rss": "https://feeds.arstechnica.com/arstechnica/index", "priority": "high"},
                {"name": "MIT Technology Review", "rss": "https://www.technologyreview.com/feed/", "priority": "high"},
                {"name": "Wired", "rss": "https://www.wired.com/feed/rss", "priority": "medium"},
                {"name": "VentureBeat", "rss": "https://venturebeat.com/feed/", "priority": "medium"},
                {"name": "ZDNet", "rss": "https://www.zdnet.com/news/rss.xml", "priority": "medium"},
                {"name": "TechNews", "rss": "https://www.technewsworld.com/feed/", "priority": "medium"},
                {"name": "AI News", "rss": "https://www.artificialintelligence-news.com/feed/", "priority": "medium"},
                {"name": "Next Web", "rss": "https://thenextweb.com/feed/", "priority": "medium"},
                {"name": "Tech Republic", "rss": "https://www.techrepublic.com/rssfeeds/articles/", "priority": "low"},
                {"name": "Engadget", "rss": "https://www.engadget.com/rss.xml", "priority": "medium"},
                # Research & Papers
                {"name": "ArXiv CS", "rss": "http://export.arxiv.org/rss/cs", "priority": "medium"},
                {"name": "Google AI Blog", "rss": "https://ai.googleblog.com/feeds/posts/default", "priority": "high"}
            ],
            
            "finance": [
                # Major Financial News
                {"name": "Reuters Business", "rss": "https://feeds.reuters.com/reuters/businessNews", "priority": "high"},
                {"name": "MarketWatch", "rss": "https://feeds.marketwatch.com/marketwatch/topstories/", "priority": "high"},
                {"name": "Yahoo Finance", "rss": "https://feeds.finance.yahoo.com/rss/2.0/headline", "priority": "high"},
                {"name": "Financial Times", "rss": "https://www.ft.com/rss", "priority": "high"},
                {"name": "Bloomberg", "rss": "https://feeds.bloomberg.com/markets/news.rss", "priority": "high"},
                {"name": "CNBC", "rss": "https://www.cnbc.com/id/100003114/device/rss/rss.html", "priority": "high"},
                {"name": "Seeking Alpha", "rss": "https://seekingalpha.com/feed.xml", "priority": "medium"},
                {"name": "Investor's Business Daily", "rss": "https://www.investors.com/feed/", "priority": "medium"},
                {"name": "The Motley Fool", "rss": "https://www.fool.com/a/feeds/nasdaq-articles/", "priority": "medium"},
                # Crypto & Fintech
                {"name": "CoinDesk", "rss": "https://feeds.coindesk.com/coindesk-news", "priority": "medium"},
                {"name": "CoinTelegraph", "rss": "https://cointelegraph.com/rss", "priority": "medium"},
                # Economic News
                {"name": "Federal Reserve", "rss": "https://www.federalreserve.gov/feeds/press_all.xml", "priority": "high"},
                {"name": "The Economist", "rss": "https://www.economist.com/finance-and-economics/rss.xml", "priority": "medium"}
            ],
            
            "politics": [
                # US Politics
                {"name": "Politico", "rss": "https://www.politico.com/rss/politicopicks.xml", "priority": "high"},
                {"name": "Reuters Politics", "rss": "https://feeds.reuters.com/reuters/politicsNews", "priority": "high"},
                {"name": "The Hill", "rss": "https://thehill.com/feed/", "priority": "high"},
                {"name": "CNN Politics", "rss": "http://rss.cnn.com/rss/cnn_allpolitics.rss", "priority": "high"},
                {"name": "Associated Press", "rss": "https://feeds.apnews.com/rss/apf-politics.rss", "priority": "high"},
                {"name": "NPR Politics", "rss": "https://feeds.npr.org/1014/feed.json", "priority": "medium"},
                # International Politics  
                {"name": "BBC News", "rss": "http://feeds.bbci.co.uk/news/politics/rss.xml", "priority": "high"},
                {"name": "The Guardian Politics", "rss": "https://www.theguardian.com/politics/rss", "priority": "medium"},
                {"name": "Washington Post", "rss": "https://feeds.washingtonpost.com/rss/politics", "priority": "high"},
                {"name": "New York Times", "rss": "https://rss.nytimes.com/services/xml/rss/nyt/Politics.xml", "priority": "high"},
                # Analysis
                {"name": "Foreign Affairs", "rss": "https://www.foreignaffairs.com/rss.xml", "priority": "medium"},
                {"name": "Foreign Policy", "rss": "https://foreignpolicy.com/feed/", "priority": "medium"},
                {"name": "Roll Call", "rss": "https://www.rollcall.com/feed/", "priority": "medium"}
            ]
        }
    
    def _setup_database(self):
        """Setup enhanced SQLite database"""
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
                    reading_time INTEGER DEFAULT 0,
                    extracted_at TIMESTAMP,
                    is_read BOOLEAN DEFAULT FALSE,
                    is_starred BOOLEAN DEFAULT FALSE,
                    read_at TIMESTAMP,
                    starred_at TIMESTAMP
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
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS daily_overviews (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT UNIQUE,
                    overview_text TEXT,
                    total_articles INTEGER,
                    high_priority_count INTEGER,
                    generated_at TIMESTAMP
                )
            """)
            
            # Performance indexes
            conn.execute("CREATE INDEX IF NOT EXISTS idx_category ON articles(category)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_published ON articles(published_date)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_priority ON articles(priority)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_read_starred ON articles(is_read, is_starred)")
    
    def _calculate_priority(self, title: str, content: str, source_priority: str, category: str) -> str:
        """Enhanced priority detection based on content analysis"""
        priority_score = 0
        text = f"{title} {content}".lower()
        
        # Base score from source priority
        priority_base = {"high": 3, "medium": 2, "low": 1}
        priority_score = priority_base.get(source_priority, 2)
        
        # Category-specific high-priority indicators
        high_priority_terms = {
            'ai': [
                'breakthrough', 'released', 'announces', 'launches', 'gpt', 'claude',
                'funding', 'acquisition', 'partnership', 'regulation', 'banned',
                'agi', 'openai', 'google', 'microsoft', 'billion', 'million'
            ],
            'finance': [
                'fed decision', 'interest rate', 'inflation', 'recession', 'crash',
                'bank failure', 'earnings beat', 'guidance', 'outlook', 'upgraded',
                'downgraded', 'merger', 'acquisition', 'ipo', 'bankruptcy'
            ],
            'politics': [
                'breaking', 'urgent', 'senate votes', 'house passes', 'president',
                'supreme court', 'indictment', 'investigation', 'scandal',
                'election', 'poll', 'debate', 'resignation', 'appointed'
            ]
        }
        
        category_terms = high_priority_terms.get(category, [])
        
        # Count high-priority term matches
        term_matches = sum(1 for term in category_terms if term in text)
        priority_score += min(term_matches * 0.5, 2)  # Max 2 bonus points
        
        # Boost for numbers/percentages (usually important data)
        if re.search(r'\d+%|\$\d+\.?\d*[bmk]|\d+\.\d+%', text):
            priority_score += 0.5
        
        # Boost for urgency words
        urgency_terms = ['breaking', 'urgent', 'just in', 'developing', 'alert']
        if any(term in text for term in urgency_terms):
            priority_score += 1
        
        # Determine final priority
        if priority_score >= 4:
            return "high"
        elif priority_score >= 2.5:
            return "medium"
        else:
            return "low"
    
    def _calculate_reading_time(self, content: str) -> int:
        """Calculate estimated reading time in minutes"""
        words = len(content.split())
        # Average reading speed: 200 words per minute
        minutes = max(1, round(words / 200))
        return min(minutes, 15)  # Cap at 15 minutes
    
    async def background_collection(self):
        """Continuous background collection - every 30 minutes"""
        logger.info("🚀 Starting continuous news collection...")
        
        # Initial collection on startup
        await self._run_collection_cycle()
        
        # Continue with regular collection cycle
        while True:
            try:
                await asyncio.sleep(1800)  # Wait 30 minutes (more frequent updates)
                await self._run_collection_cycle()
                
            except Exception as e:
                logger.error(f"Background collection error: {str(e)}")
                await asyncio.sleep(300)  # Wait 5 minutes on error
    
    async def _run_collection_cycle(self):
        """Run a single collection cycle"""
        if self.is_collecting:
            logger.info("Collection already in progress, skipping...")
            return
            
        self.is_collecting = True
        logger.info("🔄 Starting collection cycle...")
        
        try:
            async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=45),
                headers={'User-Agent': 'RPNews/2.0 News Aggregator'}
            ) as session:
                self.session = session
                total_new = await self.collect_all_news()
                self.session = None
                
            logger.info(f"✅ Collection cycle complete: {total_new} new articles")
            
        except Exception as e:
            logger.error(f"Collection cycle error: {e}")
        finally:
            self.is_collecting = False
    
    async def collect_all_news(self):
        """Enhanced news collection with better error handling"""
        total_new_articles = 0
        
        for category in ['ai', 'finance', 'politics']:
            try:
                count = await self.collect_category(category)
                total_new_articles += count
                
                # Update stats
                with sqlite3.connect(self.db_path) as conn:
                    conn.execute("""
                        INSERT INTO collection_stats 
                        (category, articles_collected, last_run, status)
                        VALUES (?, ?, ?, ?)
                    """, (category, count, datetime.now(), 'success'))
                
                logger.info(f"✅ {category}: {count} new articles")
                
            except Exception as e:
                logger.error(f"Error collecting {category}: {str(e)}")
                
                # Record error in stats
                with sqlite3.connect(self.db_path) as conn:
                    conn.execute("""
                        INSERT INTO collection_stats 
                        (category, articles_collected, last_run, status)
                        VALUES (?, ?, ?, ?)
                    """, (category, 0, datetime.now(), f'error: {str(e)[:100]}'))
        
        # Generate daily overview after collection
        await self._generate_daily_overview()
        
        return total_new_articles
    
    async def _generate_daily_overview(self):
        """Generate and store daily overview"""
        today = datetime.now().strftime('%Y-%m-%d')
        
        try:
            # Get today's articles by category
            articles_by_category = {}
            
            with sqlite3.connect(self.db_path) as conn:
                for category in ['ai', 'finance', 'politics']:
                    cursor = conn.execute("""
                        SELECT title, ai_summary, priority FROM articles 
                        WHERE category = ? AND date(published_date) = date('now')
                        ORDER BY 
                            CASE priority 
                                WHEN 'high' THEN 3 
                                WHEN 'medium' THEN 2 
                                ELSE 1 
                            END DESC
                        LIMIT 10
                    """, (category,))
                    
                    articles = []
                    for row in cursor.fetchall():
                        articles.append({
                            'title': row[0],
                            'aiSummary': row[1],
                            'priority': row[2]
                        })
                    
                    articles_by_category[category] = articles
                
                # Generate overview
                overview_text = self.ai.generate_daily_overview(articles_by_category)
                
                total_articles = sum(len(articles) for articles in articles_by_category.values())
                high_priority_count = sum(
                    len([a for a in articles if a.get('priority') == 'high']) 
                    for articles in articles_by_category.values()
                )
                
                # Store overview
                conn.execute("""
                    INSERT OR REPLACE INTO daily_overviews 
                    (date, overview_text, total_articles, high_priority_count, generated_at)
                    VALUES (?, ?, ?, ?, ?)
                """, (today, overview_text, total_articles, high_priority_count, datetime.now()))
                
        except Exception as e:
            logger.error(f"Error generating daily overview: {e}")
    
    async def collect_category(self, category: str) -> int:
        """Enhanced category collection with better error handling"""
        sources = self.sources.get(category, [])
        new_articles = 0
        
        for source in sources:
            try:
                articles = await self.fetch_rss_feed(source, category)
                for article in articles:
                    if self.save_article(article):
                        new_articles += 1
                
                # Rate limiting - be respectful
                await asyncio.sleep(2)
                
            except Exception as e:
                logger.warning(f"Error with {source['name']}: {str(e)}")
                continue
        
        return new_articles
    
    async def fetch_rss_feed(self, source: Dict[str, str], category: str) -> List[NewsArticle]:
        """Enhanced RSS feed processing with better error handling"""
        articles = []
        
        try:
            # Set a reasonable timeout
            async with self.session.get(source['rss'], timeout=30) as response:
                if response.status != 200:
                    logger.warning(f"HTTP {response.status} for {source['name']}")
                    return articles
                
                content = await response.text()
                feed = feedparser.parse(content)
                
                if not hasattr(feed, 'entries') or not feed.entries:
                    logger.warning(f"No entries found for {source['name']}")
                    return articles
                
                for entry in feed.entries[:10]:  # Limit per source
                    try:
                        # Skip if no link
                        if not hasattr(entry, 'link') or not entry.link:
                            continue
                            
                        article_id = hashlib.md5(entry.link.encode()).hexdigest()
                        
                        # Skip if already exists
                        if self._article_exists(article_id):
                            continue
                        
                        # Parse published date
                        published_date = datetime.now()
                        if hasattr(entry, 'published_parsed') and entry.published_parsed:
                            try:
                                published_date = datetime(*entry.published_parsed[:6])
                            except:
                                pass
                        
                        # Skip very old articles (more than 7 days)
                        if (datetime.now() - published_date).days > 7:
                            continue
                        
                        # Extract and clean content
                        content = ''
                        if hasattr(entry, 'summary'):
                            content = entry.summary
                        elif hasattr(entry, 'content') and entry.content:
                            content = entry.content[0].value if isinstance(entry.content, list) else str(entry.content)
                        elif hasattr(entry, 'description'):
                            content = entry.description
                        
                        if content:
                            soup = BeautifulSoup(content, 'html.parser')
                            content = soup.get_text().strip()
                        
                        # Skip if no meaningful content
                        if len(content) < 50:
                            continue
                        
                        # Get title
                        title = getattr(entry, 'title', 'No Title').strip()
                        if not title or len(title) < 10:
                            continue
                        
                        # Enhanced priority detection
                        priority = self._calculate_priority(title, content, source['priority'], category)
                        
                        # Calculate reading time
                        reading_time = self._calculate_reading_time(content)
                        
                        # Generate excerpt and AI summary
                        excerpt = content[:400] + "..." if len(content) > 400 else content
                        ai_summary = self.ai.generate_summary(title, content[:2000], category)
                        
                        # Extract tags
                        tags = self._extract_tags(title, content, category)
                        
                        article = NewsArticle(
                            id=article_id,
                            title=title,
                            url=entry.link,
                            source=source['name'],
                            author=getattr(entry, 'author', None),
                            published_date=published_date,
                            content=content,
                            excerpt=excerpt,
                            ai_summary=ai_summary,
                            category=category,
                            priority=priority,
                            tags=tags,
                            reading_time=reading_time,
                            extracted_at=datetime.now()
                        )
                        
                        articles.append(article)
                        
                    except Exception as e:
                        logger.warning(f"Error processing entry from {source['name']}: {str(e)}")
                        continue
                        
        except asyncio.TimeoutError:
            logger.warning(f"Timeout fetching {source['name']}")
        except Exception as e:
            logger.error(f"Error fetching {source['name']}: {str(e)}")
        
        return articles
    
    def _article_exists(self, article_id: str) -> bool:
        """Check if article already exists"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("SELECT 1 FROM articles WHERE id = ?", (article_id,))
                return cursor.fetchone() is not None
        except:
            return False
    
    def _extract_tags(self, title: str, content: str, category: str) -> List[str]:
        """Enhanced tag extraction with better categorization"""
        text = f"{title} {content}".lower()
        tags = []
        
        # Category-specific tag extraction
        if category == "ai":
            ai_terms = {
                'gpt': ['gpt', 'chatgpt', 'gpt-4', 'gpt-3'],
                'llm': ['language model', 'llm', 'large language'],
                'ml': ['machine learning', 'deep learning', 'neural network'],
                'startup': ['startup', 'funding', 'investment', 'series a'],
                'research': ['paper', 'research', 'study', 'journal'],
                'robotics': ['robot', 'robotics', 'autonomous'],
                'computer_vision': ['computer vision', 'image recognition'],
                'nlp': ['natural language', 'nlp', 'text processing'],
                'ethics': ['ethics', 'bias', 'fairness', 'responsible ai']
            }
        elif category == "finance":
            ai_terms = {
                'crypto': ['bitcoin', 'cryptocurrency', 'crypto', 'ethereum'],
                'stocks': ['stock', 'equity', 'shares', 'nasdaq', 'sp500'],
                'fed': ['federal reserve', 'fed', 'interest rate', 'fomc'],
                'market': ['market', 'trading', 'dow jones'],
                'banking': ['bank', 'banking', 'credit', 'loan'],
                'inflation': ['inflation', 'cpi', 'consumer price'],
                'earnings': ['earnings', 'revenue', 'profit', 'quarterly'],
                'ipo': ['ipo', 'public offering', 'listing'],
                'merger': ['merger', 'acquisition', 'm&a']
            }
        else:  # politics
            ai_terms = {
                'congress': ['congress', 'senate', 'house', 'representatives'],
                'election': ['election', 'vote', 'campaign', 'ballot'],
                'policy': ['policy', 'legislation', 'bill', 'law'],
                'international': ['international', 'foreign', 'diplomatic'],
                'supreme_court': ['supreme court', 'scotus', 'judicial'],
                'presidency': ['president', 'white house', 'administration'],
                'healthcare': ['healthcare', 'medicare', 'medicaid'],
                'economy': ['economic', 'fiscal', 'budget'],
                'climate': ['climate', 'environmental', 'green energy']
            }
            
        for tag, keywords in ai_terms.items():
            if any(keyword in text for keyword in keywords):
                tags.append(tag)
        
        return tags[:8]  # Limit to 8 tags
    
    def save_article(self, article: NewsArticle) -> bool:
        """Enhanced article saving with conflict handling"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT OR IGNORE INTO articles 
                    (id, title, url, source, author, published_date, content, excerpt,
                     ai_summary, category, priority, tags, reading_time, extracted_at,
                     is_read, is_starred)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, FALSE, FALSE)
                """, (
                    article.id, article.title, article.url, article.source, article.author,
                    article.published_date, article.content, article.excerpt, article.ai_summary,
                    article.category, article.priority, json.dumps(article.tags), 
                    article.reading_time, article.extracted_at
                ))
                
                # Return True if a new article was inserted
                return conn.total_changes > 0
                
        except Exception as e:
            logger.error(f"Error saving article: {e}")
            return False
    
    def mark_article_read(self, article_id: str) -> bool:
        """Mark article as read"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    UPDATE articles 
                    SET is_read = TRUE, read_at = ? 
                    WHERE id = ?
                """, (datetime.now(), article_id))
                return True
        except Exception as e:
            logger.error(f"Error marking article read: {e}")
            return False
    
    def star_article(self, article_id: str, starred: bool = True) -> bool:
        """Star or unstar an article"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                starred_at = datetime.now() if starred else None
                conn.execute("""
                    UPDATE articles 
                    SET is_starred = ?, starred_at = ? 
                    WHERE id = ?
                """, (starred, starred_at, article_id))
                return True
        except Exception as e:
            logger.error(f"Error starring article: {e}")
            return False

# Initialize FastAPI application
app = FastAPI(title="RPNews - Complete AI News Intelligence", version="2.0.2")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the enhanced news engine
news_engine = RPNewsEngine()

@app.on_event("startup")
async def startup_event():
    """Start background tasks when FastAPI starts"""
    logger.info("🚀 Complete FastAPI startup - starting continuous background collection")
    news_engine.start_background_collection()

# Complete professional news dashboard with full UI
@app.get("/", response_class=HTMLResponse)
async def dashboard():
    """Complete professional news intelligence dashboard with full frontend"""
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RPNews - AI News Intelligence</title>
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
        
        .controls {
            display: flex;
            gap: 10px;
            align-items: center;
        }
        
        .control-btn {
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            border: none;
            padding: 10px 16px;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 6px;
            font-size: 0.9em;
        }
        
        .control-btn:hover {
            transform: translateY(-1px);
            box-shadow: 0 6px 16px rgba(102, 126, 234, 0.3);
        }
        
        .control-btn.secondary {
            background: rgba(102, 126, 234, 0.1);
            color: #667eea;
            border: 1px solid rgba(102, 126, 234, 0.3);
        }
        
        .status-indicator {
            display: flex;
            align-items: center;
            gap: 6px;
            font-size: 0.85em;
            color: #666;
        }
        
        .status-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #28a745;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 30px 20px;
        }
        
        .briefing-header {
            text-align: center;
            margin-bottom: 30px;
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
            margin-bottom: 20px;
        }
        
        .daily-overview {
            background: linear-gradient(135deg, #f8f9ff, #e8ecff);
            padding: 25px;
            border-radius: 15px;
            border-left: 5px solid #667eea;
            margin-bottom: 20px;
            font-size: 1.05em;
            line-height: 1.7;
            color: #2c3e50;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.1);
        }
        
        .overview-title {
            font-weight: 700;
            color: #667eea;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 8px;
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
            padding: 12px 20px;
            background: rgba(102, 126, 234, 0.1);
            border-radius: 12px;
            min-width: 100px;
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
        
        .view-controls {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 25px;
            flex-wrap: wrap;
            gap: 15px;
        }
        
        .filter-controls {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }
        
        .filter-btn {
            padding: 8px 16px;
            border: 1px solid rgba(102, 126, 234, 0.3);
            background: rgba(102, 126, 234, 0.1);
            color: #667eea;
            border-radius: 20px;
            cursor: pointer;
            font-size: 0.9em;
            transition: all 0.3s ease;
        }
        
        .filter-btn.active {
            background: #667eea;
            color: white;
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
            flex: 1;
        }
        
        .category-stats {
            display: flex;
            gap: 15px;
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
            opacity: 1;
        }
        
        .article-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(0, 0, 0, 0.15);
        }
        
        .article-card.read {
            opacity: 0.7;
        }
        
        .article-card.starred {
            border-left: 4px solid #ffd700;
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
        
        .article-time-info {
            display: flex;
            align-items: center;
            gap: 10px;
            color: #95a5a6;
            font-size: 0.85em;
        }
        
        .reading-time {
            background: rgba(102, 126, 234, 0.1);
            color: #667eea;
            padding: 2px 8px;
            border-radius: 10px;
            font-size: 0.8em;
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
            cursor: pointer;
            transition: color 0.3s ease;
        }
        
        .article-title:hover {
            color: #667eea;
        }
        
        .article-actions {
            position: absolute;
            top: 15px;
            left: 15px;
            display: flex;
            gap: 5px;
        }
        
        .action-btn {
            width: 28px;
            height: 28px;
            border-radius: 50%;
            border: none;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 14px;
            transition: all 0.3s ease;
            background: rgba(255, 255, 255, 0.9);
            color: #666;
        }
        
        .action-btn:hover {
            background: white;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
        }
        
        .action-btn.read {
            color: #28a745;
        }
        
        .action-btn.starred {
            color: #ffd700;
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
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .article-summary:hover {
            background: linear-gradient(135deg, #f0f4ff, #e8ecff);
            transform: translateX(2px);
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
        
        .initial-loading {
            background: rgba(255, 255, 255, 0.9);
            padding: 40px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            margin: 40px 0;
        }
        
        .collection-status {
            background: rgba(40, 167, 69, 0.1);
            border: 1px solid rgba(40, 167, 69, 0.3);
            color: #28a745;
            padding: 15px 20px;
            border-radius: 10px;
            margin: 20px 0;
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 10px;
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
            
            .controls {
                width: 100%;
                justify-content: center;
                flex-wrap: wrap;
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
                flex-wrap: wrap;
            }
            
            .view-controls {
                flex-direction: column;
                align-items: flex-start;
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
                <button class="nav-tab active" data-view="briefing">Daily Briefing</button>
                <button class="nav-tab" data-view="ai">AI & Technology</button>
                <button class="nav-tab" data-view="finance">Finance & Markets</button>
                <button class="nav-tab" data-view="politics">Politics & Policy</button>
                <button class="nav-tab" data-view="starred">⭐ Starred</button>
            </div>
            <div class="controls">
                <div class="status-indicator">
                    <div class="status-dot"></div>
                    <span>Auto-updating</span>
                </div>
                <button class="control-btn secondary" data-view="reading-list">📖 Reading List</button>
                <button class="control-btn secondary" onclick="debugAPI()">🔍 Debug</button>
                <button class="control-btn" onclick="refreshNews()">
                    <span id="refresh-icon">↻</span> Refresh
                </button>
            </div>
        </div>
    </header>

    <div class="container">
        <div id="loading" class="loading">
            <div class="loading-spinner"></div>
            <h3>Loading your personalized news briefing...</h3>
            <p>Collecting and analyzing articles from premium sources</p>
            <div class="collection-status">
                <span>🔄</span>
                News collection is running automatically every 30 minutes
            </div>
        </div>

        <div id="content" style="display: none;">
            <div class="briefing-header">
                <h1 class="briefing-title">Daily Intelligence Briefing</h1>
                <p class="briefing-date" id="briefing-date"></p>
                
                <div id="daily-overview" class="daily-overview" style="display: none;">
                    <div class="overview-title">🌅 Daily Overview</div>
                    <div id="overview-text"></div>
                </div>
                
                <div class="stats-bar" id="stats-bar"></div>
            </div>

            <div class="view-controls">
                <div class="filter-controls">
                    <button class="filter-btn active" data-filter="all">All Priority</button>
                    <button class="filter-btn" data-filter="high">High Priority</button>
                    <button class="filter-btn" data-filter="unread">Unread Only</button>
                </div>
            </div>

            <div id="news-content"></div>
        </div>
    </div>

    <script>
        let currentData = null;
        let currentView = 'briefing';
        let currentFilter = 'all';
        let isLoading = false;

        // Initialize
        document.addEventListener('DOMContentLoaded', function() {
            loadBriefing();
            setupNavigation();
            setupFilters();
            
            // Auto-refresh every 5 minutes to check for new articles
            setInterval(autoRefresh, 300000); // 5 minutes
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

        function setupFilters() {
            document.querySelectorAll('.filter-btn').forEach(btn => {
                btn.addEventListener('click', function() {
                    document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                    this.classList.add('active');
                    
                    currentFilter = this.dataset.filter;
                    if (currentData) {
                        displayContent();
                    }
                });
            });
        }

        async function loadBriefing() {
            if (isLoading) return;
            isLoading = true;
            
            try {
                showLoading();
                const response = await fetch('/api/morning-briefing');
                
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}`);
                }
                
                currentData = await response.json();
                
                // Log the response for debugging
                console.log('Briefing data received:', currentData);
                
                // Always try to display content, even if it seems empty
                displayContent();
                
            } catch (error) {
                console.error('Error loading briefing:', error);
                // Even on error, try to show something
                hideLoading();
                showEmptyState(`Unable to load news briefing. Error: ${error.message}`);
            } finally {
                isLoading = false;
            }
        }

        async function autoRefresh() {
            // Silent refresh - don't show loading spinner
            try {
                const response = await fetch('/api/morning-briefing');
                if (response.ok) {
                    const newData = await response.json();
                    
                    // Only update if we got more articles
                    const newTotal = newData.total_articles || 0;
                    const currentTotal = currentData?.total_articles || 0;
                    
                    if (newTotal > currentTotal) {
                        currentData = newData;
                        displayContent();
                        console.log(`Auto-refresh: Found ${newTotal - currentTotal} new articles`);
                    }
                }
            } catch (error) {
                console.log('Auto-refresh failed:', error);
            }
        }

        async function refreshNews() {
            const refreshIcon = document.getElementById('refresh-icon');
            refreshIcon.style.animation = 'spin 1s linear infinite';
            
            try {
                await loadBriefing();
            } finally {
                setTimeout(() => {
                    refreshIcon.style.animation = 'none';
                }, 1000);
            }
        }

        async function debugAPI() {
            console.log('=== DEBUG API CALLS ===');
            
            try {
                // Test health endpoint
                console.log('Testing health endpoint...');
                const healthResponse = await fetch('/api/health');
                const healthData = await healthResponse.json();
                console.log('Health data:', healthData);
                
                // Test morning briefing endpoint
                console.log('Testing morning briefing endpoint...');
                const briefingResponse = await fetch('/api/morning-briefing');
                const briefingData = await briefingResponse.json();
                console.log('Briefing data:', briefingData);
                
                // Test stats endpoint
                console.log('Testing stats endpoint...');
                const statsResponse = await fetch('/api/stats');
                const statsData = await statsResponse.json();
                console.log('Stats data:', statsData);
                
                alert(`Debug complete! Check browser console (F12) for details. 
Articles found: ${briefingData.total_articles || 0}`);
                
            } catch (error) {
                console.error('Debug error:', error);
                alert(`Debug failed: ${error.message}`);
            }
        }

        async function markAsRead(articleId, element) {
            try {
                const response = await fetch(`/api/articles/${articleId}/read`, { method: 'POST' });
                if (response.ok) {
                    element.closest('.article-card').classList.add('read');
                    const btn = element.closest('.article-card').querySelector('.read-btn');
                    btn.classList.add('read');
                    btn.innerHTML = '✓';
                }
            } catch (error) {
                console.error('Error marking as read:', error);
            }
        }

        async function toggleStar(articleId, element) {
            try {
                const card = element.closest('.article-card');
                const isStarred = card.classList.contains('starred');
                
                const response = await fetch(`/api/articles/${articleId}/star`, { 
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ starred: !isStarred })
                });
                
                if (response.ok) {
                    if (isStarred) {
                        card.classList.remove('starred');
                        element.innerHTML = '☆';
                        element.classList.remove('starred');
                    } else {
                        card.classList.add('starred');
                        element.innerHTML = '★';
                        element.classList.add('starred');
                    }
                }
            } catch (error) {
                console.error('Error toggling star:', error);
            }
        }

        function openArticle(url, summaryElement) {
            // Mark the summary as clicked (visual feedback)
            summaryElement.style.background = 'linear-gradient(135deg, #e8ecff, #d4e3ff)';
            
            // Open article in new tab
            window.open(url, '_blank', 'noopener,noreferrer');
        }

        function showLoading() {
            document.getElementById('loading').style.display = 'block';
            document.getElementById('content').style.display = 'none';
        }

        function hideLoading() {
            document.getElementById('loading').style.display = 'none';
            document.getElementById('content').style.display = 'block';
        }

        function showEmptyState(message) {
            hideLoading();
            document.getElementById('news-content').innerHTML = `
                <div class="empty-state">
                    <div class="empty-state-icon">📰</div>
                    <h3>News Collection in Progress</h3>
                    <p>${message}</p>
                    <div class="collection-status">
                        <span>🔄</span>
                        Articles are being collected automatically every 30 minutes
                    </div>
                </div>
            `;
        }

        function displayContent() {
            hideLoading();
            
            // Log what we received
            console.log('Displaying content. Data check:', {
                hasData: !!currentData,
                hasBriefing: !!(currentData && currentData.briefing),
                totalArticles: currentData?.total_articles || 0,
                aiArticles: currentData?.briefing?.ai?.length || 0,
                financeArticles: currentData?.briefing?.finance?.length || 0,
                politicsArticles: currentData?.briefing?.politics?.length || 0
            });
            
            if (!currentData) {
                showEmptyState("No data received from server. Please try refreshing.");
                return;
            }

            // Check if we have any articles at all
            const totalArticles = (currentData.briefing?.ai?.length || 0) + 
                                 (currentData.briefing?.finance?.length || 0) + 
                                 (currentData.briefing?.politics?.length || 0);
            
            console.log('Total articles found:', totalArticles);
