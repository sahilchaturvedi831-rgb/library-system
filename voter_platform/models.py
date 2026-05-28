import sqlite3
from config import Config

def init_db():
    """Initialize database with all required tables"""
    conn = sqlite3.connect(Config.DB_FILE)
    c = conn.cursor()
    
    # Voters table
    c.execute('''CREATE TABLE IF NOT EXISTS voters (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        voter_id TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        age INTEGER,
        gender TEXT,
        phone TEXT,
        email TEXT,
        address TEXT,
        booth_id INTEGER,
        constituency TEXT,
        ward TEXT,
        voter_segment TEXT,
        profile_score REAL DEFAULT 0,
        engagement_level TEXT DEFAULT 'low',
        turnout_prediction REAL DEFAULT 0.5,
        sentiment_score REAL DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (booth_id) REFERENCES booths(id)
    )''')
    
    # Booths table
    c.execute('''CREATE TABLE IF NOT EXISTS booths (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        booth_name TEXT NOT NULL,
        location TEXT,
        constituency TEXT,
        ward TEXT,
        total_voters INTEGER DEFAULT 0,
        assigned_volunteers INTEGER DEFAULT 0,
        priority_score REAL DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Issues table
    c.execute('''CREATE TABLE IF NOT EXISTS issues (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        category TEXT,
        priority TEXT DEFAULT 'medium',
        status TEXT DEFAULT 'open',
        reported_by INTEGER,
        assigned_to INTEGER,
        booth_id INTEGER,
        votes INTEGER DEFAULT 1,
        sentiment REAL DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        resolved_at TIMESTAMP,
        FOREIGN KEY (reported_by) REFERENCES volunteers(id),
        FOREIGN KEY (assigned_to) REFERENCES volunteers(id),
        FOREIGN KEY (booth_id) REFERENCES booths(id)
    )''')
    
    # Schemes table
    c.execute('''CREATE TABLE IF NOT EXISTS schemes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        category TEXT,
        eligibility TEXT,
        benefits TEXT,
        target_voters INTEGER DEFAULT 0,
        enrolled_voters INTEGER DEFAULT 0,
        status TEXT DEFAULT 'active',
        start_date TEXT,
        end_date TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Scheme enrollments
    c.execute('''CREATE TABLE IF NOT EXISTS scheme_enrollments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        voter_id INTEGER NOT NULL,
        scheme_id INTEGER NOT NULL,
        enrollment_date TEXT,
        status TEXT DEFAULT 'enrolled',
        FOREIGN KEY (voter_id) REFERENCES voters(id),
        FOREIGN KEY (scheme_id) REFERENCES schemes(id),
        UNIQUE(voter_id, scheme_id)
    )''')
    
    # Volunteers table
    c.execute('''CREATE TABLE IF NOT EXISTS volunteers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT,
        email TEXT,
        constituency TEXT,
        ward TEXT,
        assigned_booths TEXT,
        role TEXT DEFAULT 'volunteer',
        tasks_completed INTEGER DEFAULT 0,
        performance_score REAL DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Communications table
    c.execute('''CREATE TABLE IF NOT EXISTS communications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        voter_id INTEGER NOT NULL,
        message TEXT NOT NULL,
        channel TEXT DEFAULT 'sms',
        status TEXT DEFAULT 'sent',
        sent_by INTEGER,
        response TEXT,
        sentiment REAL DEFAULT 0,
        sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (voter_id) REFERENCES voters(id),
        FOREIGN KEY (sent_by) REFERENCES volunteers(id)
    )''')
    
    # Analytics cache table
    c.execute('''CREATE TABLE IF NOT EXISTS analytics_cache (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cache_key TEXT UNIQUE NOT NULL,
        data TEXT,
        computed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(Config.DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def query_db(query, args=(), one=False):
    """Execute a SELECT query and return results"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(query, args)
    rv = cur.fetchall()
    conn.close()
    return (rv[0] if rv else None) if one else rv

def execute_db(query, args=()):
    """Execute an INSERT/UPDATE/DELETE query"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(query, args)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
