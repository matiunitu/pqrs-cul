import psycopg2
from psycopg2.extras import RealDictCursor

def get_db_connection():
    return psycopg2.connect(
        host="ep-fragrant-glitter-aig2qu6i-pooler.c-4.us-east-1.aws.neon.tech",
        port=5432,
        user="neondb_owner",
        password="npg_E0rTLVPGDin3",
        dbname="pqrsdb",
        sslmode="require",           
        cursor_factory=RealDictCursor 
    )