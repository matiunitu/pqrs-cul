"""
Diagnostico: simular exactamente el flujo de auth_controller.login
paso a paso para detectar donde falla.
"""
import sys
sys.path.insert(0, 'app')

from config.db_config import get_db_connection
from config.jwt_config import verify_password

USERNAME = "nelson"
PASSWORD = "1234"

print(f"Simulando login para: username='{USERNAME}', password='{PASSWORD}'")
print("-" * 60)

conn = get_db_connection()
cur = conn.cursor()

cur.execute("""
    SELECT u.id_usuario, u.nombre, u.password_hash, u.estado,
           r.nombre_rol
    FROM   usuarios u
    JOIN   roles r ON u.id_rol = r.id_rol
    WHERE  LOWER(u.nombre) = LOWER(%s)
       OR LOWER(u.correo) = LOWER(%s)
       OR u.documento = %s
    LIMIT  1
""", (USERNAME, USERNAME, USERNAME))

row = cur.fetchone()
conn.close()

if not row:
    print("RESULTADO: Usuario NO encontrado en la BD")
else:
    print(f"Usuario encontrado: ID={row['id_usuario']}, nombre='{row['nombre']}'")
    print(f"Estado: {row['estado']}")
    ph = row['password_hash']
    print(f"Password hash: {repr(ph[:50]) if ph else 'NINGUNO'}...")
    
    # Verificar estado
    if row['estado'] in (0, False, None):
        print("RESULTADO: FALLO - usuario inactivo")
    elif not ph:
        print("RESULTADO: FALLO - sin password_hash")
    else:
        result = verify_password(PASSWORD, ph)
        print(f"verify_password('{PASSWORD}', hash) = {result}")
        if result:
            print("RESULTADO: LOGIN DEBERIA FUNCIONAR correctamente")
        else:
            print("RESULTADO: FALLO - verify_password retorno False")
            # Probar directamente con bcrypt
            import bcrypt
            try:
                direct = bcrypt.checkpw(PASSWORD.encode('utf-8'), ph.encode('utf-8'))
                print(f"bcrypt.checkpw directo = {direct}")
            except Exception as ex:
                print(f"Error bcrypt directo: {ex}")
            
            # Mostrar tipo del hash
            print(f"Tipo password_hash: {type(ph)}")
            print(f"Hash completo: {ph}")
