"""
RPNews - AI Processing Module
Handles AI-powered summarization with open source LLMs
"""

import re
import logging
import os
from typing import Dict, List

logger = logging.getLogger(__name__)

class RPNewsAI:
    """Advanced AI news analysis with open source LLMs"""
    
    def __init__(self):
        self.ai_type = "enhanced_rules"
        self.ai_available = False
        self.ollama_available = False
        self.transformers_available = False
        logger.info("🤖 Initializing AI analysis system with open source models...")
        
        # Try Ollama first (best for local/self-hosted LLMs)
        try:
            import requests
            # Test if Ollama is running locally
            ollama_url = os.environ.get("OLLAMA_URL", "http://localhost:11434")
            response = requests.get(f"{ollama_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get("models", [])
                # Look for good summarization models
                preferred_models = ["llama3.2", "llama3.1", "mistral", "qwen2.5", "phi3"]
                self.ollama_model = None
                
                for model_info in models:
                    model_name = model_info.get("name", "").split(":")[0]
                    if model_name in preferred_models:
                        self.ollama_model = model_info.get("name")
                        break
                
                if not self.ollama_model and models:
                    # Use any available model as fallback
                    self.ollama_model = models[0].get("name")
                
                if self.ollama_model:
                    self.ollama_url = ollama_url
                    self.ai_available = True
                    self.ollama_available = True
                    self.ai_type = f"ollama_{self.ollama_model.split(':')[0]}"
                    logger.info(f"✅ Ollama model loaded: {self.ollama_model}")
                else:
                    logger.info("ℹ️ No suitable Ollama models found")
            else:
                logger.info("ℹ️ Ollama not accessible, trying Hugging Face...")
        except Exception as e:
            logger.info(f"ℹ️ Ollama not available: {e}")
        
        # Try Hugging Face Transformers if Ollama failed
        if not self.ai_available:
            try:
                from transformers import pipeline
                import torch
                
                # Choose model based on available memory/compute
                model_options = [
                    "facebook/bart-large-cnn",  # Best quality
                    "sshleifer/distilbart-cnn-12-6",  # Faster, good quality
                    "google/pegasus-xsum",  # Good for news
                    "t5-small"  # Lightweight fallback
                ]
                
                self.summarizer = None
                for model_name in model_options:
                    try:
                        logger.info(f"📦 Attempting to load {model_name}...")
                        self.summarizer = pipeline(
                            "summarization",
                            model=model_name,
                            device=-1,  # CPU only for deployment
                            max_length=1024
                        )
                        self.ai_available = True
                        self.transformers_available = True
                        self.ai_type = f"transformers_{model_name.split('/')[-1]}"
                        logger.info(f"✅ Transformers model loaded: {model_name}")
                        break
                    except Exception as model_error:
                        logger.warning(f"Failed to load {model_name}: {model_error}")
                        continue
                
                if not self.summarizer:
                    logger.info("📝 No transformers models available, using enhanced rules")
                    
            except ImportError:
                logger.info("📝 Transformers not available, using enhanced rule-based analysis")
            except Exception as e:
                logger.warning(f"⚠️ Transformers setup failed: {e}")
        
        # Log final configuration
        if self.ai_available:
            logger.info(f"🎯 AI System Ready: {self.ai_type}")
        else:
            logger.info("📝 Using enhanced rule-based analysis")
    
    def generate_summary(self, title: str, content: str, category: str) -> str:
        """Generate intelligent summary using best available open source AI"""
        if self.ollama_available:
            return self._ollama_summary(title, content, category)
        elif self.transformers_available:
            return self._transformers_summary(title, content, category)
        else:
            return self._smart_rule_summary(title, content, category)
    
    def _ollama_summary(self, title: str, content: str, category: str) -> str:
        """Generate summary using Ollama (local LLM)"""
        try:
            import requests
            
            # Clean content for API
            clean_content = self._clean_text(content)[:2000]  # Limit for local processing
            
            category_context = {
                "ai": "This is an AI and technology news article. Focus on technical developments, business impact, and implications for the AI industry.",
                "finance": "This is a financial news article. Focus on market impact, economic implications, and key financial metrics or changes.",
                "politics": "This is a political news article. Focus on policy implications, political developments, and potential societal impact."
            }
            
            context = category_context.get(category, "This is a news article.")
            
            prompt = f"""{context} 

Please provide a concise, informative 2-3 sentence summary that captures the key points and implications.

Title: {title}
Content: {clean_content}

Summary:"""
            
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.ollama_model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.3,
                        "top_p": 0.9,
                        "max_tokens": 150
                    }
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                summary = result.get("response", "").strip()
                
                # Clean up the response
                summary = summary.replace("Summary:", "").strip()
                
                # Add category prefix
                category_config = {
                    "ai": "🤖 AI Development",
                    "finance": "💰 Market Update",
                    "politics": "🏛️ Policy Update"
                }
                
                prefix = category_config.get(category, "📰 News Update")
                return f"{prefix}: {summary}"
            else:
                logger.warning(f"Ollama API error: {response.status_code}")
                return self._smart_rule_summary(title, content, category)
            
        except Exception as e:
            logger.warning(f"Ollama summary failed: {e}")
            return self._smart_rule_summary(title, content, category)
    
    def _transformers_summary(self, title: str, content: str, category: str) -> str:
        """Generate AI-powered summary using Hugging Face transformers"""
        try:
            # Clean and prepare text
            clean_content = self._clean_text(content)
            
            # Truncate to model limits
            words = clean_content.split()
            if len(words) > 500:  # Reduced for better performance
                clean_content = " ".join(words[:500])
            
            # Generate summary with appropriate length
            summary_result = self.summarizer(
                clean_content,
                max_length=120,
                min_length=40,
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
            logger.warning(f"Transformers summary failed: {e}")
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
        """Generate comprehensive daily overview using best available AI"""
        if self.ollama_available:
            return self._ollama_daily_overview(articles_by_category)
        elif self.transformers_available:
            return self._transformers_daily_overview(articles_by_category)
        else:
            return self._rule_daily_overview(articles_by_category)
    
    def _ollama_daily_overview(self, articles_by_category: Dict[str, List]) -> str:
        """Generate daily overview using Ollama"""
        try:
            import requests
            
            # Collect top headlines from each category
            overview_content = "Today's top news headlines:\n\n"
            
            for category, articles in articles_by_category.items():
                if not articles:
                    continue
                
                top_articles = articles[:3]  # Top 3 per category
                headlines = [f"- {a.get('title', '')}" for a in top_articles]
                overview_content += f"{category.upper()}:\n" + "\n".join(headlines) + "\n\n"
            
            prompt = f"""Based on these headlines, create a brief, engaging 2-3 sentence daily overview that highlights the most important themes and connections across AI, finance, and politics:

{overview_content}

Daily Overview:"""
            
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.ollama_model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.4,
                        "max_tokens": 200
                    }
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                overview = result.get("response", "").strip()
                overview = overview.replace("Daily Overview:", "").strip()
                return f"🌅 Today's Intelligence Overview: {overview}"
            
        except Exception as e:
            logger.warning(f"Ollama daily overview failed: {e}")
        
        return self._rule_daily_overview(articles_by_category)
    
    def _transformers_daily_overview(self, articles_by_category: Dict[str, List]) -> str:
        """AI-powered daily overview generation using transformers"""
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
                    max_length=150,
                    min_length=60,
                    do_sample=False,
                    truncation=True
                )
                return f"🌅 Today's Intelligence Overview: {summary_result[0]['summary_text']}"
            
        except Exception as e:
            logger.warning(f"Transformers daily overview failed: {e}")
        
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
