import psycopg2
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from config.db_config import get_db_connection
from models.facultad_model import Facultad


class FacultadesController:
    def create_facultad(self, facultad: Facultad):
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO facultades (nombre_facultad, descripcion) VALUES (%s, %s) RETURNING id_facultad",
                (facultad.nombre_facultad, facultad.descripcion),
            )
            id_facultad = cur.fetchone()[0]
            conn.commit()
            return {"id_facultad": id_facultad, "resultado": "Facultad creada"}
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def get_facultad(self, id_facultad: int):
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(
                "SELECT id_facultad, nombre_facultad, descripcion FROM facultades WHERE id_facultad=%s",
                (id_facultad,),
            )
            result = cur.fetchone()
            if not result:
                raise HTTPException(status_code=404, detail="Facultad no encontrada")
            return jsonable_encoder({
                "id_facultad": result[0],
                "nombre_facultad": result[1],
                "descripcion": result[2],
            })
        except psycopg2.Error as err:
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def get_facultades(self):
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT id_facultad, nombre_facultad, descripcion FROM facultades")
            rows = cur.fetchall()
            return jsonable_encoder([
                {
                    "id_facultad": r[0],
                    "nombre_facultad": r[1],
                    "descripcion": r[2],
                }
                for r in rows
            ])
        except psycopg2.Error as err:
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def update_facultad(self, id_facultad: int, facultad: Facultad):
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(
                "UPDATE facultades SET nombre_facultad=%s, descripcion=%s WHERE id_facultad=%s",
                (facultad.nombre_facultad, facultad.descripcion, id_facultad),
            )
            if cur.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="Facultad no encontrada")
            conn.commit()
            return {"resultado": "Facultad actualizada"}
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def delete_facultad(self, id_facultad: int):
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM facultades WHERE id_facultad=%s", (id_facultad,))
            if cur.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="Facultad no encontrada")
            conn.commit()
            return {"resultado": "Facultad eliminada"}
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()
