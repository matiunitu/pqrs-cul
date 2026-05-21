from app.config.db_config import get_db_connection

def main():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id_usuario, nombre, estado FROM usuarios ORDER BY id_usuario LIMIT 20')
    rows = cur.fetchall()
    for r in rows:
        print(r)
    cur.close()
    conn.close()

if __name__ == '__main__':
    main()
