"""
RPNews - AI Processing Module
Handles AI-powered summarization and analysis
"""

import re
import logging
from typing import Dict, List

logger = logging.getLogger(__name__)

class RPNewsAI:
    """Advanced AI news analysis with proper summarization"""
    
    def __init__(self):
        self.ai_type = "enhanced_rules"
        self.ai_available = False
        logger.info("🤖 Initializing AI analysis system...")
        
        # Try to load actual AI model, fallback to enhanced rules
        try:
            # Only try to import if transformers is available
            import transformers
            from transformers import pipeline
            
            logger.info("📦 Transformers library found, attempting to load BART model...")
            self.summarizer = pipeline(
                "summarization", 
                model="facebook/bart-large-cnn",
                device=-1,  # CPU only for deployment
                max_length=1024  # Limit model size
            )
            self.ai_available = True
            self.ai_type = "transformer_based"
            logger.info("✅ BART summarization model loaded successfully")
            
        except ImportError:
            logger.info("📝 Transformers not available, using enhanced rule-based analysis")
            self.summarizer = None
            
        except Exception as e:
            logger.warning(f"⚠️ Could not load transformer model: {e}")
            logger.info("📝 Falling back to enhanced rule-based analysis")
            self.summarizer = None
    
    def generate_summary(self, title: str, content: str, category: str) -> str:
        """Generate intelligent summary using AI or enhanced rules"""
        if self.ai_available and self.summarizer and len(content) > 100:
            return self._ai_summary(title, content, category)
        else:
            return self._smart_rule_summary(title, content, category)
    
    def _ai_summary(self, title: str, content: str, category: str) -> str:
        """Generate AI-powered summary using BART model"""
        try:
            # Clean and prepare text
            clean_content = self._clean_text(content)
            
            # Truncate to model limits (1024 tokens ≈ 800 words)
            words = clean_content.split()
            if len(words) > 800:
                clean_content = " ".join(words[:800])
            
            # Generate summary with appropriate length
            summary_result = self.summarizer(
                clean_content,
                max_length=150,
                min_length=50,
                do_sample=False,
                truncation=True
            )
            
            ai_text = summary_result[0]['summary_text']
            
            # Category-specific formatting
            category_config = {
                "ai": "🤖 AI Development",
                "finance": "💰 Market Update", 
                "politics": "🏛️ Policy Update"
            }
            
            prefix = category_config.get(category, "📰 News Update")
            
            return f"{prefix}: {ai_text}"
            
        except Exception as e:
            logger.warning(f"AI summary failed: {e}")
            return self._smart_rule_summary(title, content, category)
    
    def _clean_text(self, text: str) -> str:
        """Clean text for AI processing"""
        # Remove HTML remnants
        text = re.sub(r'<[^>]+>', '', text)
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters that might confuse the model
        text = re.sub(r'[^\w\s\.\,\!\?\-\:\;]', '', text)
        return text.strip()
    
    def _smart_rule_summary(self, title: str, content: str, category: str) -> str:
        """Enhanced rule-based summary with intelligent parsing"""
        
        # Extract key sentences using importance indicators
        sentences = content.replace('\n', ' ').split('.')
        important_sentences = []
        
        # Enhanced key phrases by category
        key_indicators = {
            'ai': ['announces', 'launches', 'breakthrough', 'develops', 'ai', 'model', 'algorithm', 'machine learning', 'neural', 'artificial intelligence'],
            'finance': ['reports', 'earnings', 'revenue', 'profit', 'investment', 'funding', 'market', 'stock', 'financial', 'economic', 'fed', 'rate'],
            'politics': ['policy', 'legislation', 'congress', 'senate', 'president', 'governor', 'election', 'vote', 'political', 'government']
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
        """Generate comprehensive daily overview using AI or enhanced rules"""
        if self.ai_available and self.summarizer:
            return self._ai_daily_overview(articles_by_category)
        else:
            return self._rule_daily_overview(articles_by_category)
    
    def _ai_daily_overview(self, articles_by_category: Dict[str, List]) -> str:
        """AI-powered daily overview generation"""
        try:
            # Collect key summaries from each category
            overview_text = "Today's key developments:\n\n"
            
            for category, articles in articles_by_category.items():
                if not articles:
                    continue
                    
                # Get top 3 high-priority articles
                top_articles = [a for a in articles if a.get('priority') == 'high'][:3]
                if not top_articles:
                    top_articles = articles[:3]
                
                summaries = [a.get('aiSummary', a.get('title', '')) for a in top_articles]
                category_text = " ".join(summaries)
                
                if category_text:
                    overview_text += f"{category.upper()}: {category_text}\n\n"
            
            # Generate AI overview
            if len(overview_text) > 100:
                summary_result = self.summarizer(
                    overview_text,
                    max_length=200,
                    min_length=80,
                    do_sample=False,
                    truncation=True
                )
                return summary_result[0]['summary_text']
            
        except Exception as e:
            logger.warning(f"AI daily overview failed: {e}")
        
        return self._rule_daily_overview(articles_by_category)
    
    def _rule_daily_overview(self, articles_by_category: Dict[str, List]) -> str:
        """Rule-based daily overview generation"""
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
            return "📰 Your daily briefing is being prepared. Check back in a few minutes for the latest updates."
        
        overview = "🌅 Today's Intelligence Overview: " + "; ".join(overview_parts)
        overview += f". Total articles for review: {sum(len(articles) for articles in articles_by_category.values())}."
        
        return overview
