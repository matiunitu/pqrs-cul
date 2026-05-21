import psycopg2
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from config.db_config import get_db_connection
from models.historial_estados_model import HistorialEstados


class HistorialEstadosController:
    def create_historial_estados(self, historial: HistorialEstados):
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO historial_estados (fecha_cambio, id_pqrs, id_estado_anterior, id_estado_nuevo, cambiado_por) VALUES (%s, %s, %s, %s, %s) RETURNING id_historial",
                (historial.fecha_cambio, historial.id_pqrs, historial.id_estado_anterior, historial.id_estado_nuevo, historial.cambiado_por),
            )
            id_historial = cur.fetchone()[0]
            conn.commit()
            return {"id_historial": id_historial, "resultado": "Historial estado creado"}
        except psycopg2.IntegrityError as err:
            conn.rollback()
            raise HTTPException(status_code=400, detail=f"Integrity error: {str(err)}")
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def get_historial_estados(self, id_historial: int):
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT id_historial, fecha_cambio, id_pqrs, id_estado_anterior, id_estado_nuevo, cambiado_por FROM historial_estados WHERE id_historial=%s", (id_historial,))
            r = cur.fetchone()
            if not r:
                raise HTTPException(status_code=404, detail="Historial estado no encontrado")
            return jsonable_encoder({"id_historial": r[0], "fecha_cambio": r[1], "id_pqrs": r[2], "id_estado_anterior": r[3], "id_estado_nuevo": r[4], "cambiado_por": r[5]})
        except psycopg2.Error as err:
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def get_historiales_estados(self):
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT id_historial, fecha_cambio, id_pqrs, id_estado_anterior, id_estado_nuevo, cambiado_por FROM historial_estados")
            rows = cur.fetchall()
            return jsonable_encoder([
                {"id_historial": r[0], "fecha_cambio": r[1], "id_pqrs": r[2], "id_estado_anterior": r[3], "id_estado_nuevo": r[4], "cambiado_por": r[5]}
                for r in rows
            ])
        except psycopg2.Error as err:
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def update_historial_estados(self, id_historial: int, historial: HistorialEstados):
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(
                "UPDATE historial_estados SET fecha_cambio=%s, id_pqrs=%s, id_estado_anterior=%s, id_estado_nuevo=%s, cambiado_por=%s WHERE id_historial=%s",
                (historial.fecha_cambio, historial.id_pqrs, historial.id_estado_anterior, historial.id_estado_nuevo, historial.cambiado_por, id_historial),
            )
            if cur.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="Historial estado no encontrado")
            conn.commit()
            return {"resultado": "Historial estado actualizado"}
        except psycopg2.IntegrityError as err:
            conn.rollback()
            raise HTTPException(status_code=400, detail=f"Integrity error: {str(err)}")
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def delete_historial_estados(self, id_historial: int):
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM historial_estados WHERE id_historial=%s", (id_historial,))
            if cur.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="Historial estado no encontrado")
            conn.commit()
            return {"resultado": "Historial estado eliminado"}
        except psycopg2.IntegrityError as err:
            conn.rollback()
            raise HTTPException(status_code=400, detail=f"Integrity error: {str(err)}")
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()
