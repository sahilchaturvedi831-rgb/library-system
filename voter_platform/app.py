from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os
from datetime import datetime

from config import Config
from models import init_db, query_db, execute_db
from routes.voters import voters_bp
from routes.booths import booths_bp
from routes.issues import issues_bp
from routes.schemes import schemes_bp
from routes.analytics import analytics_bp
# Initialize database
init_db()

# Serve static frontend
@app.route('/')
def serve_index():
    static_path = os.path.join(os.path.dirname(__file__), 'static')
    return send_from_directory(static_path, 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    static_path = os.path.join(os.path.dirname(__file__), 'static')
    return send_from_directory(static_path, filename)

# Health check
@app.route('/api/health')
def health_check():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "platform": "Voter Intelligence Platform"
    })

if __name__ == "__main__":
    print("=" * 50)
    print("Voter Intelligence Platform - Web Server")
    print("=" * 50)
    print("\nTo access from other devices on your network:")
    print("1. Find your computer's IP address:")
    print("   - Windows: Run 'ipconfig' in CMD")
    print("   - Look for IPv4 Address (e.g., 192.168.1.x)")
    print("\n2. On another device, open browser and go to:")
    print("   http://YOUR_IP_ADDRESS:5000/")
    print("\nServer running on http://localhost:5000")
    print("=" * 50)
    app.run(host='0.0.0.0', port=5000, debug=True)
