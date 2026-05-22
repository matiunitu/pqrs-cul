from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from config.db_config import get_db_connection
from models.pqrs_model import Pqrs

class PqrsController:
    def _safe_dependencia(self, cur, id_dep):
        """Returns id_dep only if it exists in dependencias, else None."""
        if not id_dep:
            return None
        cur.execute("SELECT 1 FROM dependencias WHERE id_dependencia = %s", (id_dep,))
        return id_dep if cur.fetchone() else None

    def create_pqrs(self, pqrs: Pqrs):
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            id_dep = self._safe_dependencia(cur, pqrs.id_dependencia)
            cur.execute(
                """INSERT INTO pqrs (radicado, descripcion, fecha_creacion, fecha_limite,
                   id_usuario, id_dependencia, id_tipospqrs, id_estado, id_prioridad)
                   VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id_pqrs""",
                (
                    pqrs.radicado,
                    pqrs.descripcion,
                    pqrs.fecha_creacion,
                    pqrs.fecha_limite,
                    pqrs.id_usuario,
                    id_dep,
                    pqrs.id_tipospqrs,
                    pqrs.id_estado,
                    pqrs.id_prioridad,
                ),
            )
            id_pqrs = cur.fetchone()['id_pqrs']
            conn.commit()
            return {"id_pqrs": id_pqrs, "resultado": "PQRS creado"}
        except Exception as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def get_pqrs_all(self):
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT * FROM pqrs")
            rows = cur.fetchall()
            return rows
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def get_pqrs(self, id_pqrs: int):
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT * FROM pqrs WHERE id_pqrs=%s", (id_pqrs,))
            r = cur.fetchone()
            if not r:
                raise HTTPException(status_code=404, detail="PQRS no encontrado")
            return r
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def update_pqrs(self, id_pqrs: int, pqrs: Pqrs):
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(
                """UPDATE pqrs SET radicado=%s, descripcion=%s, fecha_creacion=%s, fecha_limite=%s,
                   id_usuario=%s, id_dependencia=%s, id_tipospqrs=%s, id_estado=%s, id_prioridad=%s
                   WHERE id_pqrs=%s""",
                (
                    pqrs.radicado,
                    pqrs.descripcion,
                    pqrs.fecha_creacion,
                    pqrs.fecha_limite,
                    pqrs.id_usuario,
                    pqrs.id_dependencia,
                    pqrs.id_tipospqrs,
                    pqrs.id_estado,
                    pqrs.id_prioridad,
                    id_pqrs
                )
            )
            if cur.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="PQRS no encontrado")
            conn.commit()
            return {"resultado": "PQRS actualizado"}
        except Exception as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def delete_pqrs(self, id_pqrs: int):
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            # Borrar dependencias primero para evitar violación de llave foránea
            cur.execute("DELETE FROM historial_estados WHERE id_pqrs=%s", (id_pqrs,))
            cur.execute("DELETE FROM respuestas WHERE id_pqrs=%s", (id_pqrs,))
            # Ahora borrar la PQRS
            cur.execute("DELETE FROM pqrs WHERE id_pqrs=%s", (id_pqrs,))
            if cur.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="PQRS no encontrado")
            conn.commit()
            return {"resultado": "PQRS eliminado"}
        except Exception as err:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()

    def generate_pdf(self, id_pqrs: int):
        try:
            from xhtml2pdf import pisa
            from io import BytesIO
        except ImportError:
            raise HTTPException(status_code=500, detail="La librería xhtml2pdf no está instalada.")

        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("""
                SELECT p.*, u.nombre as usuario_nombre
                FROM pqrs p
                LEFT JOIN usuarios u ON p.id_usuario = u.id_usuario
                WHERE p.id_pqrs=%s
            """, (id_pqrs,))
            p_data = cur.fetchone()
            if not p_data:
                raise HTTPException(status_code=404, detail="PQRS no encontrado")
            
            cur.execute("SELECT * FROM respuestas WHERE id_pqrs=%s ORDER BY fecha_respuesta DESC LIMIT 1", (id_pqrs,))
            resp = cur.fetchone()
            respuesta_texto = resp['mensaje'] if resp else "Sin respuesta oficial aún."

            TIPO = {1: 'Queja', 2: 'Petición', 3: 'Reclamo', 4: 'Sugerencia'}
            ESTADO = {1: 'Activo', 2: 'Inactivo'} # Ajusta según tu tabla de estados si es necesario
            
            html_template = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Constancia de PQRS</title>
    <style>
        @page {
            size: A4;
            margin: 2.5cm;
        }
        body {
            font-family: Arial, sans-serif;
            color: #000000;
            line-height: 1.5;
            font-size: 11pt;
        }
        .header {
            text-align: center;
            border-bottom: 2px solid #1a365d;
            padding-bottom: 10px;
            margin-bottom: 30px;
        }
        .institution-name {
            font-size: 16pt;
            font-weight: bold;
            color: #1a365d;
            text-transform: uppercase;
        }
        .title {
            text-align: center;
            font-weight: bold;
            font-size: 14pt;
            margin-bottom: 20px;
        }
        .intro {
            text-align: justify;
            margin-bottom: 30px;
        }
        .info-section {
            margin-bottom: 30px;
        }
        .info-row {
            margin-bottom: 8px;
        }
        .info-label {
            font-weight: bold;
            display: inline-block;
            width: 150px;
        }
        .section-title {
            font-weight: bold;
            margin-top: 20px;
            margin-bottom: 10px;
            color: #1a365d;
        }
        .description-box {
            text-align: justify;
            margin-bottom: 30px;
        }
        .response-box {
            text-align: justify;
            border: 1px solid #d1d5db;
            background-color: #f9fafb;
            padding: 15px;
            margin-bottom: 40px;
        }
        .footer {
            text-align: center;
            font-size: 8pt;
            color: #4b5563;
            margin-top: 40px;
            margin-bottom: 20px;
        }
        .signature-section {
            margin-top: 60px;
        }
        .signature-line {
            width: 250px;
            border-bottom: 1px solid #000;
            margin-bottom: 5px;
        }
        .signature-text {
            font-size: 10pt;
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="institution-name">{institucion}</div>
    </div>
    <div class="title">
        CONSTANCIA DE PQRS
    </div>
    <div class="intro">
        El presente documento certifica el registro y estado actual de la Petición, Queja, Reclamo o Sugerencia (PQRS) presentada ante nuestra institución. A continuación, se detallan los datos correspondientes al caso.
    </div>
    <div class="info-section">
        <div class="info-row"><span class="info-label">Radicado:</span> {radicado}</div>
        <div class="info-row"><span class="info-label">Fecha:</span> {fecha}</div>
        <div class="info-row"><span class="info-label">Usuario:</span> {usuario}</div>
        <div class="info-row"><span class="info-label">Tipo de Solicitud:</span> {tipo}</div>
        <div class="info-row"><span class="info-label">Estado:</span> {estado}</div>
    </div>
    <div class="section-title">Descripción de la Solicitud</div>
    <div class="description-box">
        {descripcion}
    </div>
    <div class="section-title">Respuesta Oficial</div>
    <div class="response-box">
        {respuesta}
    </div>
    <div class="signature-section">
        <div class="signature-line"></div>
        <div class="signature-text">Firma autorizada</div>
    </div>
    <div class="footer">
        Documento generado automáticamente por el sistema PQRS
    </div>
</body>
</html>"""

            data = {
                "institucion": "Institución Educativa",
                "radicado": p_data['radicado'] or f"PQRS-{id_pqrs}",
                "fecha": p_data['fecha_creacion'].strftime("%d/%m/%Y") if p_data['fecha_creacion'] else "N/A",
                "usuario": p_data['usuario_nombre'] or f"ID {p_data['id_usuario']}",
                "tipo": TIPO.get(p_data['id_tipospqrs'], f"Tipo {p_data['id_tipospqrs']}"),
                "estado": ESTADO.get(p_data['id_estado'], f"ID {p_data['id_estado']}"),
                "descripcion": p_data['descripcion'] or "Sin descripción",
                "respuesta": respuesta_texto
            }
            html_content = html_template.format(**data)
            
            result = BytesIO()
            pisa_status = pisa.CreatePDF(BytesIO(html_content.encode("utf-8")), dest=result)
            
            if pisa_status.err:
                raise HTTPException(status_code=500, detail="Error al generar el PDF")
                
            return result.getvalue()
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            conn.close()