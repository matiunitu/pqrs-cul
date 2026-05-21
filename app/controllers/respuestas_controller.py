import psycopg2
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from config.db_config import get_db_connection
from models.respuesta_model import Respuesta


class RespuestasController:
    def create_respuesta(self, respuesta: Respuesta):
        try:
            conn = get_db_connection()
            cur = conn.cursor()

            # 1. Insertar la respuesta
            cur.execute(
                "INSERT INTO respuestas (mensaje, fecha_respuesta, id_pqrs, id_usuario) VALUES (%s, %s, %s, %s) RETURNING id_respuesta",
                (respuesta.mensaje, respuesta.fecha_respuesta, respuesta.id_pqrs, respuesta.id_usuario),
            )
            id_respuesta = cur.fetchone()[0]

            # 2. Cambiar el estado de la PQRS a 'Resuelto' automáticamente
            # Busca el estado con nombre 'Resuelto' (prioridad) o 'Respondido'
            cur.execute("""
                SELECT id_estado FROM estados
                WHERE LOWER(nombre_estado) = 'resuelto'
                LIMIT 1
            """)
            estado = cur.fetchone()
            if not estado:
                cur.execute("""
                    SELECT id_estado FROM estados
                    WHERE LOWER(nombre_estado) LIKE '%respond%'
                    LIMIT 1
                """)
                estado = cur.fetchone()

            if estado and respuesta.id_pqrs:
                cur.execute(
                    "UPDATE pqrs SET id_estado = %s WHERE id_pqrs = %s",
                    (estado[0], respuesta.id_pqrs)
                )

            conn.commit()
            return {"id_respuesta": id_respuesta, "resultado": "Respuesta creada y PQRS marcada como Resuelta"}
        except psycopg2.IntegrityError as err:
            conn.rollback()
            raise HTTPException(status_code=400, detail=f"Integrity error: {str(err)}")
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def get_respuesta(self, id_respuesta: int):
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT id_respuesta, mensaje, fecha_respuesta, id_pqrs, id_usuario FROM respuestas WHERE id_respuesta=%s", (id_respuesta,))
            r = cur.fetchone()
            if not r:
                raise HTTPException(status_code=404, detail="Respuesta no encontrada")
            return jsonable_encoder({"id_respuesta": r[0], "mensaje": r[1], "fecha_respuesta": r[2], "id_pqrs": r[3], "id_usuario": r[4]})
        except psycopg2.Error as err:
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def get_respuestas(self):
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT id_respuesta, mensaje, fecha_respuesta, id_pqrs, id_usuario FROM respuestas")
            rows = cur.fetchall()
            return jsonable_encoder([{"id_respuesta": r[0], "mensaje": r[1], "fecha_respuesta": r[2], "id_pqrs": r[3], "id_usuario": r[4]} for r in rows])
        except psycopg2.Error as err:
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def update_respuesta(self, id_respuesta: int, respuesta: Respuesta):
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("UPDATE respuestas SET mensaje=%s, fecha_respuesta=%s, id_pqrs=%s, id_usuario=%s WHERE id_respuesta=%s", (respuesta.mensaje, respuesta.fecha_respuesta, respuesta.id_pqrs, respuesta.id_usuario, id_respuesta))
            if cur.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="Respuesta no encontrada")
            conn.commit()
            return {"resultado": "Respuesta actualizada"}
        except psycopg2.IntegrityError as err:
            conn.rollback()
            raise HTTPException(status_code=400, detail=f"Integrity error: {str(err)}")
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def delete_respuesta(self, id_respuesta: int):
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM respuestas WHERE id_respuesta=%s", (id_respuesta,))
            if cur.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="Respuesta no encontrada")
            conn.commit()
            return {"resultado": "Respuesta eliminada"}
        except psycopg2.IntegrityError as err:
            conn.rollback()
            raise HTTPException(status_code=400, detail=f"Integrity error: {str(err)}")
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()
