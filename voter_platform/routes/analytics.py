from flask import Blueprint, jsonify, request
from models import query_db, execute_db
from ai.predictions import PredictionEngine

analytics_bp = Blueprint('analytics', __name__)
predictions = PredictionEngine()

@analytics_bp.route('/api/analytics/turnout', methods=['GET'])
def get_turnout_prediction():
    constituency = request.args.get('constituency')
    booth_id = request.args.get('booth_id', type=int)
    historical = [0.65, 0.70, 0.68]  # Sample historical data
    
    result = predictions.predict_turnout(constituency or 'General', booth_id, historical)
    return jsonify(result)

@analytics_bp.route('/api/analytics/swing', methods=['GET'])
def get_swing_analysis():
    constituency = request.args.get('constituency', 'General')
    result = predictions.analyze_swing(constituency)
    return jsonify(result)

@analytics_bp.route('/api/analytics/segments', methods=['GET'])
def get_segment_analysis():
    segments = query_db('''SELECT voter_segment, COUNT(*) as count, 
                          AVG(profile_score) as avg_score, AVG(turnout_prediction) as avg_turnout
                          FROM voters GROUP BY voter_segment''')
    return jsonify([dict(row) for row in segments])

@analytics_bp.route('/api/analytics/dashboard', methods=['GET'])
def get_dashboard():
    total_voters = query_db('SELECT COUNT(*) as count FROM voters', one=True)
    total_booths = query_db('SELECT COUNT(*) as count FROM booths', one=True)
    total_issues = query_db('SELECT COUNT(*) as count FROM issues', one=True)
    open_issues = query_db('SELECT COUNT(*) as count FROM issues WHERE status = "open"', one=True)
    
    segment_dist = query_db('SELECT voter_segment, COUNT(*) as count FROM voters GROUP BY voter_segment')
    
    return jsonify({
        "total_voters": total_voters['count'] if total_voters else 0,
        "total_booths": total_booths['count'] if total_booths else 0,
        "total_issues": total_issues['count'] if total_issues else 0,
        "open_issues": open_issues['count'] if open_issues else 0,
        "segment_distribution": [dict(row) for row in segment_dist]
    })
