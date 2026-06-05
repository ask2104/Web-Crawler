import sqlite3

def get_connection():
    return sqlite3.connect("search.db")

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS pages (
        url TEXT PRIMARY KEY,
        title TEXT,
        content TEXT
    )
    """)
    conn.commit()
    conn.close()

def insert_page(url, title, content):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT OR IGNORE INTO pages VALUES (?, ?, ?)", (url, title, content))
        conn.commit()
        conn.close()
    except:
        pass

def get_all_pages():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT url, title, content FROM pages")
    rows = cur.fetchall()
    conn.close()
    return rows

def get_pages(urls):
    conn = get_connection()
    cur = conn.cursor()
    results = []
    for u in urls:
        cur.execute("SELECT url, title, content FROM pages WHERE url=?", (u,))
        row = cur.fetchone()
        if row:
            results.append({
                "url": row[0],
                "title": row[1],
                "content": row[2]
            })
    conn.close()
    return results

init_db()