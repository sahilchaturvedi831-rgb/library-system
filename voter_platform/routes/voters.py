from flask import Blueprint, jsonify, request
from models import query_db, execute_db
from ai.profiler import VoterProfiler

voters_bp = Blueprint('voters', __name__)
profiler = VoterProfiler()

@voters_bp.route('/api/voters', methods=['GET'])
def get_voters():
    """Get all voters with optional filtering"""
    constituency = request.args.get('constituency')
    ward = request.args.get('ward')
    segment = request.args.get('segment')
    limit = request.args.get('limit', 100, type=int)
    offset = request.args.get('offset', 0, type=int)
    
    query = 'SELECT * FROM voters WHERE 1=1'
    params = []
    
    if constituency:
        query += ' AND constituency = ?'
        params.append(constituency)
    if ward:
        query += ' AND ward = ?'
        params.append(ward)
    if segment:
        query += ' AND voter_segment = ?'
        params.append(segment)
    
    query += ' LIMIT ? OFFSET ?'
    params.extend([limit, offset])
    
    voters = query_db(query, tuple(params))
    return jsonify([dict(row) for row in voters])

@voters_bp.route('/api/voters/<int:voter_id>', methods=['GET'])
def get_voter(voter_id):
    """Get a specific voter by ID"""
    voter = query_db('SELECT * FROM voters WHERE id = ?', (voter_id,), one=True)
    if not voter:
        return jsonify({"message": "Voter not found"}), 404
    return jsonify(dict(voter))

@voters_bp.route('/api/voters', methods=['POST'])
def add_voter():
    """Add a new voter"""
    data = request.json
    
    required_fields = ['voter_id', 'name']
    for field in required_fields:
        if field not in data:
            return jsonify({"message": f"Missing required field: {field}"}), 400
    
    # Check for duplicate voter_id
    existing = query_db('SELECT * FROM voters WHERE voter_id = ?', (data['voter_id'],), one=True)
    if existing:
        return jsonify({"message": "Voter ID already exists"}), 400
    
    # Use AI to profile the voter
    profile = profiler.profile_voter(data)
    
    query = '''INSERT INTO voters (
        voter_id, name, age, gender, phone, email, address, 
        booth_id, constituency, ward, voter_segment, profile_score, 
        engagement_level, turnout_prediction, sentiment_score
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
    
    execute_db(query, (
        data['voter_id'],
        data['name'],
        data.get('age'),
        data.get('gender'),
        data.get('phone'),
        data.get('email'),
        data.get('address'),
        data.get('booth_id'),
        data.get('constituency'),
        data.get('ward'),
        profile['voter_segment'],
        profile['profile_score'],
        profile['engagement_level'],
        0.5,  # Default turnout prediction
        0     # Default sentiment score
    ))
    
    voter = query_db('SELECT * FROM voters WHERE voter_id = ?', (data['voter_id'],), one=True)
    return jsonify({
        "message": f"Voter '{data['name']}' added successfully",
        "voter": dict(voter),
        "profile": profile
    }), 201

@voters_bp.route('/api/voters/<int:voter_id>', methods=['PUT'])
def update_voter(voter_id):
    """Update voter information"""
    data = request.json
    
    voter = query_db('SELECT * FROM voters WHERE id = ?', (voter_id,), one=True)
    if not voter:
        return jsonify({"message": "Voter not found"}), 404
    
    # Update fields
    fields = []
    values = []
    for field in ['name', 'age', 'gender', 'phone', 'email', 'address', 'booth_id', 'constituency', 'ward']:
        if field in data:
            fields.append(f"{field} = ?")
            values.append(data[field])
    
    if fields:
        values.append(voter_id)
        query = f"UPDATE voters SET {', '.join(fields)} WHERE id = ?"
        execute_db(query, tuple(values))
    
    # Re-profile if demographic data changed
    updated_voter = query_db('SELECT * FROM voters WHERE id = ?', (voter_id,), one=True)
    profile = profiler.profile_voter(dict(updated_voter))
    
    # Update profile fields
    execute_db('''UPDATE voters SET voter_segment = ?, profile_score = ?, engagement_level = ? WHERE id = ?''',
               (profile['voter_segment'], profile['profile_score'], profile['engagement_level'], voter_id))
    
    return jsonify({
        "message": "Voter updated successfully",
        "profile": profile
    })

@voters_bp.route('/api/voters/<int:voter_id>', methods=['DELETE'])
def delete_voter(voter_id):
    """Delete a voter"""
    voter = query_db('SELECT * FROM voters WHERE id = ?', (voter_id,), one=True)
    if not voter:
        return jsonify({"message": "Voter not found"}), 404
    
    execute_db('DELETE FROM voters WHERE id = ?', (voter_id,))
    return jsonify({"message": f"Voter '{voter['name']}' deleted"})

@voters_bp.route('/api/voters/search', methods=['GET'])
def search_voters():
    """Search voters by name, voter_id, phone, or address"""
    query = request.args.get('q', '')
    if len(query) < 2:
        return jsonify({"message": "Search query must be at least 2 characters"}), 400
    
    results = query_db('''SELECT * FROM voters WHERE 
        name LIKE ? OR voter_id LIKE ? OR phone LIKE ? OR address LIKE ?
        LIMIT 50''', (f'%{query}%', f'%{query}%', f'%{query}%', f'%{query}%'))
    
    return jsonify([dict(row) for row in results])

@voters_bp.route('/api/voters/segments', methods=['GET'])
def get_voter_segments():
    """Get voter segment distribution"""
    results = query_db('''SELECT voter_segment, COUNT(*) as count, 
        AVG(profile_score) as avg_profile_score,
        AVG(turnout_prediction) as avg_turnout
        FROM voters GROUP BY voter_segment''')
    
    return jsonify([dict(row) for row in results])

@voters_bp.route('/api/voters/graph', methods=['GET'])
def get_voter_graph():
    """Get voter data for graph visualization"""
    # Get voters grouped by constituency and ward
    constituency_data = query_db('''SELECT constituency, ward, 
        COUNT(*) as voter_count,
        AVG(profile_score) as avg_engagement,
        AVG(turnout_prediction) as avg_turnout
        FROM voters 
        WHERE constituency IS NOT NULL
        GROUP BY constituency, ward''')
    
    return jsonify([dict(row) for row in constituency_data])

@voters_bp.route('/api/voters/bulk-profile', methods=['POST'])
def bulk_profile_voters():
    """Bulk profile multiple voters using AI"""
    data = request.json
    voter_ids = data.get('voter_ids', [])
    
    if not voter_ids:
        return jsonify({"message": "No voter IDs provided"}), 400
    
    placeholders = ','.join('?' * len(voter_ids))
    voters = query_db(f'SELECT * FROM voters WHERE id IN ({placeholders})', tuple(voter_ids))
    
    results = []
    for voter in voters:
        voter_dict = dict(voter)
        profile = profiler.profile_voter(voter_dict)
        results.append({
            "voter_id": voter['id'],
            "profile": profile
        })
    
    return jsonify(results)
