import sqlite3
import datetime
DB_FILE = "chats.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS chats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER,
            role TEXT,
            content TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(chat_id) REFERENCES chats(id)
        )
    ''')
    conn.commit()
    conn.close()

def create_new_chat():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    title = f"Chat {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    c.execute("INSERT INTO chats (title) VALUES (?)", (title,))
    chat_id = c.lastrowid
    conn.commit()
    conn.close()
    return chat_id

def get_all_chats():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT id, title FROM chats ORDER BY id DESC")
    chats = c.fetchall()
    conn.close()
    return chats

def get_messages(chat_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT role, content FROM messages WHERE chat_id = ? ORDER BY id", (chat_id,))
    messages = c.fetchall()
    conn.close()
    return messages

def save_message(chat_id, role, content):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO messages (chat_id, role, content) VALUES (?, ?, ?)", (chat_id, role, content))
    conn.commit()
    conn.close()


def system_prompt() -> str:
    return """ You are a friendly and helpful personal assistant for Juma. 
Juma is curious and works on different kinds of digital projects. 
He likes clear, simple answers and sometimes needs help with tasks, organizing things, or solving problems. 
Keep the conversation casual, ask if you're not sure, and always try to be useful and respectful."""