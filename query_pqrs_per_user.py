from app.config.db_config import get_db_connection

def main():
    conn = get_db_connection()
    cur = conn.cursor()
    user_ids = [2,15,16,17,19,20,27,28]
    placeholders = ','.join(['%s'] * len(user_ids))
    query = f'''
    SELECT u.id_usuario, u.nombre, COUNT(p.id_pqrs) as total_pqrs
    FROM usuarios u
    LEFT JOIN pqrs p ON u.id_usuario = p.id_usuario
    WHERE u.id_usuario IN ({placeholders})
    GROUP BY u.id_usuario, u.nombre
    ORDER BY u.id_usuario
    '''
    cur.execute(query, user_ids)
    rows = cur.fetchall()
    print("=== PQRS Count Per User ===")
    for row in rows:
        print(row)
    cur.close()
    conn.close()

if __name__ == '__main__':
    main()
