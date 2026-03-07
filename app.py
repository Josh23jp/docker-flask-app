import os
import psycopg2
from flask import Flask

app = Flask(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")


def get_db_connection():
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL is not set")
    return psycopg2.connect(DATABASE_URL)


@app.route("/")
def home():
    conn = get_db_connection()
    cur = conn.cursor()

    # 1) Create table if it doesn't exist
    cur.execute("""
        CREATE TABLE IF NOT EXISTS visits (
            id SERIAL PRIMARY KEY,
            visited_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
        );
    """)

    # 2) Insert a new visit
    cur.execute("INSERT INTO visits DEFAULT VALUES;")

    # 3) Read total count + latest visit time
    cur.execute("SELECT COUNT(*) FROM visits;")
    total = cur.fetchone()[0]

    cur.execute("SELECT visited_at FROM visits ORDER BY id DESC LIMIT 1;")
    last_visit = cur.fetchone()[0]

    conn.commit()
    cur.close()
    conn.close()

    return f"Visits: {total} | Last visit: {last_visit}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)