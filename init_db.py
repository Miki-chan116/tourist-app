import sqlite3

conn = sqlite3.connect("tourist.db")

with open("schema.sql", "r", encoding="utf-8") as f:
    schema = f.read()

conn.executescript(schema)
conn.commit()
conn.close()

print("tourist.db を作成しました")