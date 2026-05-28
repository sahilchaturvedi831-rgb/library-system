from flask import Blueprint, jsonify, request
from models import query_db, execute_db
from ai.sentiment import SentimentAnalyzer

issues_bp = Blueprint('issues', __name__)
sentiment = SentimentAnalyzer()

@issues_bp.route('/api/issues', methods=['GET'])
def get_issues():
    status = request.args.get('status')
    category = request.args.get('category')
    priority = request.args.get('priority')
    limit = request.args.get('limit', 100, type=int)
    
    query = 'SELECT * FROM issues WHERE 1=1'
    params = []
    
    if status:
        query += ' AND status = ?'
        params.append(status)
    if category:
        query += ' AND category = ?'
        params.append(category)
    if priority:
        query += ' AND priority = ?'
        params.append(priority)
    
    query += ' ORDER BY created_at DESC LIMIT ?'
    params.append(limit)
    
    issues = query_db(query, tuple(params))
    return jsonify([dict(row) for row in issues])

@issues_bp.route('/api/issues/<int:issue_id>', methods=['GET'])
def get_issue(issue_id):
    issue = query_db('SELECT * FROM issues WHERE id = ?', (issue_id,), one=True)
    if not issue:
        return jsonify({"message": "Issue not found"}), 404
    return jsonify(dict(issue))

@issues_bp.route('/api/issues', methods=['POST'])
def add_issue():
    data = request.json
    if not data.get('title'):
        return jsonify({"message": "Title is required"}), 400
    
    # Analyze sentiment
    analysis = sentiment.analyze_issue(data)
    
    query = '''INSERT INTO issues (title, description, category, priority, status, reported_by, booth_id, votes, sentiment)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'''
    
    execute_db(query, (
        data['title'], data.get('description'), data.get('category'), 
        analysis['priority'], 'open', data.get('reported_by'), 
        data.get('booth_id'), 1, analysis['sentiment_score']
    ))
    
    issue = query_db('SELECT * FROM issues ORDER BY id DESC LIMIT 1', one=True)
    return jsonify({"message": "Issue added", "issue": dict(issue), "analysis": analysis}), 201

@issues_bp.route('/api/issues/<int:issue_id>', methods=['PUT'])
def update_issue(issue_id):
    data = request.json
    issue = query_db('SELECT * FROM issues WHERE id = ?', (issue_id,), one=True)
    if not issue:
        return jsonify({"message": "Issue not found"}), 404
    
    fields = []
    values = []
    for field in ['title', 'description', 'category', 'priority', 'status', 'assigned_to', 'votes']:
        if field in data:
            fields.append(f"{field} = ?")
            values.append(data[field])
    
    if fields:
        values.append(issue_id)
        execute_db(f"UPDATE issues SET {', '.join(fields)} WHERE id = ?", tuple(values))
    
    return jsonify({"message": "Issue updated"})

@issues_bp.route('/api/issues/<int:issue_id>', methods=['DELETE'])
def delete_issue(issue_id):
    issue = query_db('SELECT * FROM issues WHERE id = ?', (issue_id,), one=True)
    if not issue:
        return jsonify({"message": "Issue not found"}), 404
    execute_db('DELETE FROM issues WHERE id = ?', (issue_id,))
    return jsonify({"message": "Issue deleted"})

@issues_bp.route('/api/issues/stats', methods=['GET'])
def get_issue_stats():
    total = query_db('SELECT COUNT(*) as count FROM issues', one=True)
    open_issues = query_db('SELECT COUNT(*) as count FROM issues WHERE status = "open"', one=True)
    by_category = query_db('SELECT category, COUNT(*) as count FROM issues GROUP BY category')
    by_priority = query_db('SELECT priority, COUNT(*) as count FROM issues GROUP BY priority')
    
    return jsonify({
        "total": total['count'] if total else 0,
        "open": open_issues['count'] if open_issues else 0,
        "by_category": [dict(row) for row in by_category],
        "by_priority": [dict(row) for row in by_priority]
    })
