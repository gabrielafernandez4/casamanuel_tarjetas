import sqlite3

conn = sqlite3.connect("clientes.db")
cursor = conn.cursor()

# añadir columna nombre si no existe
try:
    cursor.execute("ALTER TABLE clientes ADD COLUMN nombre TEXT")
except:
    pass

# crear tabla historial
cursor.execute("""
CREATE TABLE IF NOT EXISTS historial (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id TEXT,
    fecha TEXT,
    total REAL,
    saldo_usado REAL,
    pagado REAL,
    bonus REAL
)
""")

conn.commit()
conn.close()

print("Base de datos actualizada")