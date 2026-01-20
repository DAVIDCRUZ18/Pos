import os
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas

def generar_pdf(texto, ruta_pdf, titulo="Comprobante"):
    os.makedirs(os.path.dirname(ruta_pdf), exist_ok=True)

    c = canvas.Canvas(ruta_pdf, pagesize=LETTER)
    width, height = LETTER

    x = 40
    y = height - 40

    c.setFont("Courier", 9)

    for linea in texto.split("\n"):
        if y < 40:
            c.showPage()
            c.setFont("Courier", 9)
            y = height - 40
        c.drawString(x, y, linea)
        y -= 12

    c.save()
