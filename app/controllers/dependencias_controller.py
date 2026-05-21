import psycopg2
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from config.db_config import get_db_connection
from models.dependencia_model import Dependencia


class DependenciasController:
    def create_dependencia(self, dependencia: Dependencia):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO dependencias (nombre_dependencia, descripcion) VALUES (%s, %s) RETURNING id_dependencia",
                (dependencia.nombre_dependencia, dependencia.descripcion),
            )
            id_dependencia = cursor.fetchone()[0]
            conn.commit()
            return {"id_dependencia": id_dependencia, "resultado": "Dependencia creada"}
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def get_dependencia(self, id_dependencia: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id_dependencia, nombre_dependencia, descripcion FROM dependencias WHERE id_dependencia = %s",
                (id_dependencia,),
            )
            result = cursor.fetchone()
            if not result:
                raise HTTPException(status_code=404, detail="Dependencia no encontrada")
            payload = {
                "id_dependencia": result[0],
                "nombre_dependencia": result[1],
                "descripcion": result[2],
            }
            return jsonable_encoder(payload)
        except psycopg2.Error as err:
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def get_dependencias(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id_dependencia, nombre_dependencia, descripcion FROM dependencias")
            results = cursor.fetchall()
            payload = [
                {"id_dependencia": r[0], "nombre_dependencia": r[1], "descripcion": r[2]} for r in results
            ]
            return jsonable_encoder(payload)
        except psycopg2.Error as err:
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def update_dependencia(self, id_dependencia: int, dependencia: Dependencia):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE dependencias SET nombre_dependencia=%s, descripcion=%s WHERE id_dependencia=%s",
                (dependencia.nombre_dependencia, dependencia.descripcion, id_dependencia),
            )
            if cursor.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="Dependencia no encontrada")
            conn.commit()
            return {"resultado": "Dependencia actualizada"}
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def delete_dependencia(self, id_dependencia: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM dependencias WHERE id_dependencia=%s", (id_dependencia,))
            if cursor.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="Dependencia no encontrada")
            conn.commit()
            return {"resultado": "Dependencia eliminada"}
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()
