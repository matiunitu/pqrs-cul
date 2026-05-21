import psycopg2
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from config.db_config import get_db_connection
from models.rol_model import Rol


class RolesController:
    def create_role(self, role: Rol):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO roles (nombre_rol, descripcion) VALUES (%s, %s) RETURNING id_rol",
                (role.nombre_rol, role.descripcion),
            )
            id_rol = cursor.fetchone()[0]
            conn.commit()
            return {"id_rol": id_rol, "resultado": "Rol creado"}
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def get_role(self, id_rol: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id_rol, nombre_rol, descripcion FROM roles WHERE id_rol = %s",
                (id_rol,),
            )
            result = cursor.fetchone()
            if not result:
                raise HTTPException(status_code=404, detail="Rol no encontrado")
            payload = {
                "id_rol": result[0],
                "nombre_rol": result[1],
                "descripcion": result[2],
            }
            return jsonable_encoder(payload)
        except psycopg2.Error as err:
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def get_roles(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id_rol, nombre_rol, descripcion FROM roles")
            results = cursor.fetchall()
            payload = []
            for r in results:
                payload.append({"id_rol": r[0], "nombre_rol": r[1], "descripcion": r[2]})
            return jsonable_encoder(payload)
        except psycopg2.Error as err:
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def update_role(self, id_rol: int, role: Rol):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE roles SET nombre_rol=%s, descripcion=%s WHERE id_rol=%s",
                (role.nombre_rol, role.descripcion, id_rol),
            )
            if cursor.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="Rol no encontrado")
            conn.commit()
            return {"resultado": "Rol actualizado"}
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def delete_role(self, id_rol: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM roles WHERE id_rol=%s", (id_rol,))
            if cursor.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="Rol no encontrado")
            conn.commit()
            return {"resultado": "Rol eliminado"}
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()
