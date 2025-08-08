"""
RPNews - API Routes
Handles all HTTP endpoints and API logic
"""

import json
import logging
import sqlite3
from datetime import datetime
from fastapi import HTTPException, BackgroundTasks
import aiohttp

logger = logging.getLogger(__name__)

class APIRoutes:
    """API endpoint handlers"""
    
    def __init__(self, news_engine):
        self.news_engine = news_engine
    
    async def get_morning_briefing(self):
        """Generate comprehensive morning briefing with daily overview"""
        try:
            with sqlite3.connect(self.news_engine.db_path) as conn:
                briefing = {}
                total_articles = 0
                high_priority_count = 0
                
                for category in ['ai', 'finance', 'politics']:
                    cursor = conn.execute("""
                        SELECT id, title, url, source, author, published_date, excerpt,
                               ai_summary, priority, tags, reading_time, is_read, is_starred
                        FROM articles 
                        WHERE category = ? AND published_date >= datetime('now', '-24 hours')
                        ORDER BY 
                            CASE priority 
                                WHEN 'high' THEN 3 
                                WHEN 'medium' THEN 2 
                                ELSE 1 
                            END DESC,
                            published_date DESC
                        LIMIT 15
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
                        
                        is_high_priority = row[8] == 'high'
                        if is_high_priority:
                            high_priority_count += 1
                        
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
                            'readingTime': row[10] or 2,
                            'category': category,
                            'timeAgo': time_str,
                            'isRead': bool(row[11]),
                            'isStarred': bool(row[12])
                        })
                    
                    briefing[category] = articles
                    total_articles += len(articles)
                
                # Get daily overview
                today = datetime.now().strftime('%Y-%m-%d')
                cursor = conn.execute("""
                    SELECT overview_text FROM daily_overviews 
                    WHERE date = ? ORDER BY generated_at DESC LIMIT 1
                """, (today,))
                overview_result = cursor.fetchone()
                daily_overview = overview_result[0] if overview_result else None
                
                return {
                    'platform': 'RPNews Enhanced',
                    'date': datetime.now().strftime('%B %d, %Y'),
                    'briefing': briefing,
                    'daily_overview': daily_overview,
                    'generated_at': datetime.now().isoformat(),
                    'total_articles': total_articles,
                    'high_priority_count': high_priority_count,
                    'ai_type': self.news_engine.ai.ai_type,
                    'message': 'Your enhanced AI-powered briefing is ready!'
                }
                
        except Exception as e:
            logger.error(f"Error generating briefing: {str(e)}")
            return {
                'platform': 'RPNews Enhanced',
                'date': datetime.now().strftime('%B %d, %Y'),
                'briefing': {'ai': [], 'finance': [], 'politics': []},
                'daily_overview': 'Daily overview will be available after first news collection.',
                'error': 'Briefing generation failed - this may be the first run',
                'generated_at': datetime.now().isoformat(),
                'suggestion': 'Try clicking "Refresh" to collect the latest news'
            }
    
    async def mark_article_read(self, article_id: str):
        """Mark an article as read"""
        success = self.news_engine.mark_article_read(article_id)
        if success:
            return {'status': 'success', 'message': 'Article marked as read'}
        else:
            raise HTTPException(status_code=500, detail="Failed to mark article as read")
    
    async def star_article(self, article_id: str, request: dict):
        """Star or unstar an article"""
        starred = request.get('starred', True)
        success = self.news_engine.star_article(article_id, starred)
        if success:
            action = 'starred' if starred else 'unstarred'
            return {'status': 'success', 'message': f'Article {action}'}
        else:
            raise HTTPException(status_code=500, detail="Failed to update article star status")
    
    async def get_starred_articles(self):
        """Get all starred articles"""
        try:
            with sqlite3.connect(self.news_engine.db_path) as conn:
                cursor = conn.execute("""
                    SELECT id, title, url, source, author, published_date, excerpt,
                           ai_summary, category, priority, tags, reading_time, starred_at
                    FROM articles 
                    WHERE is_starred = TRUE
                    ORDER BY starred_at DESC
                    LIMIT 100
                """)
                
                articles = []
                for row in cursor.fetchall():
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
                        'category': row[8],
                        'priority': row[9],
                        'tags': json.loads(row[10] or '[]'),
                        'readingTime': row[11] or 2,
                        'timeAgo': time_str,
                        'starredAt': row[12],
                        'isStarred': True
                    })
                
                return {
                    'articles': articles,
                    'count': len(articles),
                    'generated_at': datetime.now().isoformat()
                }
                
        except Exception as e:
            logger.error(f"Error getting starred articles: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to get starred articles")
    
    async def get_articles(self, category: str, limit: int = 50, priority: str = "all"):
        """Get articles for a specific category with enhanced features"""
        if category not in ['ai', 'finance', 'politics']:
            raise HTTPException(status_code=400, detail="Category must be ai, finance, or politics")
        
        try:
            with sqlite3.connect(self.news_engine.db_path) as conn:
                query = """
                    SELECT id, title, url, source, author, published_date, excerpt,
                           ai_summary, priority, tags, reading_time, is_read, is_starred
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
                        'readingTime': row[10] or 2,
                        'category': category,
                        'timeAgo': time_str,
                        'isRead': bool(row[11]),
                        'isStarred': bool(row[12])
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
    
    async def get_stats(self):
        """Enhanced platform statistics"""
        try:
            with sqlite3.connect(self.news_engine.db_path) as conn:
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
                    
                    # High priority today
                    cursor = conn.execute("""
                        SELECT COUNT(*) FROM articles 
                        WHERE category = ? AND priority = 'high' AND published_date >= date('now')
                    """, (category,))
                    stats[f'{category}_high_priority'] = cursor.fetchone()[0]
                
                # Reading stats
                cursor = conn.execute("SELECT COUNT(*) FROM articles WHERE is_read = TRUE")
                stats['articles_read'] = cursor.fetchone()[0]
                
                cursor = conn.execute("SELECT COUNT(*) FROM articles WHERE is_starred = TRUE")
                stats['articles_starred'] = cursor.fetchone()[0]
                
                # Source counts
                stats['sources'] = {
                    'ai': len(self.news_engine.sources['ai']),
                    'finance': len(self.news_engine.sources['finance']),
                    'politics': len(self.news_engine.sources['politics'])
                }
                
                # AI type
                stats['ai_type'] = self.news_engine.ai.ai_type
                stats['ai_available'] = self.news_engine.ai.ai_available
                
                return stats
                
        except Exception as e:
            logger.error(f"Error getting stats: {str(e)}")
            return {
                'error': 'Stats temporarily unavailable',
                'ai_type': self.news_engine.ai.ai_type,
                'ai_available': self.news_engine.ai.ai_available,
                'sources': {
                    'ai': len(self.news_engine.sources['ai']),
                    'finance': len(self.news_engine.sources['finance']),
                    'politics': len(self.news_engine.sources['politics'])
                }
            }
    
    async def trigger_collection(self, background_tasks: BackgroundTasks):
        """Enhanced manual collection trigger"""
        
        async def run_collection():
            try:
                logger.info("Manual collection triggered")
                async with aiohttp.ClientSession(
                    timeout=aiohttp.ClientTimeout(total=45),
                    headers={'User-Agent': 'RPNews Enhanced/2.0'}
                ) as session:
                    self.news_engine.session = session
                    total_collected = await self.news_engine.collect_all_news()
                    self.news_engine.session = None
                    logger.info(f"Manual collection completed: {total_collected} articles")
            except Exception as e:
                logger.error(f"Manual collection error: {str(e)}")
        
        background_tasks.add_task(run_collection)
        
        return {
            'message': 'Enhanced news collection started',
            'timestamp': datetime.now().isoformat(),
            'status': 'Background collection initiated with AI processing',
            'note': 'Articles with AI summaries will appear in a few minutes',
            'features': ['AI summaries', 'Priority detection', 'Reading time estimation']
        }
    
    async def health_check(self):
        """Enhanced health check with AI status"""
        try:
            # Test database connectivity
            with sqlite3.connect(self.news_engine.db_path) as conn:
                cursor = conn.execute("SELECT COUNT(*) FROM articles")
                article_count = cursor.fetchone()[0]
                
                cursor = conn.execute("SELECT COUNT(*) FROM articles WHERE is_read = TRUE")
                read_count = cursor.fetchone()[0]
                
                cursor = conn.execute("SELECT COUNT(*) FROM articles WHERE is_starred = TRUE")
                starred_count = cursor.fetchone()[0]
            
            return {
                'status': 'healthy',
                'platform': 'RPNews Enhanced',
                'timestamp': datetime.now().isoformat(),
                'ai_type': self.news_engine.ai.ai_type,
                'ai_available': self.news_engine.ai.ai_available,
                'article_count': article_count,
                'articles_read': read_count,
                'articles_starred': starred_count,
                'sources_count': sum(len(sources) for sources in self.news_engine.sources.values()),
                'database': 'connected',
                'features': ['AI Summaries', 'Priority Detection', 'Article Management', 'Daily Overview']
            }
        except Exception as e:
            return {
                'status': 'unhealthy',
                'platform': 'RPNews Enhanced', 
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
