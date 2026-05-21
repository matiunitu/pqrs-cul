"""
Script de auto-reparacion: detecta y arregla usuarios sin password_hash
y verifica que todos los usuarios pueden iniciar sesion con sus credenciales.
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

DEFAULT_PASSWORD = '1234'


def hash_pw(plain: str) -> str:
    return bcrypt.hashpw(plain.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def verify_pw(plain: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(plain.encode('utf-8'), hashed.encode('utf-8'))
    except Exception:
        return False


def main():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    print("=" * 70)
    print("  AUTO-REPARACION DE USUARIOS")
    print("=" * 70)

    # 1. Traer todos los usuarios
    cur.execute("""
        SELECT u.id_usuario, u.nombre, u.correo, u.documento,
               u.estado, u.activo, u.password_hash,
               r.nombre_rol
        FROM usuarios u
        LEFT JOIN roles r ON u.id_rol = r.id_rol
        ORDER BY u.id_usuario
    """)
    usuarios = cur.fetchall()
    print(f"\nTotal usuarios en BD: {len(usuarios)}")

    reparados = []
    ok = []
    con_problemas = []

    for u in usuarios:
        uid = u['id_usuario']
        nombre = u['nombre']
        ph = u['password_hash']

        # Detectar si necesita reparacion
        necesita_repair = False
        razon = []

        if ph is None or ph == '':
            necesita_repair = True
            razon.append("SIN_PASSWORD")
        elif not ph.startswith('$2'):
            necesita_repair = True
            razon.append(f"FORMATO_INVALIDO({ph[:15]})")

        if necesita_repair:
            # Reparar: asignar password por defecto '1234'
            nuevo_hash = hash_pw(DEFAULT_PASSWORD)
            cur.execute(
                "UPDATE usuarios SET password_hash = %s WHERE id_usuario = %s",
                (nuevo_hash, uid)
            )
            reparados.append({
                'id': uid,
                'nombre': nombre,
                'razon': ', '.join(razon),
                'nuevo_pw': DEFAULT_PASSWORD
            })
            print(f"  [REPARADO] ID:{uid:3} | {nombre:<20} | Razon: {', '.join(razon)} -> password seteado a '{DEFAULT_PASSWORD}'")
        else:
            # Verificar que la clave 1234 funciona (para usuarios con bcrypt OK)
            pw_ok = verify_pw(DEFAULT_PASSWORD, ph)
            ok.append({'id': uid, 'nombre': nombre, 'pw_1234_ok': pw_ok})

    conn.commit()

    print(f"\n{'='*70}")
    print(f"  RESUMEN DE REPARACION")
    print(f"{'='*70}")
    print(f"  Usuarios reparados : {len(reparados)}")
    print(f"  Usuarios OK        : {len(ok)}")
    print()

    # 2. Verificar login simulado para TODOS los usuarios
    print("  VERIFICACION DE LOGIN (prueba con contrasena '1234')")
    print(f"  {'-'*60}")

    # Refrescar datos tras reparacion
    cur.execute("""
        SELECT u.id_usuario, u.nombre, u.correo, u.estado, u.activo,
               u.password_hash, r.nombre_rol
        FROM usuarios u
        LEFT JOIN roles r ON u.id_rol = r.id_rol
        ORDER BY u.id_usuario
    """)
    usuarios_post = cur.fetchall()

    login_ok = []
    login_fail = []

    for u in usuarios_post:
        uid = u['id_usuario']
        nombre = u['nombre']
        ph = u['password_hash']
        estado = u['estado']
        activo = u['activo']
        rol = u['nombre_rol']

        # Verificar estado
        if estado in (0, False, None):
            login_fail.append((uid, nombre, rol, "USUARIO_INACTIVO"))
            print(f"  [FAIL] ID:{uid:3} | {nombre:<20} | rol:{str(rol):<12} | USUARIO_INACTIVO")
            continue

        # Verificar password
        if not ph:
            login_fail.append((uid, nombre, rol, "SIN_PASSWORD"))
            print(f"  [FAIL] ID:{uid:3} | {nombre:<20} | rol:{str(rol):<12} | SIN_PASSWORD")
            continue

        pw_ok = verify_pw(DEFAULT_PASSWORD, ph)
        if pw_ok:
            login_ok.append((uid, nombre, rol))
            print(f"  [ OK ] ID:{uid:3} | {nombre:<20} | rol:{str(rol):<12} | login con '1234': OK")
        else:
            login_fail.append((uid, nombre, rol, "PASSWORD_DISTINTO_A_1234"))
            print(f"  [WARN] ID:{uid:3} | {nombre:<20} | rol:{str(rol):<12} | login con '1234': NO (tiene otra contrasena, eso es normal)")

    print(f"\n{'='*70}")
    print(f"  Pueden iniciar sesion con '1234': {len(login_ok)}")
    print(f"  Con contrasena diferente o inactivos: {len(login_fail)}")
    print(f"{'='*70}")

    if reparados:
        print(f"\n  USUARIOS REPARADOS (contrasena reseteada a '{DEFAULT_PASSWORD}'):")
        for r in reparados:
            print(f"    - ID:{r['id']} | {r['nombre']} | Razon: {r['razon']}")

    print("\n  Reparacion completada exitosamente.")
    conn.close()


if __name__ == '__main__':
    main()
