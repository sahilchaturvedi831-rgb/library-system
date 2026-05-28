from flask import Blueprint, jsonify, request
from models import query_db, execute_db
from ai.sentiment import SentimentAnalyzer

communications_bp = Blueprint('communications', __name__)
sentiment = SentimentAnalyzer()

@communications_bp.route('/api/communications', methods=['GET'])
def get_communications():
    voter_id = request.args.get('voter_id', type=int)
    query = 'SELECT c.*, v.name as voter_name FROM communications c JOIN voters v ON c.voter_id = v.id'
    params = []
    if voter_id:
        query += ' WHERE c.voter_id = ?'
        params.append(voter_id)
    query += ' ORDER BY c.sent_at DESC LIMIT 100'
    comms = query_db(query, tuple(params) if params else ())
    return jsonify([dict(row) for row in comms])

@communications_bp.route('/api/communications', methods=['POST'])
def send_message():
    data = request.json
    if not data.get('voter_id') or not data.get('message'):
        return jsonify({"message": "voter_id and message are required"}), 400
    
    # Analyze sentiment
    analysis = sentiment.analyze_text(data['message'])
    
    execute_db('''INSERT INTO communications (voter_id, message, channel, status, sent_by, sentiment)
                  VALUES (?, ?, ?, ?, ?, ?)''',
               (data['voter_id'], data['message'], data.get('channel', 'sms'), 
                'sent', data.get('sent_by'), analysis))
    
    return jsonify({"message": "Message sent", "sentiment": analysis}), 201

@communications_bp.route('/api/communications/bulk', methods=['POST'])
def bulk_send():
    data = request.json
    voter_ids = data.get('voter_ids', [])
    message = data.get('message', '')
    channel = data.get('channel', 'sms')
    
    if not voter_ids or not message:
        return jsonify({"message": "voter_ids and message are required"}), 400
    
    analysis = sentiment.analyze_text(message)
    count = 0
    for voter_id in voter_ids:
        execute_db('''INSERT INTO communications (voter_id, message, channel, status, sentiment)
                      VALUES (?, ?, ?, 'sent', ?)''',
                   (voter_id, message, channel, analysis))
        count += 1
    
    return jsonify({"message": f"Message sent to {count} voters", "count": count})
