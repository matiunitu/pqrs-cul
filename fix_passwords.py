import sys
import os
import bcrypt
sys.path.append(os.path.abspath('app'))
from config.db_config import get_db_connection

conn = get_db_connection()
cur = conn.cursor()

# Get the default hashed password for '1234'
default_password = '1234'
hashed_pw = bcrypt.hashpw(default_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

cur.execute("UPDATE usuarios SET password_hash = %s WHERE password_hash IS NULL", (hashed_pw,))
conn.commit()
print(f"Updated {cur.rowcount} users with a default password of 1234")
conn.close()
