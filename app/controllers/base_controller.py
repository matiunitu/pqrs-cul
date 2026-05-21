import psycopg2
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from config.db_config import get_db_connection


class BaseController:
    """Clase base para todos los controladores con métodos CRUD comunes"""
    
    def execute_query(self, query, params=None, fetch_one=False, fetch_all=False):
        """Ejecuta una consulta SQL y retorna los resultados"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(query, params or ())
            
            if fetch_one:
                result = cursor.fetchone()
                conn.close()
                return result
            elif fetch_all:
                results = cursor.fetchall()
                conn.close()
                return results
            else:
                conn.commit()
                conn.close()
                return cursor.rowcount
        except psycopg2.IntegrityError as err:
            conn.rollback()
            conn.close()
            raise HTTPException(status_code=400, detail=f"Integrity error: {str(err)}")
        except psycopg2.Error as err:
            conn.rollback()
            conn.close()
            raise HTTPException(status_code=500, detail=str(err))

    def execute_returning_id(self, query, params=None):
        """Ejecuta una consulta INSERT RETURNING y retorna el ID"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(query, params or ())
            result = cursor.fetchone()
            conn.commit()
            conn.close()
            return result[0] if result else None
        except psycopg2.IntegrityError as err:
            conn.rollback()
            conn.close()
            raise HTTPException(status_code=400, detail=f"Integrity error: {str(err)}")
        except psycopg2.Error as err:
            conn.rollback()
            conn.close()
            raise HTTPException(status_code=500, detail=str(err))
