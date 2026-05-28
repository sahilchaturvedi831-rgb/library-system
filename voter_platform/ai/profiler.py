import random
from datetime import datetime, timedelta

class VoterProfiler:
    """AI-powered voter profiling to categorize and score voters"""
    
    def __init__(self):
        self.segments = {
            'youth_urban': {'name': 'Urban Youth', 'age_range': (18, 35), 'engagement': 'high'},
            'middle_class': {'name': 'Middle Class Families', 'age_range': (30, 50), 'engagement': 'medium'},
            'senior_citizen': {'name': 'Senior Citizens', 'age_range': (60, 100), 'engagement': 'low'},
            'rural_farmer': {'name': 'Rural Farmers', 'age_range': (25, 70), 'engagement': 'medium'},
            'working_class': {'name': 'Working Class', 'age_range': (20, 55), 'engagement': 'low'},
            'professional': {'name': 'Urban Professionals', 'age_range': (25, 45), 'engagement': 'high'}
        }
    
    def profile_voter(self, voter_data):
        """
        Profile a voter based on their demographic data
        Returns profile score and segment
        """
        age = voter_data.get('age', 0)
        constituency = voter_data.get('constituency', '').lower()
        
        # Determine segment based on age and location
        segment = self._determine_segment(age, constituency)
        
        # Calculate profile score (0-100)
        profile_score = self._calculate_profile_score(voter_data, segment)
        
        # Determine engagement level
        engagement = self._predict_engagement(age, profile_score)
        
        return {
            'voter_segment': segment,
            'profile_score': profile_score,
            'engagement_level': engagement,
            'recommended_approach': self._get_recommended_approach(segment, engagement)
        }
    
    def _determine_segment(self, age, constituency):
        """Determine voter segment based on age and location"""
        if age < 35:
            if 'urban' in constituency or 'city' in constituency:
                return 'youth_urban'
            return 'rural_farmer'
        elif age < 50:
            if 'urban' in constituency or 'city' in constituency:
                return 'professional'
            return 'middle_class'
        else:
            return 'senior_citizen'
    
    def _calculate_profile_score(self, voter_data, segment):
        """Calculate profile completeness score"""
        score = 0
        required_fields = ['name', 'age', 'phone', 'constituency', 'ward']
        
        for field in required_fields:
            if voter_data.get(field):
                score += 20
        
        # Boost score based on segment
        if self.segments.get(segment, {}).get('engagement') == 'high':
            score = min(100, score + 10)
        
        return score
    
    def _predict_engagement(self, age, profile_score):
        """Predict voter engagement level"""
        if profile_score > 80:
            if age < 35:
                return 'high'
            elif age < 55:
                return 'medium'
            else:
                return 'medium'
        elif profile_score > 50:
            return 'medium'
        else:
            return 'low'
    
    def _get_recommended_approach(self, segment, engagement):
        """Get recommended outreach approach"""
        approaches = {
            ('youth_urban', 'high'): 'Social media campaigns, WhatsApp groups',
            ('youth_urban', 'medium'): 'Digital ads, college campus outreach',
            ('youth_urban', 'low'): 'SMS campaigns, community events',
            ('middle_class', 'high'): 'Door-to-door, community meetings',
            ('middle_class', 'medium'): 'Local events, family outreach',
            ('middle_class', 'low'): 'Phone calls, WhatsApp messages',
            ('senior_citizen', 'high'): 'Door-to-door, family coordination',
            ('senior_citizen', 'medium'): 'Phone calls, community centers',
            ('senior_citizen', 'low'): 'Personal visits, assistance programs',
            ('rural_farmer', 'high'): 'Gram panchayat meetings, field visits',
            ('rural_farmer', 'medium'): 'Agricultural events, cooperative societies',
            ('rural_farmer', 'low'): 'Community leaders, radio campaigns',
            ('working_class', 'high'): 'Workplace outreach, digital campaigns',
            ('working_class', 'medium'): 'Evening meetings, family coordination',
            ('working_class', 'low'): 'SMS, community gatherings',
            ('professional', 'high'): 'LinkedIn, professional associations',
            ('professional', 'medium'): 'Evening events, digital campaigns',
            ('professional', 'low'): 'Email, professional networks'
        }
        return approaches.get((segment, engagement), 'General outreach')
    
    def bulk_profile(self, voters):
        """Profile multiple voters"""
        return [self.profile_voter(voter) for voter in voters]
