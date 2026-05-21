import sys
import os
sys.path.append(os.path.abspath('app'))
from config.db_config import get_db_connection

conn = get_db_connection()
cur = conn.cursor()
cur.execute("SELECT id_usuario, nombre, id_rol, password_hash FROM usuarios ORDER BY id_usuario DESC LIMIT 5;")
for row in cur.fetchall():
    print(row)
conn.close()
