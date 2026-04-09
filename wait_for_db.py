import time
import psycopg2

while True:
    try:
        conn = psycopg2.connect(
            dbname="wedding",
            user="user",
            password="password",
            host="db",
            port="5432"
        )
        conn.close()
        print("✅ Database is ready!")
        break
    except:
        print("⏳ Waiting for DB...")
        time.sleep(2)
        