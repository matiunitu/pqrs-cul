import psycopg2
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from config.db_config import get_db_connection
from models.estado_model import Estado


class EstadosController:
    def create_estado(self, estado: Estado):
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO estados (nombre_estado) VALUES (%s) RETURNING id_estado",
                (estado.nombre_estado,),
            )
            id_estado = cur.fetchone()[0]
            conn.commit()
            return {"id_estado": id_estado, "resultado": "Estado creado"}
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def get_estado(self, id_estado: int):
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT id_estado, nombre_estado FROM estados WHERE id_estado=%s", (id_estado,))
            r = cur.fetchone()
            if not r:
                raise HTTPException(status_code=404, detail="Estado no encontrado")
            return jsonable_encoder({"id_estado": r[0], "nombre_estado": r[1]})
        except psycopg2.Error as err:
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def get_estados(self):
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT id_estado, nombre_estado FROM estados")
            rows = cur.fetchall()
            return jsonable_encoder([{"id_estado": r[0], "nombre_estado": r[1]} for r in rows])
        except psycopg2.Error as err:
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def update_estado(self, id_estado: int, estado: Estado):
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("UPDATE estados SET nombre_estado=%s WHERE id_estado=%s", (estado.nombre_estado, id_estado))
            if cur.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="Estado no encontrado")
            conn.commit()
            return {"resultado": "Estado actualizado"}
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def delete_estado(self, id_estado: int):
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM estados WHERE id_estado=%s", (id_estado,))
            if cur.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="Estado no encontrado")
            conn.commit()
            return {"resultado": "Estado eliminado"}
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()
