# Routes Module for Voter Intelligence Platform

from .voters import voters_bp
from .booths import booths_bp
from .issues import issues_bp
from .schemes import schemes_bp
from .analytics import analytics_bp
from .communications import communications_bp
from .volunteers import volunteers_bp

__all__ = [
    'voters_bp', 
    'booths_bp', 
    'issues_bp', 
    'schemes_bp', 
    'analytics_bp', 
    'communications_bp', 
    'volunteers_bp'
]
