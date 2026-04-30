import sqlite3

conn = sqlite3.connect("clientes.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS clientes (
    id TEXT PRIMARY KEY,
    nombre TEXT,
    saldo REAL DEFAULT 0
)
""")

for i in range(1, 401):
    id_str = str(i).zfill(3)
    cursor.execute(
        "INSERT OR IGNORE INTO clientes (id, nombre, saldo) VALUES (?, ?, 0)",
        (id_str, "")
    )

conn.commit()
conn.close()

print("Clientes creados")