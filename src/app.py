import os
from flask import Flask
import pymysql
from pymysql.err import OperationalError

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_USER = os.getenv("DB_USER", "user")
DB_PASS = os.getenv("DB_PASS", "password")
DB_NAME = os.getenv("DB_NAME", "testdb")


def get_conn():
    return pymysql.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASS, database=DB_NAME, cursorclass=pymysql.cursors.DictCursor)


@app.route("/")
def hello():
    try:
        conn = get_conn()
    except OperationalError as e:
        return f"Hola Mundo — error BD: {e}", 500

    with conn:
        with conn.cursor() as cur:
            cur.execute("CREATE TABLE IF NOT EXISTS greetings (id INT AUTO_INCREMENT PRIMARY KEY, message VARCHAR(255))")
            cur.execute("SELECT message FROM greetings ORDER BY id DESC LIMIT 1")
            row = cur.fetchone()
            if not row:
                cur.execute("INSERT INTO greetings (message) VALUES ('Hola Mundo desde MySQL')")
                conn.commit()
                message = "Hola Mundo desde MySQL (creado)"
            else:
                message = row['message']

    return message


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
