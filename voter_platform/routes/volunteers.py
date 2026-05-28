from flask import Blueprint, jsonify, request
from models import query_db, execute_db

volunteers_bp = Blueprint('volunteers', __name__)

@volunteers_bp.route('/api/volunteers', methods=['GET'])
def get_volunteers():
    constituency = request.args.get('constituency')
    query = 'SELECT * FROM volunteers'
    params = []
    if constituency:
        query += ' WHERE constituency = ?'
        params.append(constituency)
    volunteers = query_db(query, tuple(params) if params else ())
    return jsonify([dict(row) for row in volunteers])

@volunteers_bp.route('/api/volunteers/<int:volunteer_id>', methods=['GET'])
def get_volunteer(volunteer_id):
    volunteer = query_db('SELECT * FROM volunteers WHERE id = ?', (volunteer_id,), one=True)
    if not volunteer:
        return jsonify({"message": "Volunteer not found"}), 404
    return jsonify(dict(volunteer))

@volunteers_bp.route('/api/volunteers', methods=['POST'])
def add_volunteer():
    data = request.json
    if not data.get('name'):
        return jsonify({"message": "Name is required"}), 400
    
    execute_db('''INSERT INTO volunteers (name, phone, email, constituency, ward, assigned_booths, role)
                  VALUES (?, ?, ?, ?, ?, ?, ?)''',
               (data['name'], data.get('phone'), data.get('email'), 
                data.get('constituency'), data.get('ward'), data.get('assigned_booths'), data.get('role', 'volunteer')))
    
    volunteer = query_db('SELECT * FROM volunteers ORDER BY id DESC LIMIT 1', one=True)
    return jsonify({"message": "Volunteer added", "volunteer": dict(volunteer)}), 201

@volunteers_bp.route('/api/volunteers/<int:volunteer_id>', methods=['PUT'])
def update_volunteer(volunteer_id):
    data = request.json
    fields = []
    values = []
    for field in ['name', 'phone', 'email', 'constituency', 'ward', 'assigned_booths', 'role', 'tasks_completed', 'performance_score']:
        if field in data:
            fields.append(f"{field} = ?")
            values.append(data[field])
    
    if fields:
        values.append(volunteer_id)
        execute_db(f"UPDATE volunteers SET {', '.join(fields)} WHERE id = ?", tuple(values))
    
    return jsonify({"message": "Volunteer updated"})

@volunteers_bp.route('/api/volunteers/<int:volunteer_id>', methods=['DELETE'])
def delete_volunteer(volunteer_id):
    volunteer = query_db('SELECT * FROM volunteers WHERE id = ?', (volunteer_id,), one=True)
    if not volunteer:
        return jsonify({"message": "Volunteer not found"}), 404
    execute_db('DELETE FROM volunteers WHERE id = ?', (volunteer_id,))
    return jsonify({"message": "Volunteer deleted"})
