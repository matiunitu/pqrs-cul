import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "app"))
from config.db_config import get_db_connection
from config.jwt_config import hash_password

def run():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT id_rol FROM roles WHERE nombre_rol = 'admin' LIMIT 1")
    admin_rol_id = cur.fetchone()["id_rol"]

    cur.execute("SELECT id_programa FROM programas LIMIT 1")
    prog_row = cur.fetchone()
    prog_id = prog_row["id_programa"]

    hashed = hash_password("123456")

    cur.execute("SELECT id_usuario FROM usuarios WHERE LOWER(nombre) = 'juan' LIMIT 1")
    existing = cur.fetchone()

    if not existing:
        cur.execute("""
            INSERT INTO usuarios
                (nombre, tipo_documento, documento, correo, telefono, id_rol, id_programa,
                 password_hash, estado, activo)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, ("juan", "CC", "99999999", "juan@admin.com", "000-0000",
              admin_rol_id, prog_id, hashed, 1, True))
        conn.commit()
        print("USER 'juan' CREADO")
    else:
        cur.execute("""
            UPDATE usuarios
            SET password_hash = %s, estado = 1, id_rol = %s
            WHERE LOWER(nombre) = 'juan'
        """, (hashed, admin_rol_id))
        conn.commit()
        print("USER 'juan' ACTUALIZADO")
    conn.close()

if __name__ == "__main__":
    run()
