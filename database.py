import sqlite3
import json # <--- ADDED IMPORT
from grok_api import rank_lead

def init_db():
    conn = sqlite3.connect('leads.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            company TEXT NOT NULL DEFAULT '',
            email TEXT NOT NULL,
            description TEXT DEFAULT '',
            score INTEGER,
            message TEXT,
            status TEXT DEFAULT 'New',
            contacted BOOLEAN DEFAULT 0,
            responded BOOLEAN DEFAULT 0,
            interested BOOLEAN DEFAULT 0,
            meeting_time TEXT,
            sale_completed BOOLEAN DEFAULT 0,
            follow_up_count INTEGER DEFAULT 0,
            sent_messages TEXT DEFAULT '',
            gender TEXT,
            age INTEGER,
            profession TEXT,
            industry TEXT,
            income_level TEXT,
            location TEXT,
            preferred_contact TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_lead(name, email, company='', description='', gender=None, age=None, profession=None, industry=None, income_level=None, location=None, preferred_contact=None):
    conn = sqlite3.connect('leads.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO leads (name, company, email, description, gender, age, profession, industry, income_level, location, preferred_contact)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (name, company, email, description, gender, age, profession, industry, income_level, location, preferred_contact))
    conn.commit()
    lead_id = cursor.lastrowid
    conn.close()
    return lead_id

def update_score(lead_id, score):
    conn = sqlite3.connect('leads.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE leads SET score = ? WHERE id = ?', (score, lead_id))
    conn.commit()
    conn.close()

def update_message(lead_id, message):
    conn = sqlite3.connect('leads.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE leads SET message = ? WHERE id = ?', (message, lead_id))
    conn.commit()
    conn.close()

def update_status(lead_id, status):
    conn = sqlite3.connect('leads.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE leads SET status = ? WHERE id = ?', (status, lead_id))
    conn.commit()
    conn.close()

def get_all_leads(search=None, sort_by='score', sort_order='DESC', limit=10, offset=0):
    conn = sqlite3.connect('leads.db')
    cursor = conn.cursor()
    query = 'SELECT * FROM leads'
    params = []
    if search:
        query += ' WHERE name LIKE ? OR company LIKE ? OR email LIKE ?'
        search_term = f'%{search}%'
        params.extend([search_term, search_term, search_term])
    query += f' ORDER BY {sort_by} {sort_order}'
    if limit is not None:
        query += ' LIMIT ? OFFSET ?'
        params.extend([limit, offset])
    cursor.execute(query, params)
    leads = cursor.fetchall()
    conn.close()
    return leads

def get_leads_count(search=None):
    conn = sqlite3.connect('leads.db')
    cursor = conn.cursor()
    query = 'SELECT COUNT(*) FROM leads'
    params = []
    if search:
        query += ' WHERE name LIKE ? OR company LIKE ? OR email LIKE ?'
        search_term = f'%{search}%'
        params.extend([search_term, search_term, search_term])
    cursor.execute(query, params)
    count = cursor.fetchone()[0]
    conn.close()
    return count

def get_lead_by_id(lead_id):
    conn = sqlite3.connect('leads.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM leads WHERE id = ?', (lead_id,))
    lead = cursor.fetchone()
    conn.close()
    return lead

def update_contacted(lead_id, contacted):
    conn = sqlite3.connect('leads.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE leads SET contacted = ? WHERE id = ?', (contacted, lead_id))
    conn.commit()
    conn.close()

def update_responded(lead_id, responded):
    conn = sqlite3.connect('leads.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE leads SET responded = ? WHERE id = ?', (responded, lead_id))
    conn.commit()
    conn.close()

def update_interested(lead_id, interested):
    conn = sqlite3.connect('leads.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE leads SET interested = ? WHERE id = ?', (interested, lead_id))
    conn.commit()
    conn.close()

def update_meeting_time(lead_id, meeting_time):
    conn = sqlite3.connect('leads.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE leads SET meeting_time = ? WHERE id = ?', (meeting_time, lead_id))
    conn.commit()
    conn.close()

def update_sale_completed(lead_id, sale_completed):
    conn = sqlite3.connect('leads.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE leads SET sale_completed = ? WHERE id = ?', (sale_completed, lead_id))
    conn.commit()
    conn.close()

def increment_follow_up(lead_id):
    conn = sqlite3.connect('leads.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE leads SET follow_up_count = follow_up_count + 1 WHERE id = ?', (lead_id,))
    conn.commit()
    conn.close()

# --- REPLACED/IMPROVED FUNCTION ---
def append_message(lead_id, new_message):
    """
    Appends a new message to the sent_messages list, storing it as a JSON string.
    This replaces the old string concatenation logic for robust message history.
    """
    conn = sqlite3.connect('leads.db')
    cursor = conn.cursor()
    
    # 1. Fetch the current sent_messages JSON string
    cursor.execute('SELECT sent_messages FROM leads WHERE id = ?', (lead_id,))
    fetch_result = cursor.fetchone()
    current_json = fetch_result[0] if fetch_result else None

    # 2. Convert JSON string to Python list
    messages_list = []
    if current_json:
        try:
            # If there's existing data, load it.
            messages_list = json.loads(current_json)
        except json.JSONDecodeError:
            # If the stored data is not valid JSON (e.g., old raw text), treat it as an empty list to start fresh
            messages_list = []
    
    # 3. Append the new message
    messages_list.append(new_message)
    
    # 4. Convert the updated list back to a JSON string
    updated_json = json.dumps(messages_list)

    # 5. Save the new JSON string back to the database
    cursor.execute('UPDATE leads SET sent_messages = ? WHERE id = ?', (updated_json, lead_id))
    conn.commit()
    conn.close()

def get_ranking_desc():
    conn = sqlite3.connect('leads.db')
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM settings WHERE key = 'ranking_description'")
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else ''

def set_ranking_desc(ranking_desc):
    conn = sqlite3.connect('leads.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO settings (key, value)
        VALUES ('ranking_description', ?)
    """, (ranking_desc,))
    conn.commit()
    conn.close()

def re_score_all(ranking_desc):
    leads = get_all_leads(limit=None)
    for lead in leads:
        lead_id = lead[0]
        lead_data = f"Name: {lead[1]}, Email: {lead[3]}, Gender: {lead[15] or 'N/A'}, Age: {lead[16] or 'N/A'}, Profession: {lead[17] or 'N/A'}, Industry: {lead[18] or 'N/A'}, Income Level: {lead[19] or 'N/A'}, Location: {lead[20] or 'N/A'}, Preferred Contact: {lead[21] or 'N/A'}"
        if ranking_desc:
            try:
                score = rank_lead(lead_data, ranking_desc)
                update_score(lead_id, score)
            except Exception as e:
                print(f"Error re-scoring lead ID {lead_id}: {str(e)}")
                pass  # Skip if error

# Initialize the database on import
init_db()