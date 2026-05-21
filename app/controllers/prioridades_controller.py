import psycopg2
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from config.db_config import get_db_connection
from models.prioridad_model import Prioridad


class PrioridadesController:
    def create_prioridad(self, prioridad: Prioridad):
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO prioridades (nombre_prioridad, nivel) VALUES (%s, %s) RETURNING id_prioridad",
                (prioridad.nombre_prioridad, prioridad.nivel),
            )
            id_prioridad = cur.fetchone()[0]
            conn.commit()
            return {"id_prioridad": id_prioridad, "resultado": "Prioridad creada"}
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def get_prioridad(self, id_prioridad: int):
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT id_prioridad, nombre_prioridad, nivel FROM prioridades WHERE id_prioridad=%s", (id_prioridad,))
            r = cur.fetchone()
            if not r:
                raise HTTPException(status_code=404, detail="Prioridad no encontrada")
            return jsonable_encoder({"id_prioridad": r[0], "nombre_prioridad": r[1], "nivel": r[2]})
        except psycopg2.Error as err:
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def get_prioridades(self):
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT id_prioridad, nombre_prioridad, nivel FROM prioridades")
            rows = cur.fetchall()
            return jsonable_encoder([{"id_prioridad": r[0], "nombre_prioridad": r[1], "nivel": r[2]} for r in rows])
        except psycopg2.Error as err:
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def update_prioridad(self, id_prioridad: int, prioridad: Prioridad):
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("UPDATE prioridades SET nombre_prioridad=%s, nivel=%s WHERE id_prioridad=%s", (prioridad.nombre_prioridad, prioridad.nivel, id_prioridad))
            if cur.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="Prioridad no encontrada")
            conn.commit()
            return {"resultado": "Prioridad actualizada"}
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def delete_prioridad(self, id_prioridad: int):
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM prioridades WHERE id_prioridad=%s", (id_prioridad,))
            if cur.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="Prioridad no encontrada")
            conn.commit()
            return {"resultado": "Prioridad eliminada"}
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()
