import sqlite3

DB_NAME = "alerts.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        type TEXT,
        message TEXT,
        risk TEXT
    )
    """)

    conn.commit()
    conn.close()

def insert_alert(alert):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
    INSERT INTO alerts (timestamp, type, message, risk)
    VALUES (?, ?, ?, ?)
    """, (
        alert["timestamp"],
        alert["type"],
        alert["message"],
        alert["risk"]
    ))

    conn.commit()
    conn.close()

def get_alerts():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("SELECT timestamp, type, message, risk FROM alerts ORDER BY id DESC LIMIT 200")
    rows = c.fetchall()

    conn.close()

    return [
        {
            "timestamp": r[0],
            "type": r[1],
            "message": r[2],
            "risk": r[3]
        }
        for r in rows
    ]
def search_alerts(risk=None, query=None):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    sql = "SELECT timestamp, type, message, risk FROM alerts WHERE 1=1"
    params = []

    if risk:
        sql += " AND risk = ?"
        params.append(risk)

    if query:
        sql += " AND message LIKE ?"
        params.append(f"%{query}%")

    sql += " ORDER BY id DESC LIMIT 200"

    c.execute(sql, params)
    rows = c.fetchall()
    conn.close()

    return [
        {
            "timestamp": r[0],
            "type": r[1],
            "message": r[2],
            "risk": r[3]
        }
        for r in rows
    ]
