import os
from weasyprint import HTML

# HTML Template
html_template = """
<!DOCTYPE html>
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
</html>
"""

def generate_pqrs_pdf(output_filename="reporte_pqrs.pdf"):
    # Mock data to fill the template
    data = {
        "institucion": "Universidad Nacional de Colombia",
        "radicado": "PQRS-2026-001234",
        "fecha": "22 de Mayo de 2026",
        "usuario": "Juan Pérez",
        "tipo": "Queja",
        "estado": "En Trámite",
        "descripcion": "El usuario presenta una queja formal respecto a los tiempos de respuesta en el proceso de matrícula académica, indicando que el sistema estuvo fuera de servicio durante 48 horas.",
        "respuesta": "Su solicitud ha sido recibida y trasladada a la dependencia correspondiente. Nos pondremos en contacto con usted en un plazo máximo de 15 días hábiles."
    }
    
    # Fill variables
    html_content = html_template.format(**data)
    
    # Generate PDF
    print(f"Generando el PDF '{output_filename}' usando WeasyPrint...")
    HTML(string=html_content).write_pdf(output_filename)
    print("¡PDF generado exitosamente!")

if __name__ == "__main__":
    generate_pqrs_pdf()
