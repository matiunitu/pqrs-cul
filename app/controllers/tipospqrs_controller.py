import psycopg2
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from config.db_config import get_db_connection
from models.tipospqrs_model import Tipospqrs


class TipospqrsController:
    def create_tipospqrs(self, tipospqrs: Tipospqrs):
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO tipospqrs (nombre_tipospqrs, descripcion) VALUES (%s, %s) RETURNING id_tipospqrs",
                (tipospqrs.nombre_tipospqrs, tipospqrs.descripcion),
            )
            id_tipospqrs = cur.fetchone()[0]
            conn.commit()
            return {"id_tipospqrs": id_tipospqrs, "resultado": "Tipo PQRS creado"}
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def get_tipospqrs(self, id_tipospqrs: int):
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT id_tipospqrs, nombre_tipospqrs, descripcion FROM tipospqrs WHERE id_tipospqrs=%s", (id_tipospqrs,))
            r = cur.fetchone()
            if not r:
                raise HTTPException(status_code=404, detail="Tipo PQRS no encontrado")
            return jsonable_encoder({"id_tipospqrs": r[0], "nombre_tipospqrs": r[1], "descripcion": r[2]})
        except psycopg2.Error as err:
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def get_todos_tipospqrs(self):
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT id_tipospqrs, nombre_tipospqrs, descripcion FROM tipospqrs")
            rows = cur.fetchall()
            return jsonable_encoder([{"id_tipospqrs": r[0], "nombre_tipospqrs": r[1], "descripcion": r[2]} for r in rows])
        except psycopg2.Error as err:
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def update_tipospqrs(self, id_tipospqrs: int, tipospqrs: Tipospqrs):
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(
                "UPDATE tipospqrs SET nombre_tipospqrs=%s, descripcion=%s WHERE id_tipospqrs=%s",
                (tipospqrs.nombre_tipospqrs, tipospqrs.descripcion, id_tipospqrs),
            )
            if cur.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="Tipo PQRS no encontrado")
            conn.commit()
            return {"resultado": "Tipo PQRS actualizado"}
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def delete_tipospqrs(self, id_tipospqrs: int):
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM tipospqrs WHERE id_tipospqrs=%s", (id_tipospqrs,))
            if cur.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="Tipo PQRS no encontrado")
            conn.commit()
            return {"resultado": "Tipo PQRS eliminado"}
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()
