from app.config.db_config import get_db_connection

def main():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT COUNT(*) as total_activos FROM usuarios WHERE estado = 1')
    row = cur.fetchone()
    print(row)
    cur.close()
    conn.close()

if __name__ == '__main__':
    main()
