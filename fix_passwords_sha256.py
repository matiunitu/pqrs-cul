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

# Update anyone who has the old SHA-256 hash of '1234' to the new bcrypt hash
cur.execute("UPDATE usuarios SET password_hash = %s WHERE password_hash = '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4'", (hashed_pw,))
conn.commit()
print(f"Updated {cur.rowcount} users from SHA-256 to bcrypt")
conn.close()
