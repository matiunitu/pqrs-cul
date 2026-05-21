from app.config.db_config import get_db_connection

def main():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id_usuario, nombre, (password_hash IS NOT NULL) as has_pw FROM usuarios ORDER BY id_usuario')
    rows = cur.fetchall()
    for r in rows:
        print(r)
    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
