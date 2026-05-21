"""
seed_auth.py — Ejecutar UNA VEZ para:
  1. Agregar columnas estado/updated_at a las tablas
  2. Insertar roles base (admin, docente, estudiante)
  3. Crear/actualizar usuario demo: nelson / 1234 / admin
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "app"))

from config.db_config import get_db_connection
from config.jwt_config import hash_password


def run():
    conn = get_db_connection()
    cur = conn.cursor()

    # ── 1. Agregar columnas si no existen ──────────────────────────────────────
    alter_statements = [
        "ALTER TABLE roles        ADD COLUMN IF NOT EXISTS estado     SMALLINT  DEFAULT 1",
        "ALTER TABLE roles        ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
        "ALTER TABLE roles        ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
        "ALTER TABLE facultades   ADD COLUMN IF NOT EXISTS estado     SMALLINT  DEFAULT 1",
        "ALTER TABLE facultades   ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
        "ALTER TABLE facultades   ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
        "ALTER TABLE programas    ADD COLUMN IF NOT EXISTS estado     SMALLINT  DEFAULT 1",
        "ALTER TABLE programas    ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
        "ALTER TABLE programas    ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
        "ALTER TABLE dependencias ADD COLUMN IF NOT EXISTS estado     SMALLINT  DEFAULT 1",
        "ALTER TABLE dependencias ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
        "ALTER TABLE dependencias ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
        "ALTER TABLE tipospqrs    ADD COLUMN IF NOT EXISTS estado     SMALLINT  DEFAULT 1",
        "ALTER TABLE tipospqrs    ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
        "ALTER TABLE tipospqrs    ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
        "ALTER TABLE prioridades  ADD COLUMN IF NOT EXISTS estado     SMALLINT  DEFAULT 1",
        "ALTER TABLE prioridades  ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
        "ALTER TABLE prioridades  ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
        "ALTER TABLE usuarios     ADD COLUMN IF NOT EXISTS password_hash VARCHAR(255)",
        "ALTER TABLE usuarios     ADD COLUMN IF NOT EXISTS estado     SMALLINT  DEFAULT 1",
        "ALTER TABLE usuarios     ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
        "ALTER TABLE pqrs         ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
        "ALTER TABLE respuestas   ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
    ]

    for stmt in alter_statements:
        try:
            cur.execute(stmt)
            conn.commit()
            print(f"  OK  : {stmt[50:90]}...")
        except Exception as e:
            conn.rollback()
            print(f"  SKIP: {str(e)[:80]}")

    # ── 2. Función y triggers updated_at ──────────────────────────────────────
    try:
        cur.execute("""
            CREATE OR REPLACE FUNCTION update_updated_at_column()
            RETURNS TRIGGER AS $$
            BEGIN
              NEW.updated_at = CURRENT_TIMESTAMP;
              RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;
        """)
        conn.commit()
        print("  OK  : función update_updated_at_column creada")
    except Exception as e:
        conn.rollback()
        print(f"  SKIP función: {e}")

    for tabla in ["usuarios", "pqrs", "roles"]:
        tname = f"trg_{tabla}_updated_at"
        try:
            cur.execute(f"""
                DO $$ BEGIN
                  IF NOT EXISTS (SELECT 1 FROM pg_trigger WHERE tgname = '{tname}') THEN
                    CREATE TRIGGER {tname}
                      BEFORE UPDATE ON {tabla}
                      FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
                  END IF;
                END $$;
            """)
            conn.commit()
            print(f"  OK  : trigger {tname}")
        except Exception as e:
            conn.rollback()
            print(f"  SKIP trigger {tname}: {e}")

    # ── 3. Insertar roles base ─────────────────────────────────────────────────
    roles_base = [
        ("admin",      "Acceso total al sistema"),
        ("docente",    "Gestion de PQRS y respuestas"),
        ("estudiante", "Crear y consultar sus propias PQRS"),
    ]
    for nombre, desc in roles_base:
        cur.execute("SELECT id_rol FROM roles WHERE nombre_rol = %s", (nombre,))
        if not cur.fetchone():
            cur.execute(
                "INSERT INTO roles (nombre_rol, descripcion, estado) VALUES (%s, %s, 1)",
                (nombre, desc)
            )
            conn.commit()
            print(f"  ROL : '{nombre}' insertado")
        else:
            print(f"  ROL : '{nombre}' ya existe")

    # ── 4. Obtener id del rol admin ────────────────────────────────────────────
    cur.execute("SELECT id_rol FROM roles WHERE nombre_rol = 'admin' LIMIT 1")
    admin_row = cur.fetchone()
    if not admin_row:
        print("ERROR: no se encontro rol admin despues de insertarlo")
        conn.close()
        return
    admin_rol_id = admin_row["id_rol"]
    print(f"  INFO: id_rol admin = {admin_rol_id}")

    # ── 5. Asegurar programa demo ──────────────────────────────────────────────
    cur.execute("SELECT id_programa FROM programas LIMIT 1")
    prog_row = cur.fetchone()
    if not prog_row:
        cur.execute(
            "INSERT INTO facultades(nombre_facultad, descripcion, estado) VALUES ('Demo', 'Facultad demo', 1) RETURNING id_facultad"
        )
        fac = cur.fetchone()
        cur.execute(
            "INSERT INTO programas(nombre_programa, descripcion, id_facultad, estado) VALUES ('Ing. Demo', 'Demo', %s, 1) RETURNING id_programa",
            (fac["id_facultad"],)
        )
        prog_row = cur.fetchone()
        conn.commit()
        print(f"  INFO: programa creado id={prog_row['id_programa']}")
    else:
        print(f"  INFO: programa id={prog_row['id_programa']} ya existe")

    prog_id = prog_row["id_programa"]

    # ── 6. Crear / actualizar usuario nelson ───────────────────────────────────
    hashed = hash_password("1234")

    cur.execute("SELECT id_usuario FROM usuarios WHERE LOWER(nombre) = 'nelson' LIMIT 1")
    existing = cur.fetchone()

    if not existing:
        cur.execute("""
            INSERT INTO usuarios
                (nombre, tipo_documento, documento, correo, telefono, id_rol, id_programa,
                 password_hash, estado, activo)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, ("nelson", "CC", "00000001", "nelson@admin.com", "000-0000",
              admin_rol_id, prog_id, hashed, 1, True))
        conn.commit()
        print("  USER: 'nelson' CREADO (admin / 1234)")
    else:
        cur.execute("""
            UPDATE usuarios
            SET password_hash = %s,
                estado = 1,
                id_rol = %s,
                tipo_documento = COALESCE(NULLIF(TRIM(tipo_documento), ''), 'CC')
            WHERE LOWER(nombre) = 'nelson'
        """, (hashed, admin_rol_id))
        conn.commit()
        print("  USER: 'nelson' ACTUALIZADO (password=1234, rol=admin)")

    conn.close()
    print("\n✅ SEED COMPLETADO. Puedes iniciar sesion con:")
    print("   usuario: nelson")
    print("   password: 1234")
    print("   rol: admin")


if __name__ == "__main__":
    run()
