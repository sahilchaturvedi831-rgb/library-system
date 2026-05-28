from flask import Blueprint, jsonify, request
from models import query_db, execute_db

schemes_bp = Blueprint('schemes', __name__)

@schemes_bp.route('/api/schemes', methods=['GET'])
def get_schemes():
    status = request.args.get('status')
    category = request.args.get('category')
    schemes = query_db('SELECT * FROM schemes' + (' WHERE status = ?' if status else ''), 
                      (status,) if status else (), one=False)
    return jsonify([dict(row) for row in schemes])

@schemes_bp.route('/api/schemes/<int:scheme_id>', methods=['GET'])
def get_scheme(scheme_id):
    scheme = query_db('SELECT * FROM schemes WHERE id = ?', (scheme_id,), one=True)
    if not scheme:
        return jsonify({"message": "Scheme not found"}), 404
    return jsonify(dict(scheme))

@schemes_bp.route('/api/schemes', methods=['POST'])
def add_scheme():
    data = request.json
    if not data.get('name'):
        return jsonify({"message": "Name is required"}), 400
    
    query = '''INSERT INTO schemes (name, description, category, eligibility, benefits, target_voters, status, start_date, end_date)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'''
    execute_db(query, (data['name'], data.get('description'), data.get('category'), 
                     data.get('eligibility'), data.get('benefits'), data.get('target_voters', 0),
                     data.get('status', 'active'), data.get('start_date'), data.get('end_date')))
    
    scheme = query_db('SELECT * FROM schemes ORDER BY id DESC LIMIT 1', one=True)
    return jsonify({"message": "Scheme added", "scheme": dict(scheme)}), 201

@schemes_bp.route('/api/schemes/<int:scheme_id>/enroll', methods=['POST'])
def enroll_voter(scheme_id):
    data = request.json
    voter_id = data.get('voter_id')
    
    scheme = query_db('SELECT * FROM schemes WHERE id = ?', (scheme_id,), one=True)
    if not scheme:
        return jsonify({"message": "Scheme not found"}), 404
    
    existing = query_db('SELECT * FROM scheme_enrollments WHERE voter_id = ? AND scheme_id = ?', (voter_id, scheme_id), one=True)
    if existing:
        return jsonify({"message": "Voter already enrolled"}), 400
    
    execute_db('INSERT INTO scheme_enrollments (voter_id, scheme_id, enrollment_date, status) VALUES (?, ?, datetime("now"), "enrolled")',
               (voter_id, scheme_id))
    execute_db('UPDATE schemes SET enrolled_voters = enrolled_voters + 1 WHERE id = ?', (scheme_id,))
    
    return jsonify({"message": "Voter enrolled successfully"})

@schemes_bp.route('/api/schemes/<int:scheme_id>/enrollments', methods=['GET'])
def get_enrollments(scheme_id):
    enrollments = query_db('''SELECT se.*, v.name as voter_name, v.voter_id as voter_number 
                             FROM scheme_enrollments se 
                             JOIN voters v ON se.voter_id = v.id 
                             WHERE se.scheme_id = ?''', (scheme_id,))
    return jsonify([dict(row) for row in enrollments])
