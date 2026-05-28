import random
from collections import Counter

class SentimentAnalyzer:
    """AI-powered sentiment analysis for voter communications and issues"""
    
    def __init__(self):
        # Keywords for sentiment analysis
        self.positive_keywords = [
            'good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic',
            'happy', 'satisfied', 'helpful', 'support', 'benefit', 'improved',
            'better', 'progress', 'success', 'thank', 'thanks', 'appreciate',
            'love', 'like', 'positive', 'optimistic', 'hope', 'trust'
        ]
        
        self.negative_keywords = [
            'bad', 'terrible', 'awful', 'horrible', 'poor', 'worst', 'hate',
            'angry', 'frustrated', 'disappointed', 'unhappy', 'problem', 'issue',
            'complaint', 'concern', 'worry', 'fear', 'failed', 'broken',
            'neglect', 'ignore', 'corrupt', 'scam', 'fraud', 'lie'
        ]
        
        self.neutral_keywords = [
            'information', 'query', 'question', 'ask', 'wonder', 'check',
            'update', 'notify', 'report', 'status', 'progress', 'know'
        ]
    
    def analyze_text(self, text):
        """
        Analyze sentiment of given text
        Returns sentiment score between -1 (very negative) and 1 (very positive)
        """
        if not text:
            return 0
        
        text_lower = text.lower()
        words = text_lower.split()
        
        positive_count = sum(1 for word in words if word in self.positive_keywords)
        negative_count = sum(1 for word in words if word in self.negative_keywords)
        
        total = positive_count + negative_count
        
        if total == 0:
            return 0
        
        sentiment_score = (positive_count - negative_count) / total
        
        # Normalize to -1 to 1 range
        return max(-1, min(1, sentiment_score))
    
    def analyze_message(self, message_data):
        """
        Analyze a voter message/communication
        """
        message = message_data.get('message', '')
        sentiment = self.analyze_text(message)
        
        # Categorize sentiment
        if sentiment > 0.3:
            category = 'positive'
        elif sentiment < -0.3:
            category = 'negative'
        else:
            category = 'neutral'
        
        return {
            'sentiment_score': sentiment,
            'sentiment_category': category,
            'message_length': len(message),
            'key_phrases': self._extract_key_phrases(message)
        }
    
    def analyze_issue(self, issue_data):
        """
        Analyze an issue for sentiment and priority
        """
        title = issue_data.get('title', '')
        description = issue_data.get('description', '')
        
        combined_text = f"{title} {description}"
        sentiment = self.analyze_text(combined_text)
        
        # Determine priority based on sentiment and keywords
        priority = self._determine_priority(issue_data, sentiment)
        
        return {
            'sentiment_score': sentiment,
            'priority': priority,
            'urgency_level': self._calculate_urgency(sentiment, priority)
        }
    
    def _determine_priority(self, issue_data, sentiment):
        """Determine issue priority based on sentiment and content"""
        keywords = issue_data.get('title', '').lower() + ' ' + issue_data.get('description', '').lower()
        
        high_priority_words = ['emergency', 'urgent', 'critical', 'death', 'accident', 'violence']
        medium_priority_words = ['delay', 'problem', 'issue', 'complaint', 'missing']
        
        for word in high_priority_words:
            if word in keywords:
                return 'high'
        
        for word in medium_priority_words:
            if word in keywords:
                return 'medium'
        
        # Negative sentiment increases priority
        if sentiment < -0.5:
            return 'high'
        elif sentiment < 0:
            return 'medium'
        
        return issue_data.get('priority', 'medium')
    
    def _calculate_urgency(self, sentiment, priority):
        """Calculate urgency level"""
        urgency_map = {
            ('high', -1): 'critical',
            ('high', -0.5): 'high',
            ('high', 0): 'high',
            ('medium', -1): 'high',
            ('medium', -0.5): 'medium',
            ('medium', 0): 'medium',
            ('low', -1): 'medium',
            ('low', -0.5): 'low',
            ('low', 0): 'low'
        }
        return urgency_map.get((priority, sentiment), 'low')
    
    def _extract_key_phrases(self, text):
        """Extract important phrases from text"""
        words = text.lower().split()
        phrases = []
        
        # Simple bigram extraction
        for i in range(len(words) - 1):
            if words[i] not in self.neutral_keywords:
                phrases.append(f"{words[i]} {words[i+1]}")
        
        return phrases[:5]  # Return top 5
    
    def bulk_analyze(self, messages):
        """Analyze multiple messages"""
        return [self.analyze_message(msg) for msg in messages]
    
    def get_overall_sentiment(self, sentiment_scores):
        """Get overall sentiment from multiple scores"""
        if not sentiment_scores:
            return 0
        
        avg = sum(sentiment_scores) / len(sentiment_scores)
        
        if avg > 0.3:
            return 'positive'
        elif avg < -0.3:
            return 'negative'
        return 'neutral'
