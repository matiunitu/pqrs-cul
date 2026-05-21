import psycopg2
from psycopg2.extras import RealDictCursor
import bcrypt

conn = psycopg2.connect(
    host='ep-fragrant-glitter-aig2qu6i-pooler.c-4.us-east-1.aws.neon.tech',
    port=5432,
    user='neondb_owner',
    password='npg_E0rTLVPGDin3',
    dbname='pqrsdb',
    sslmode='require',
    cursor_factory=RealDictCursor
)
cur = conn.cursor()
cur.execute("""
    SELECT u.id_usuario, u.nombre, u.correo, u.documento, u.estado, u.activo,
           r.nombre_rol,
           u.password_hash
    FROM usuarios u
    LEFT JOIN roles r ON u.id_rol = r.id_rol
    ORDER BY u.id_usuario
""")
rows = cur.fetchall()
print(f"Total usuarios: {len(rows)}")
print("-"*100)

problemas = []

for r in rows:
    ph = r['password_hash']
    if ph is None:
        pw_status = "SIN_PASSWORD"
        problemas.append(r['id_usuario'])
    elif ph == '':
        pw_status = "VACIO"
        problemas.append(r['id_usuario'])
    elif ph.startswith('$2'):
        pw_status = "bcrypt_OK"
        # Verificar si la clave 1234 funciona
        try:
            ok_1234 = bcrypt.checkpw(b'1234', ph.encode('utf-8'))
        except Exception:
            ok_1234 = False
        pw_status += f" (1234={'SI' if ok_1234 else 'NO'})"
    else:
        pw_status = f"FORMATO_RARO: {ph[:20]}"
        problemas.append(r['id_usuario'])

    estado_ok = r['estado'] not in (0, False, None)
    activo_ok = r['activo'] not in (False, None, 0)
    
    flags = []
    if not estado_ok:
        flags.append("INACTIVO")
        if r['id_usuario'] not in problemas:
            problemas.append(r['id_usuario'])
    if not activo_ok:
        flags.append("ACTIVO=FALSE")

    flag_str = " *** " + ",".join(flags) if flags else ""
    
    print(f"ID:{r['id_usuario']:3} | {str(r['nombre']):<20} | rol:{str(r['nombre_rol']):<12} | estado:{r['estado']} | activo:{r['activo']} | pw:{pw_status}{flag_str}")

print()
print(f"IDs con problema: {problemas}")
conn.close()
