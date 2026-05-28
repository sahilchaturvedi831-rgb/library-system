import random
from datetime import datetime, timedelta

class PredictionEngine:
    """AI-powered predictions for voter turnout and swing analysis"""
    
    def __init__(self):
        self.historical_turnout = {
            'urban': 0.65,
            'rural': 0.72,
            'suburban': 0.68
        }
        
        self.swing_indicators = [
            'economic_conditions',
            'incumbent_performance',
            'local_issues',
            'campaign_activity',
            'opposition_strength'
        ]
    
    def predict_turnout(self, constituency, booth_id=None, historical_data=None):
        """
        Predict voter turnout for a constituency or booth
        Returns probability (0-1) and confidence level
        """
        # Base turnout from historical data
        location_type = self._get_location_type(constituency)
        base_turnout = self.historical_turnout.get(location_type, 0.65)
        
        # Adjust based on historical data if available
        if historical_data:
            avg_turnout = sum(historical_data) / len(historical_data)
            base_turnout = (base_turnout + avg_turnout) / 2
        
        # Add some variance based on time to election
        days_to_election = self._get_days_to_election()
        if days_to_election < 7:
            # Last minute surge
            base_turnout = min(0.95, base_turnout + random.uniform(0.05, 0.15))
        elif days_to_election < 30:
            base_turnout += random.uniform(-0.05, 0.05)
        
        # Booth-specific adjustment
        if booth_id:
            base_turnout += random.uniform(-0.1, 0.1)
        
        return {
            'turnout_prediction': round(base_turnout, 3),
            'confidence': self._calculate_confidence(historical_data, days_to_election),
            'location_type': location_type,
            'factors': self._get_turnout_factors(base_turnout)
        }
    
    def predict_voter_segment_turnout(self, voters):
        """
        Predict turnout by voter segment
        """
        segment_turnout = {}
        
        for voter in voters:
            segment = voter.get('voter_segment', 'unknown')
            if segment not in segment_turnout:
                segment_turnout[segment] = []
            
            # Base prediction for this segment
            base = self._get_segment_base_turnout(segment)
            segment_turnout[segment].append(base)
        
        # Calculate averages
        result = {}
        for segment, turnouts in segment_turnout.items():
            result[segment] = {
                'predicted_turnout': round(sum(turnouts) / len(turnouts), 3),
                'voter_count': len(turnouts),
                'confidence': 'medium'
            }
        
        return result
    
    def analyze_swing(self, constituency, previous_results=None):
        """
        Analyze swing potential for a constituency
        Returns swing probability and key factors
        """
        # Calculate base swing probability
        swing_probability = random.uniform(0.15, 0.35)
        
        # Adjust based on previous results if available
        if previous_results:
            margin = previous_results.get('margin', 0)
            if margin < 0.05:  # Very close race
                swing_probability += 0.2
            elif margin < 0.1:
                swing_probability += 0.1
        
        # Analyze factors
        factors = self._analyze_swing_factors(constituency)
        
        # Determine swing direction (simulated)
        swing_direction = random.choice(['favor_opposition', 'favor_incumbent', 'neutral'])
        
        return {
            'swing_probability': round(min(0.8, swing_probability), 3),
            'swing_direction': swing_direction,
            'swing_magnitude': self._calculate_swing_magnitude(swing_probability),
            'key_factors': factors,
            'recommendation': self._get_swing_recommendation(swing_probability, factors)
        }
    
    def predict_engagement(self, voter_data):
        """
        Predict voter engagement level and best outreach time
        """
        age = voter_data.get('age', 35)
        segment = voter_data.get('voter_segment', 'middle_class')
        
        # Best outreach time by segment
        outreach_times = {
            'youth_urban': ['evening', 'weekend'],
            'middle_class': ['evening', 'weekend'],
            'senior_citizen': ['morning', 'afternoon'],
            'rural_farmer': ['morning', 'evening'],
            'working_class': ['evening', 'weekend'],
            'professional': ['evening', 'lunchtime']
        }
        
        # Preferred channel by segment
        channels = {
            'youth_urban': ['whatsapp', 'instagram', 'sms'],
            'middle_class': ['whatsapp', 'sms', 'phone'],
            'senior_citizen': ['phone', 'door_visit', 'sms'],
            'rural_farmer': ['door_visit', 'phone', 'community'],
            'working_class': ['whatsapp', 'sms', 'phone'],
            'professional': ['email', 'whatsapp', 'linkedin']
        }
        
        return {
            'predicted_engagement': self._predict_engagement_level(age, segment),
            'best_outreach_time': outreach_times.get(segment, ['evening']),
            'preferred_channels': channels.get(segment, ['sms']),
            'follow_up_frequency': self._get_follow_up_frequency(segment)
        }
    
    def predict_issue_impact(self, issue_data):
        """
        Predict the electoral impact of an issue
        """
        category = issue_data.get('category', 'general')
        priority = issue_data.get('priority', 'medium')
        votes = issue_data.get('votes', 1)
        
        # Base impact by category
        impact_scores = {
            'infrastructure': 0.7,
            'water': 0.8,
            'electricity': 0.7,
            'roads': 0.6,
            'healthcare': 0.75,
            'education': 0.65,
            'employment': 0.85,
            'agriculture': 0.7,
            'general': 0.4
        }
        
        base_impact = impact_scores.get(category, 0.4)
        
        # Adjust by priority and votes
        if priority == 'high':
            base_impact += 0.15
        elif priority == 'low':
            base_impact -= 0.1
        
        # More votes = more impact
        votes_factor = min(0.2, votes * 0.02)
        base_impact += votes_factor
        
        return {
            'impact_score': round(min(1.0, base_impact), 3),
            'affected_voters_estimate': votes * random.randint(10, 50),
            'electoral_significance': self._get_electoral_significance(base_impact),
            'recommended_action': self._get_issue_recommendation(base_impact, category)
        }
    
    def _get_location_type(self, constituency):
        """Determine if location is urban, rural, or suburban"""
        constituency_lower = constituency.lower()
        if 'urban' in constituency_lower or 'city' in constituency_lower:
            return 'urban'
        elif 'rural' in constituency_lower or 'village' in constituency_lower:
            return 'rural'
        return 'suburban'
    
    def _get_days_to_election(self):
        """Simulate days to next election (for demo)"""
        return random.randint(30, 180)
    
    def _calculate_confidence(self, historical_data, days_to_election):
        """Calculate confidence level of prediction"""
        if historical_data and len(historical_data) > 5:
            return 'high'
        elif historical_data or days_to_election < 30:
            return 'medium'
        return 'low'
    
    def _get_turnout_factors(self, turnout):
        """Get factors affecting turnout"""
        factors = []
        if turnout > 0.7:
            factors.append('High voter enthusiasm')
        if turnout < 0.6:
            factors.append('Potential voter apathy')
        factors.append('Weather may affect turnout')
        return factors
    
    def _get_segment_base_turnout(self, segment):
        """Get base turnout by segment"""
        base_turnouts = {
            'youth_urban': 0.58,
            'middle_class': 0.72,
            'senior_citizen': 0.78,
            'rural_farmer': 0.75,
            'working_class': 0.62,
            'professional': 0.68
        }
        return base_turnouts.get(segment, 0.65)
    
    def _analyze_swing_factors(self, constituency):
        """Analyze factors affecting swing"""
        return {
            'economic_conditions': random.uniform(0.3, 0.7),
            'incumbent_performance': random.uniform(0.3, 0.7),
            'local_issues': random.uniform(0.4, 0.8),
            'campaign_activity': random.uniform(0.3, 0.7),
            'opposition_strength': random.uniform(0.3, 0.7)
        }
    
    def _calculate_swing_magnitude(self, probability):
        """Calculate swing magnitude"""
        if probability > 0.6:
            return 'high'
        elif probability > 0.3:
            return 'medium'
        return 'low'
    
    def _get_swing_recommendation(self, probability, factors):
        """Get recommendation based on swing analysis"""
        if probability > 0.6:
            return 'Focus resources here - high swing potential'
        elif probability > 0.3:
            return 'Moderate investment recommended'
        return 'Low priority - maintain minimal presence'
    
    def _predict_engagement_level(self, age, segment):
        """Predict engagement level"""
        if age < 30:
            return random.choice(['high', 'medium'])
        elif age < 50:
            return random.choice(['medium', 'low'])
        return random.choice(['medium', 'low'])
    
    def _get_follow_up_frequency(self, segment):
        """Get recommended follow-up frequency"""
        frequencies = {
            'youth_urban': 'weekly',
            'middle_class': 'biweekly',
            'senior_citizen': 'weekly',
            'rural_farmer': 'monthly',
            'working_class': 'biweekly',
            'professional': 'monthly'
        }
        return frequencies.get(segment, 'biweekly')
    
    def _get_electoral_significance(self, impact):
        """Get electoral significance level"""
        if impact > 0.8:
            return 'critical'
        elif impact > 0.6:
            return 'high'
        elif impact > 0.4:
            return 'medium'
        return 'low'
    
    def _get_issue_recommendation(self, impact, category):
        """Get recommendation for issue handling"""
        if impact > 0.7:
            return f'Urgent action needed - {category} is major concern'
        elif impact > 0.5:
            return f'Address {category} issues in campaign'
        return 'Monitor situation'
