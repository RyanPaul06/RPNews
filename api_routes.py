"""
RPNews - API Routes (Updated with Article Detail & Chat)
Handles all HTTP endpoints and API logic with enhanced functionality
"""

import json
import logging
import sqlite3
from datetime import datetime
from fastapi import HTTPException, BackgroundTasks
from pydantic import BaseModel
import aiohttp

logger = logging.getLogger(__name__)

class ChatRequest(BaseModel):
    articleId: str
    message: str
    articleTitle: str
    articleContent: str
    aiSummary: str = None

class APIRoutes:
    """API endpoint handlers with enhanced functionality"""
    
    def __init__(self, news_engine):
        self.news_engine = news_engine
    
    async def get_morning_briefing(self):
        """Generate comprehensive morning briefing with daily overview"""
        try:
            # Use the new method that properly distributes 100 articles
            briefing = self.news_engine.get_articles_for_briefing(limit=100)
            
            total_articles = sum(len(articles) for articles in briefing.values())
            high_priority_count = sum(
                len([a for a in articles if a.get('priority') == 'high']) 
                for articles in briefing.values()
            )
            
            # Get daily overview
            today = datetime.now().strftime('%Y-%m-%d')
            with sqlite3.connect(self.news_engine.db_path) as conn:
                cursor = conn.execute("""
                    SELECT overview_text FROM daily_overviews 
                    WHERE date = ? ORDER BY generated_at DESC LIMIT 1
                """, (today,))
                overview_result = cursor.fetchone()
                daily_overview = overview_result[0] if overview_result else None
            
            return {
                'platform': 'RPNews Enhanced with Open Source LLMs',
                'date': datetime.now().strftime('%B %d, %Y'),
                'briefing': briefing,
                'daily_overview': daily_overview,
                'generated_at': datetime.now().isoformat(),
                'total_articles': total_articles,
                'high_priority_count': high_priority_count,
                'ai_type': self.news_engine.ai.ai_type,
                'ai_available': self.news_engine.ai.ai_available,
                'message': 'Your enhanced AI-powered briefing with open source LLMs is ready!',
                'distribution': {
                    'ai': len(briefing.get('ai', [])),
                    'finance': len(briefing.get('finance', [])),
                    'politics': len(briefing.get('politics', []))
                }
            }
                
        except Exception as e:
            logger.error(f"Error generating briefing: {str(e)}")
            return {
                'platform': 'RPNews Enhanced with Open Source LLMs',
                'date': datetime.now().strftime('%B %d, %Y'),
                'briefing': {'ai': [], 'finance': [], 'politics': []},
                'daily_overview': 'Daily overview will be available after first news collection.',
                'error': 'Briefing generation failed - this may be the first run',
                'generated_at': datetime.now().isoformat(),
                'suggestion': 'Try clicking "Refresh" to collect the latest news'
            }
    
    async def get_article_detail(self, article_id: str):
        """Get detailed article information for the article detail page"""
        try:
            with sqlite3.connect(self.news_engine.db_path) as conn:
                cursor = conn.execute("""
                    SELECT id, title, url, source, author, published_date, content, excerpt,
                           ai_summary, category, priority, tags, reading_time, is_read, is_starred
                    FROM articles 
                    WHERE id = ?
                """, (article_id,))
                
                row = cursor.fetchone()
                if not row:
                    raise HTTPException(status_code=404, detail="Article not found")
                
                # Calculate time ago
                try:
                    pub_date = datetime.fromisoformat(row[5])
                    hours_ago = int((datetime.now() - pub_date).total_seconds() / 3600)
                    if hours_ago < 1:
                        time_str = "Just now"
                    elif hours_ago < 24:
                        time_str = f"{hours_ago}h ago"
                    else:
                        days_ago = hours_ago // 24
                        time_str = f"{days_ago}d ago"
                except:
                    time_str = "Recently"
                
                article = {
                    'id': row[0],
                    'title': row[1],
                    'url': row[2],
                    'source': row[3],
                    'author': row[4] or 'Unknown',
                    'publishedDate': row[5],
                    'content': row[6] or row[7],  # Use full content if available, else excerpt
                    'excerpt': row[7],
                    'aiSummary': row[8],
                    'category': row[9],
                    'priority': row[10],
                    'tags': json.loads(row[11] or '[]'),
                    'readingTime': row[12] or 2,
                    'timeAgo': time_str,
                    'isRead': bool(row[13]),
                    'isStarred': bool(row[14])
                }
                
                # Mark as read when viewing detail
                self.news_engine.mark_article_read(article_id, True)
                
                return article
                
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error getting article detail: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to get article detail")
    
    async def chat_about_article(self, chat_request: ChatRequest):
        """Handle AI chat about a specific article"""
        try:
            # Get the article context
            article_context = f"""
            Article Title: {chat_request.articleTitle}
            Article Content: {chat_request.articleContent}
            AI Summary: {chat_request.aiSummary or 'No summary available'}
            
            User Question: {chat_request.message}
            """
            
            # Generate AI response based on available AI system
            if self.news_engine.ai.ollama_available:
                response = await self._chat_with_ollama(article_context, chat_request.message)
            elif self.news_engine.ai.transformers_available:
                response = await self._chat_with_transformers(article_context, chat_request.message)
            else:
                response = await self._chat_with_rules(article_context, chat_request.message)
            
            return {
                'response': response,
                'timestamp': datetime.now().isoformat(),
                'ai_type': self.news_engine.ai.ai_type
            }
            
        except Exception as e:
            logger.error(f"Error in article chat: {str(e)}")
            return {
                'response': "I apologize, but I encountered an error processing your question. Could you try rephrasing it?",
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    async def _chat_with_ollama(self, article_context: str, user_question: str) -> str:
        """Generate chat response using Ollama"""
        try:
            import requests
            
            prompt = f"""You are an AI assistant helping users understand news articles. Based on the article information provided, answer the user's question in a helpful, informative way.

            {article_context}
            
            Please provide a clear, concise answer that directly addresses the user's question. If the question is about implications or analysis, provide thoughtful insights based on the article content.
            
            Answer:"""
            
            response = requests.post(
                f"{self.news_engine.ai.ollama_url}/api/generate",
                json={
                    "model": self.news_engine.ai.ollama_model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "top_p": 0.9,
                        "max_tokens": 300
                    }
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                answer = result.get("response", "").strip()
                return answer if answer else "I don't have enough information to answer that question."
            else:
                return "I'm having trouble processing your question right now. Please try again."
                
        except Exception as e:
            logger.error(f"Ollama chat error: {e}")
            return "I'm having trouble processing your question right now. Please try again."
    
    async def _chat_with_transformers(self, article_context: str, user_question: str) -> str:
        """Generate chat response using transformers (limited capability)"""
        try:
            # For transformers, we'll provide rule-based responses since they're mainly for summarization
            return await self._chat_with_rules(article_context, user_question)
            
        except Exception as e:
            logger.error(f"Transformers chat error: {e}")
            return "I'm having trouble processing your question right now. Please try again."
    
    async def _chat_with_rules(self, article_context: str, user_question: str) -> str:
        """Generate chat response using rule-based logic"""
        try:
            question_lower = user_question.lower()
            article_content = article_context.lower()
            
            # Extract article title and content for better responses
            lines = article_context.split('\n')
            title = ""
            content = ""
            summary = ""
            
            for line in lines:
                if line.startswith("Article Title:"):
                    title = line.replace("Article Title:", "").strip()
                elif line.startswith("Article Content:"):
                    content = line.replace("Article Content:", "").strip()
                elif line.startswith("AI Summary:"):
                    summary = line.replace("AI Summary:", "").strip()
            
            # Question pattern matching
            if any(word in question_lower for word in ['takeaway', 'key point', 'main point', 'summary']):
                if summary and summary != 'No summary available':
                    return f"The key takeaways from this article are: {summary}"
                else:
                    # Extract key points from content
                    sentences = content.split('.')
                    key_sentences = [s.strip() for s in sentences[:3] if len(s.strip()) > 20]
                    return f"Based on the article content, the main points are: {'. '.join(key_sentences)}."
            
            elif any(word in question_lower for word in ['implication', 'impact', 'effect', 'consequence']):
                if 'ai' in article_content or 'technology' in article_content:
                    return f"This development in AI/technology could impact the industry by potentially changing how companies approach innovation and competition. The implications may include shifts in market dynamics, regulatory considerations, and technological adoption patterns."
                elif 'finance' in article_content or 'market' in article_content or 'economic' in article_content:
                    return f"The financial implications of this news could affect market sentiment, investor confidence, and economic policy decisions. This may influence trading patterns, investment strategies, and regulatory responses."
                elif 'politic' in article_content or 'government' in article_content or 'policy' in article_content:
                    return f"The political implications include potential policy changes, shifts in public opinion, and impacts on governance. This could affect legislative priorities, electoral dynamics, and public policy direction."
                else:
                    return f"The implications of this development could be significant across multiple sectors, potentially affecting stakeholder decisions, market conditions, and future strategic planning."
            
            elif any(word in question_lower for word in ['trend', 'pattern', 'relate', 'connection']):
                return f"This article relates to current trends by reflecting ongoing developments in its sector. It connects to broader patterns of change, innovation, and adaptation that we're seeing across industries. Understanding these connections helps contextualize the significance of this particular development."
            
            elif any(word in question_lower for word in ['should know', 'important', 'background', 'context']):
                return f"What you should know about this topic: {title} represents an important development that fits into larger industry and societal trends. The key context is understanding how this affects stakeholders, what precedents it sets, and what it might signal for future developments in this area."
            
            elif any(word in question_lower for word in ['why', 'reason', 'cause']):
                return f"The reasons behind this development likely include market forces, technological advancement, regulatory changes, or strategic business decisions. Understanding the 'why' helps predict future similar developments and their potential impacts."
            
            elif any(word in question_lower for word in ['what', 'explain', 'tell me about']):
                return f"This article discusses: {title}. {summary if summary and summary != 'No summary available' else content[:200] + '...'} The significance lies in its potential impact on the relevant industry and stakeholders."
            
            elif any(word in question_lower for word in ['future', 'next', 'predict', 'expect']):
                return f"Looking forward, this development could lead to further innovations, policy changes, or market shifts in the same direction. Future developments might build on this foundation, creating new opportunities and challenges for stakeholders."
            
            elif any(word in question_lower for word in ['who', 'affect', 'impact']):
                return f"This development affects various stakeholders including companies in the sector, consumers, investors, regulators, and potentially the broader public. The specific impacts depend on their roles and interests in relation to this topic."
            
            else:
                # Generic helpful response
                return f"Based on the article about '{title}', I can provide insights on the key points, implications, trends, and context. The article covers important developments that have broader significance. Could you be more specific about what aspect you'd like me to focus on?"
                
        except Exception as e:
            logger.error(f"Rule-based chat error: {e}")
            return "I can help you understand this article better. Could you ask me about the key takeaways, implications, or any specific aspect of the content?"
    
    async def mark_article_read(self, article_id: str):
        """Mark an article as read or toggle read status"""
        try:
            with sqlite3.connect(self.news_engine.db_path) as conn:
                cursor = conn.execute("SELECT is_read FROM articles WHERE id = ?", (article_id,))
                result = cursor.fetchone()
                if not result:
                    raise HTTPException(status_code=404, detail="Article not found")
                
                current_read_status = bool(result[0])
                new_read_status = not current_read_status
                
                success = self.news_engine.mark_article_read(article_id, new_read_status)
                
                if success:
                    action = 'marked as read' if new_read_status else 'marked as unread'
                    return {
                        'status': 'success', 
                        'message': f'Article {action}',
                        'isRead': new_read_status
                    }
                else:
                    raise HTTPException(status_code=500, detail="Failed to update article read status")
                    
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error toggling read status: {e}")
            raise HTTPException(status_code=500, detail="Failed to update article read status")
    
    async def star_article(self, article_id: str, request: dict):
        """Star or unstar an article"""
        starred = request.get('starred', True)
        success = self.news_engine.star_article(article_id, starred)
        if success:
            action = 'starred' if starred else 'unstarred'
            return {'status': 'success', 'message': f'Article {action}', 'isStarred': starred}
        else:
            raise HTTPException(status_code=500, detail="Failed to update article star status")
    
    async def pass_article(self, article_id: str):
        """Pass/dismiss an article"""
        success = self.news_engine.pass_article(article_id)
        if success:
            return {'status': 'success', 'message': 'Article passed'}
        else:
            raise HTTPException(status_code=500, detail="Failed to pass article")
    
    async def get_reading_list(self):
        """Get unread articles (reading list)"""
        try:
            with sqlite3.connect(self.news_engine.db_path) as conn:
                cursor = conn.execute("""
                    SELECT id, title, url, source, author, published_date, excerpt,
                           ai_summary, category, priority, tags, reading_time,
                           is_read, is_starred
                    FROM articles 
                    WHERE is_read = FALSE AND is_passed = FALSE
                    ORDER BY 
                        CASE priority 
                            WHEN 'high' THEN 3 
                            WHEN 'medium' THEN 2 
                            ELSE 1 
                        END DESC,
                        published_date DESC
                    LIMIT 200
                """)
                
                articles = []
                for row in cursor.fetchall():
                    try:
                        pub_date = datetime.fromisoformat(row[5])
                        hours_ago = int((datetime.now() - pub_date).total_seconds() / 3600)
                        if hours_ago < 1:
                            time_str = "Just now"
                        elif hours_ago < 24:
                            time_str = f"{hours_ago}h ago"
                        else:
                            days_ago = hours_ago // 24
                            time_str = f"{days_ago}d ago"
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
                        'isRead': bool(row[12]),
                        'isStarred': bool(row[13])
                    })
                
                return {
                    'articles': articles,
                    'count': len(articles),
                    'generated_at': datetime.now().isoformat()
                }
                
        except Exception as e:
            logger.error(f"Error getting reading list: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to get reading list")
    
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
                        if hours_ago < 1:
                            time_str = "Just now"
                        elif hours_ago < 24:
                            time_str = f"{hours_ago}h ago"
                        else:
                            days_ago = hours_ago // 24
                            time_str = f"{days_ago}d ago"
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
                    WHERE category = ? AND is_passed = FALSE
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
                        if hours_ago < 1:
                            time_str = "Just now"
                        elif hours_ago < 24:
                            time_str = f"{hours_ago}h ago"
                        else:
                            days_ago = hours_ago // 24
                            time_str = f"{days_ago}d ago"
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
                
                cursor = conn.execute("SELECT COUNT(*) FROM articles WHERE is_passed = TRUE")
                stats['articles_passed'] = cursor.fetchone()[0]
                
                # Source counts
                stats['sources'] = {
                    'ai': len(self.news_engine.sources['ai']),
                    'finance': len(self.news_engine.sources['finance']),
                    'politics': len(self.news_engine.sources['politics'])
                }
                
                # AI type and availability
                stats['ai_type'] = self.news_engine.ai.ai_type
                stats['ai_available'] = self.news_engine.ai.ai_available
                stats['ollama_available'] = getattr(self.news_engine.ai, 'ollama_available', False)
                stats['transformers_available'] = getattr(self.news_engine.ai, 'transformers_available', False)
                
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
                    headers={'User-Agent': 'RPNews Enhanced/2.0 with Open Source LLMs'}
                ) as session:
                    self.news_engine.session = session
                    total_collected = await self.news_engine.collect_all_news()
                    self.news_engine.session = None
                    logger.info(f"Manual collection completed: {total_collected} articles")
            except Exception as e:
                logger.error(f"Manual collection error: {str(e)}")
        
        background_tasks.add_task(run_collection)
        
        return {
            'message': 'Enhanced news collection started with open source LLM processing',
            'timestamp': datetime.now().isoformat(),
            'status': 'Background collection initiated with AI processing',
            'note': 'Articles with AI summaries will appear in a few minutes',
            'ai_type': self.news_engine.ai.ai_type,
            'features': ['Open source LLM summaries', 'Priority detection', 'Article management', 'Pass system']
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
                
                cursor = conn.execute("SELECT COUNT(*) FROM articles WHERE is_passed = TRUE")
                passed_count = cursor.fetchone()[0]
            
            return {
                'status': 'healthy',
                'platform': 'RPNews Enhanced with Open Source LLMs',
                'timestamp': datetime.now().isoformat(),
                'ai_type': self.news_engine.ai.ai_type,
                'ai_available': self.news_engine.ai.ai_available,
                'ollama_available': getattr(self.news_engine.ai, 'ollama_available', False),
                'transformers_available': getattr(self.news_engine.ai, 'transformers_available', False),
                'article_count': article_count,
                'articles_read': read_count,
                'articles_starred': starred_count,
                'articles_passed': passed_count,
                'sources_count': sum(len(sources) for sources in self.news_engine.sources.values()),
                'database': 'connected',
                'features': ['Open Source LLM Summaries', 'Priority Detection', 'Article Management', 'Pass System', 'Reading List', 'Article Detail View', 'AI Chat']
            }
        except Exception as e:
            return {
                'status': 'unhealthy',
                'platform': 'RPNews Enhanced with Open Source LLMs', 
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }