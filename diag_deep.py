"""
Diagnostico profundo: verificar que la BD tiene passwords validos
y que la logica de verify_password funciona igual que en auth_controller.
"""
import psycopg2
from psycopg2.extras import RealDictCursor
import bcrypt

DB_CONFIG = dict(
    host='ep-fragrant-glitter-aig2qu6i-pooler.c-4.us-east-1.aws.neon.tech',
    port=5432,
    user='neondb_owner',
    password='npg_E0rTLVPGDin3',
    dbname='pqrsdb',
    sslmode='require',
    cursor_factory=RealDictCursor
)

conn = psycopg2.connect(**DB_CONFIG)
cur = conn.cursor()

cur.execute("""
    SELECT u.id_usuario, u.nombre, u.password_hash, u.estado
    FROM usuarios u
    ORDER BY u.id_usuario
    LIMIT 5
""")
rows = cur.fetchall()

print("Verificacion directa de bcrypt contra la BD:")
print("-" * 60)
for r in rows:
    ph = r['password_hash']
    nombre = r['nombre']
    if not ph:
        print(f"  {nombre}: SIN PASSWORD HASH")
        continue
    
    # Exactamente igual que jwt_config.verify_password
    try:
        result = bcrypt.checkpw('1234'.encode('utf-8'), ph.encode('utf-8'))
        print(f"  {nombre}: bcrypt.checkpw('1234') = {result}")
        print(f"    hash en BD: {ph[:40]}...")
    except Exception as ex:
        print(f"  {nombre}: ERROR en checkpw: {ex}")
        print(f"    hash en BD: {repr(ph[:60])}")

conn.close()

# Ahora probar haciendo login via HTTP directamente con requests
print()
print("Probando via HTTP:")
import urllib.request, json

def login_http(username, password):
    body = json.dumps({"username": username, "password": password}).encode()
    req = urllib.request.Request(
        "http://127.0.0.1:8000/auth/login",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read())
        except:
            return e.code, {}
    except Exception as ex:
        return None, str(ex)

import urllib.error
status, resp = login_http("nelson", "1234")
print(f"  nelson/1234 -> HTTP {status}: {resp}")
