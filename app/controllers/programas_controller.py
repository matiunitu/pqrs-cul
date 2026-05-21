import psycopg2
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from config.db_config import get_db_connection
from models.programa_model import Programa


class ProgramasController:
    def create_programa(self, programa: Programa):
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO programas (nombre_programa, descripcion, id_facultad) VALUES (%s, %s, %s) RETURNING id_programa",
                (programa.nombre_programa, programa.descripcion, programa.id_facultad),
            )
            id_programa = cur.fetchone()[0]
            conn.commit()
            return {"id_programa": id_programa, "resultado": "Programa creado"}
        except psycopg2.IntegrityError as err:
            conn.rollback()
            raise HTTPException(status_code=400, detail=f"Integrity error: {str(err)}")
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def get_programa(self, id_programa: int):
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(
                "SELECT id_programa, nombre_programa, descripcion, id_facultad FROM programas WHERE id_programa=%s",
                (id_programa,),
            )
            r = cur.fetchone()
            if not r:
                raise HTTPException(status_code=404, detail="Programa no encontrado")
            return jsonable_encoder({
                "id_programa": r[0],
                "nombre_programa": r[1],
                "descripcion": r[2],
                "id_facultad": r[3],
            })
        except psycopg2.Error as err:
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def get_programas(self):
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT id_programa, nombre_programa, descripcion, id_facultad FROM programas")
            rows = cur.fetchall()
            return jsonable_encoder([
                {
                    "id_programa": r[0],
                    "nombre_programa": r[1],
                    "descripcion": r[2],
                    "id_facultad": r[3],
                }
                for r in rows
            ])
        except psycopg2.Error as err:
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def update_programa(self, id_programa: int, programa: Programa):
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(
                "UPDATE programas SET nombre_programa=%s, descripcion=%s, id_facultad=%s WHERE id_programa=%s",
                (programa.nombre_programa, programa.descripcion, programa.id_facultad, id_programa),
            )
            if cur.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="Programa no encontrado")
            conn.commit()
            return {"resultado": "Programa actualizado"}
        except psycopg2.IntegrityError as err:
            conn.rollback()
            raise HTTPException(status_code=400, detail=f"Integrity error: {str(err)}")
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def delete_programa(self, id_programa: int):
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM programas WHERE id_programa=%s", (id_programa,))
            if cur.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="Programa no encontrado")
            conn.commit()
            return {"resultado": "Programa eliminado"}
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()
