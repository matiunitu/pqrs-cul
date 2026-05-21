import psycopg2
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from config.db_config import get_db_connection
from models.usuario_model import Usuario, UsuarioUpdate
import bcrypt


class UsuariosController:
    def create_usuario(self, usuario: Usuario):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            pw = usuario.password_hash
            if pw and not pw.startswith('$2'):
                # hash raw password if provided
                pw = bcrypt.hashpw(pw.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            elif not pw:
                pw = bcrypt.hashpw('1234'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            # Asegurar valor por defecto para tipo_documento si viene vacío
            tipo_doc = usuario.tipo_documento if getattr(usuario, 'tipo_documento', None) else 'CC'

            cursor.execute(
                """INSERT INTO usuarios
                (nombre, tipo_documento, documento, correo, telefono, id_rol, id_programa,
                 activo, estado, password_hash)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id_usuario""",
                (
                    usuario.nombre,
                    tipo_doc,
                    usuario.documento,
                    usuario.correo,
                    usuario.telefono,
                    usuario.id_rol,
                    usuario.id_programa,
                    usuario.activo,
                    usuario.estado,
                    pw,
                ),
            )
            row = cursor.fetchone()
            # cursor may return a mapping (RealDictRow) or a tuple
            if isinstance(row, dict) or hasattr(row, 'get'):
                id_usuario = row.get('id_usuario')
            else:
                id_usuario = row[0]
            conn.commit()
            return {"id_usuario": id_usuario, "resultado": "Usuario creado"}
        except psycopg2.IntegrityError as err:
            conn.rollback()
            raise HTTPException(status_code=400, detail=f"Integrity error: {str(err)}")
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def get_usuario(self, id_usuario: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """SELECT id_usuario, nombre, documento, correo, telefono,
                id_rol, id_programa, activo, estado, created_at
                FROM usuarios
                WHERE id_usuario = %s""",
                (id_usuario,),
            )
            result = cursor.fetchone()
            if not result:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")
            payload = {
                "id_usuario": result['id_usuario'],
                "nombre": result['nombre'],
                "documento": result['documento'],
                "correo": result['correo'],
                "telefono": result['telefono'],
                "id_rol": result['id_rol'],
                "id_programa": result['id_programa'],
                "activo": result['activo'] if result['activo'] is not None else True,
                "estado": result['estado'] if result['estado'] is not None else 1,
                "created_at": result['created_at'],
            }
            return jsonable_encoder(payload)
        except psycopg2.Error as err:
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def get_usuarios(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """SELECT u.id_usuario, u.nombre, u.tipo_documento, u.documento, u.correo,
                   u.telefono, u.id_rol, r.nombre_rol, u.id_programa,
                   u.activo, u.estado, u.created_at
                   FROM usuarios u
                   LEFT JOIN roles r ON u.id_rol = r.id_rol
                   ORDER BY u.id_usuario"""
            )
            results = cursor.fetchall()
            payload = []
            for r in results:
                payload.append(
                    {
                        "id_usuario":     r['id_usuario'],
                        "nombre":         r['nombre'],
                        "tipo_documento": r['tipo_documento'],
                        "documento":      r['documento'],
                        "correo":         r['correo'],
                        "telefono":       r['telefono'],
                        "id_rol":         r['id_rol'],
                        "nombre_rol":     r['nombre_rol'],
                        "id_programa":    r['id_programa'],
                        "activo":         bool(r['activo']) if r['activo'] is not None else True,
                        "estado":         int(r['estado']) if r['estado'] is not None else 1,
                        "created_at":     r['created_at'],
                    }
                )
            return jsonable_encoder(payload)
        except psycopg2.Error as err:
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def get_usuarios_by_rol(self, nombre_rol: str):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """SELECT u.id_usuario, u.nombre, r.nombre_rol
                   FROM usuarios u
                   JOIN roles r ON u.id_rol = r.id_rol
                   WHERE LOWER(r.nombre_rol) = LOWER(%s)
                   AND u.estado = 1
                   ORDER BY u.nombre""",
                (nombre_rol,)
            )
            results = cursor.fetchall()
            return jsonable_encoder([
                {"id_usuario": r[0], "nombre": r[1], "nombre_rol": r[2]}
                for r in results
            ])
        except psycopg2.Error as err:
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def update_usuario(self, id_usuario: int, usuario: UsuarioUpdate):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Construir consulta dinámica para actualización parcial
            data = usuario.dict(exclude_unset=True)
            if not data:
                return {"resultado": "No hay campos para actualizar"}
            
            campos = []
            valores = []
            for k, v in data.items():
                if k == "password_hash":
                    # Si se incluye password_hash, lo hasheamos
                    if v and not v.startswith('$2'):
                        v = bcrypt.hashpw(v.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                campos.append(f"{k}=%s")
                valores.append(v)
            
            valores.append(id_usuario)
            query = f"UPDATE usuarios SET {', '.join(campos)} WHERE id_usuario=%s"
            
            cursor.execute(query, tuple(valores))
            if cursor.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="Usuario no encontrado")
            conn.commit()
            return {"resultado": "Usuario actualizado"}
        except psycopg2.IntegrityError as err:
            conn.rollback()
            raise HTTPException(status_code=400, detail=f"Integrity error: {str(err)}")
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def change_password(self, id_usuario: int, password: str):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            cursor.execute(
                "UPDATE usuarios SET password_hash=%s WHERE id_usuario=%s",
                (hashed_pw, id_usuario)
            )
            if cursor.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="Usuario no encontrado")
            conn.commit()
            return {"resultado": "Contraseña actualizada"}
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def delete_usuario(self, id_usuario: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            # Verificar si existen PQRS referenciando este usuario
            cursor.execute("SELECT COUNT(*) as cnt FROM pqrs WHERE id_usuario = %s", (id_usuario,))
            cnt = cursor.fetchone()
            cnt_val = cnt['cnt'] if isinstance(cnt, dict) or hasattr(cnt, '__getitem__') else (cnt[0] if cnt else 0)
            if cnt_val and int(cnt_val) > 0:
                # No permitir borrado si hay PQRS relacionadas
                raise HTTPException(status_code=400, detail=f"No se puede eliminar: existen {int(cnt_val)} PQRS referenciando este usuario. Elimine o reasigne las PQRS primero.")

            cursor.execute("DELETE FROM usuarios WHERE id_usuario=%s", (id_usuario,))
            if cursor.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="Usuario no encontrado")
            conn.commit()
            return {"resultado": "Usuario eliminado"}
        except psycopg2.IntegrityError as err:
            conn.rollback()
            raise HTTPException(status_code=400, detail=f"Integrity error: {str(err)}")
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def reasignar_pqrs(self, from_id: int, to_id: int, delete_source: bool = False):
        """Reasigna todas las PQRS de from_id a to_id. Si delete_source=True intenta borrar el usuario origen al final."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Verificar existencia de usuarios
            cursor.execute("SELECT id_usuario FROM usuarios WHERE id_usuario = %s", (from_id,))
            if cursor.fetchone() is None:
                raise HTTPException(status_code=404, detail=f"Usuario origen {from_id} no encontrado")
            cursor.execute("SELECT id_usuario FROM usuarios WHERE id_usuario = %s", (to_id,))
            if cursor.fetchone() is None:
                raise HTTPException(status_code=404, detail=f"Usuario destino {to_id} no encontrado")

            # Reasignar PQRS
            cursor.execute("UPDATE pqrs SET id_usuario = %s WHERE id_usuario = %s", (to_id, from_id))
            reassigned = cursor.rowcount

            # También reasignar respuestas y historial_estados que referencian usuarios si existe
            cursor.execute("UPDATE respuestas SET id_usuario = %s WHERE id_usuario = %s", (to_id, from_id))
            reassigned += cursor.rowcount
            cursor.execute("UPDATE historial_estados SET cambiado_por = %s WHERE cambiado_por = %s", (to_id, from_id))
            reassigned += cursor.rowcount

            if delete_source:
                # Intentar borrar el usuario origen (ya no debería tener FK en pqrs/respuestas/historial)
                cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s", (from_id,))
                deleted = cursor.rowcount
            else:
                deleted = 0

            conn.commit()
            return {"reassigned_count": reassigned, "deleted_source": bool(deleted)}
        except psycopg2.Error as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()
