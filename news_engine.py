"""
RPNews - News Engine
Handles RSS feed collection, content processing, and data storage
"""

import asyncio
import aiohttp
import feedparser
import json
import logging
import sqlite3
import hashlib
import re
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from bs4 import BeautifulSoup

from ai_processor import RPNewsAI

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

class RPNewsEngine:
    """Enhanced news intelligence engine"""
    
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
                'breakthrough', 'released', 'announces', 'launches', 'gpt-', 'claude',
                'funding round', 'acquisition', 'partnership', 'regulation', 'banned',
                'agi', 'superintelligence', '$', 'billion', 'million funding'
            ],
            'finance': [
                'fed decision', 'interest rate', 'inflation', 'recession', 'crash',
                'bank failure', 'earnings beat', 'guidance', 'outlook', 'upgraded',
                'downgraded', 'merger', 'acquisition', 'ipo', 'bankruptcy'
            ],
            'politics': [
                'breaking', 'urgent', 'senate votes', 'house passes', 'president',
                'supreme court', 'indictment', 'investigation', 'scandal',
                'election results', 'poll', 'debate', 'resignation', 'appointed'
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
        """Enhanced background collection with initial startup collection"""
        logger.info("🚀 Starting initial news collection...")
        
        # Initial collection on startup
        try:
            async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=45),
                headers={'User-Agent': 'RPNews/2.0 (+https://rpnews.com)'}
            ) as session:
                self.session = session
                await self.collect_all_news()
                self.session = None
            logger.info("✅ Initial collection completed")
        except Exception as e:
            logger.error(f"Initial collection error: {e}")
        
        # Continue with regular collection cycle
        while True:
            try:
                await asyncio.sleep(3600)  # Wait 1 hour
                
                logger.info("🔄 Background collection starting...")
                async with aiohttp.ClientSession(
                    timeout=aiohttp.ClientTimeout(total=30),
                    headers={'User-Agent': 'RPNews/2.0 (+https://rpnews.com)'}
                ) as session:
                    self.session = session
                    await self.collect_all_news()
                    self.session = None
                
                logger.info("✅ Background collection complete. Next run in 1 hour.")
                
            except Exception as e:
                logger.error(f"Background collection error: {str(e)}")
                await asyncio.sleep(600)  # Wait 10 minutes on error
    
    async def collect_all_news(self):
        """Enhanced news collection with better processing"""
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
        
        # Generate daily overview after collection
        await self._generate_daily_overview()
        
        logger.info(f"✅ Total articles collected: {total_articles}")
        return total_articles
    
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
                
                logger.info(f"📊 Daily overview generated: {total_articles} articles, {high_priority_count} high priority")
                
        except Exception as e:
            logger.error(f"Error generating daily overview: {e}")
    
    async def collect_category(self, category: str) -> int:
        """Enhanced category collection with better AI processing"""
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
        """Enhanced RSS feed processing with better content extraction"""
        articles = []
        
        try:
            async with self.session.get(source['rss']) as response:
                if response.status != 200:
                    return articles
                
                content = await response.text()
                feed = feedparser.parse(content)
                
                for entry in feed.entries[:15]:  # Increased limit per source
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
                        
                        # Enhanced priority detection
                        priority = self._calculate_priority(entry.title, content, source['priority'], category)
                        
                        # Calculate reading time
                        reading_time = self._calculate_reading_time(content)
                        
                        # Generate excerpt and AI summary
                        excerpt = content[:400] + "..." if len(content) > 400 else content
                        ai_summary = self.ai.generate_summary(entry.title, content[:2000], category)
                        
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
                            priority=priority,
                            tags=tags,
                            reading_time=reading_time,
                            extracted_at=datetime.now()
                        )
                        
                        articles.append(article)
                        
                    except Exception as e:
                        logger.warning(f"Error processing article from {source['name']}: {str(e)}")
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
        """Enhanced tag extraction with better categorization"""
        text = f"{title} {content}".lower()
        tags = []
        
        # Category-specific tag extraction
        if category == "ai":
            ai_terms = {
                'gpt': ['gpt', 'chatgpt', 'gpt-4', 'gpt-3'],
                'llm': ['language model', 'llm', 'large language'],
                'ml': ['machine learning', 'deep learning', 'neural network'],
                'startup': ['startup', 'funding', 'investment', 'series a', 'series b'],
                'research': ['paper', 'research', 'arxiv', 'study', 'journal'],
                'robotics': ['robot', 'robotics', 'autonomous'],
                'computer_vision': ['computer vision', 'image recognition', 'cv'],
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
    
    def save_article(self, article: NewsArticle):
        """Enhanced article saving with new fields"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO articles 
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
