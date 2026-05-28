from flask import Blueprint, jsonify, request
from models import query_db, execute_db

booths_bp = Blueprint('booths', __name__)

@booths_bp.route('/api/booths', methods=['GET'])
def get_booths():
    """Get all booths with optional filtering"""
    constituency = request.args.get('constituency')
    ward = request.args.get('ward')
    limit = request.args.get('limit', 100, type=int)
    offset = request.args.get('offset', 0, type=int)
    
    query = 'SELECT * FROM booths WHERE 1=1'
    params = []
    
    if constituency:
        query += ' AND constituency = ?'
        params.append(constituency)
    if ward:
        query += ' AND ward = ?'
        params.append(ward)
    
    query += ' LIMIT ? OFFSET ?'
    params.extend([limit, offset])
    
    booths = query_db(query, tuple(params))
    return jsonify([dict(row) for row in booths])

@booths_bp.route('/api/booths/<int:booth_id>', methods=['GET'])
def get_booth(booth_id):
    """Get a specific booth by ID"""
    booth = query_db('SELECT * FROM booths WHERE id = ?', (booth_id,), one=True)
    if not booth:
        return jsonify({"message": "Booth not found"}), 404
    
    # Get voter count for this booth
    voter_count = query_db('SELECT COUNT(*) as count FROM voters WHERE booth_id = ?', (booth_id,), one=True)
    
    booth_data = dict(booth)
    booth_data['voter_count'] = voter_count['count'] if voter_count else 0
    
    return jsonify(booth_data)

@booths_bp.route('/api/booths', methods=['POST'])
def add_booth():
    """Add a new booth"""
    data = request.json
    
    required_fields = ['booth_name']
    for field in required_fields:
        if field not in data:
            return jsonify({"message": f"Missing required field: {field}"}), 400
    
    query = '''INSERT INTO booths (
        booth_name, location, constituency, ward, total_voters, 
        assigned_volunteers, priority_score
    ) VALUES (?, ?, ?, ?, ?, ?, ?)'''
    
    execute_db(query, (
        data['booth_name'],
        data.get('location'),
        data.get('constituency'),
        data.get('ward'),
        data.get('total_voters', 0),
        data.get('assigned_volunteers', 0),
        data.get('priority_score', 0)
    ))
    
    booth = query_db('SELECT * FROM booths WHERE booth_name = ?', (data['booth_name'],), one=True)
    return jsonify({
        "message": f"Booth '{data['booth_name']}' added successfully",
        "booth": dict(booth)
    }), 201

@booths_bp.route('/api/booths/<int:booth_id>', methods=['PUT'])
def update_booth(booth_id):
    """Update booth information"""
    data = request.json
    
    booth = query_db('SELECT * FROM booths WHERE id = ?', (booth_id,), one=True)
    if not booth:
        return jsonify({"message": "Booth not found"}), 404
