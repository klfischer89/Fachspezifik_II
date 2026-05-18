import sqlite3
import requests

# read data with API
try:
    response = requests.get("")
    response.raise_for_status()
    todos = response.json()

    # establish connection to database todo
    conn = sqlite3.connect("todos.db")
    cursor = conn.cursor()

    # create table todo
    cursor.execute("""CREATE TABLE IF NOT EXISTS todo(
                   id INTEGER Primary Key,
                   title TEXT NOT NULL,
                   status TEXT NOT NULL)
                   """)
    conn.commit()
    print("Tabelle wurde angelegt (falls nicht bereits vorhanden).")

    # insert data requested by API into database
    for todo in todos[:50]:
        cursor.execute("""INSERT INTO todo (id, title, status) VALUES (?,?,?)""", (todo['id'], todo['title'], todo['completed']))
        conn.commit()
        print("Erfolgreich in Datenbank gespeichert.")

# Exception handling, considering API and database
except requests.exceptions.RequestException as e:
    print(f"Fehler beim Abrufen der API: {e}")
except sqlite3.Error as d:
    print(f"Datenbankfehler: {d}")

conn.close()

import logging

# monitoring the process. level for logging: DEBUG, INFO, WARNING, ERROR, CRITICAL, using INFO
logging.basicConfig(filename="app.log", level=logging.INFO, format="%(asctime) s - %(message) s")

try:
    result = 10/0
except ZeroDivisionError as e:
    logging.error("Fehler aufgetreten: &s", e)

# 3 attempts to take risky_opertaion
from tenacity import retry, wait_exponantial, stop_after_attempt
@retry(wait=wait_exponantial(multiplier=1, min=4, max=10), stop=stop_after_attempt(3))

def risky_operation():
    print("Versuche...")
    raise Exception("Fehler.")

try:
    risky_operation()
except Exception as e:
    print("Operation fehlgeschlagen.")