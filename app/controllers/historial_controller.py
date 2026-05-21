import psycopg2
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from config.db_config import get_db_connection
from models.historial_model import Historial


class HistorialController:
    def create_historial(self, historial: Historial):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO historial (id_usuario, accion, fecha, cambiado_por) VALUES (%s, %s, %s, %s) RETURNING id_historial",
                (historial.id_usuario, historial.accion, historial.fecha, historial.cambiado_por),
            )
            id_historial = cursor.fetchone()[0]
            conn.commit()
            return {"id_historial": id_historial, "resultado": "Historial creado"}
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def get_historial(self, id_historial: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id_historial, id_usuario, accion, fecha, cambiado_por FROM historial WHERE id_historial=%s",
                (id_historial,),
            )
            result = cursor.fetchone()
            if not result:
                raise HTTPException(status_code=404, detail="Historial no encontrado")
            payload = {
                "id_historial": result[0],
                "id_usuario": result[1],
                "accion": result[2],
                "fecha": result[3],
                "cambiado_por": result[4],
            }
            return jsonable_encoder(payload)
        except psycopg2.Error as err:
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def get_historiales(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id_historial, id_usuario, accion, fecha, cambiado_por FROM historial")
            results = cursor.fetchall()
            payload = [
                {
                    "id_historial": r[0],
                    "id_usuario": r[1],
                    "accion": r[2],
                    "fecha": r[3],
                    "cambiado_por": r[4],
                }
                for r in results
            ]
            return jsonable_encoder(payload)
        except psycopg2.Error as err:
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def update_historial(self, id_historial: int, historial: Historial):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE historial SET id_usuario=%s, accion=%s, fecha=%s, cambiado_por=%s WHERE id_historial=%s",
                (historial.id_usuario, historial.accion, historial.fecha, historial.cambiado_por, id_historial),
            )
            if cursor.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="Historial no encontrado")
            conn.commit()
            return {"resultado": "Historial actualizado"}
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def delete_historial(self, id_historial: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM historial WHERE id_historial=%s", (id_historial,))
            if cursor.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="Historial no encontrado")
            conn.commit()
            return {"resultado": "Historial eliminado"}
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()
