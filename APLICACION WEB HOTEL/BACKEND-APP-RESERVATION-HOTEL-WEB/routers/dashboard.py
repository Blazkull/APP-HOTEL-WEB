from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, extract
from datetime import datetime
from decimal import Decimal
from fastapi.responses import FileResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfgen import canvas
import os

from core.database import SessionDep
from models.reservation import Reservation
from models.client import Client
from models.room import Room

router = APIRouter()

@router.get("/api/dashboard")
def get_dashboard_data(
    session: SessionDep,
    month: int = Query(default=datetime.now().month, ge=1, le=12),
    year: int = Query(default=datetime.now().year)
):
    total_recaudo = session.query(func.sum(Reservation.total))\
        .filter(extract('month', Reservation.check_in_date) == month)\
        .filter(extract('year', Reservation.check_in_date) == year)\
        .scalar() or Decimal(0.00)

    total_habitaciones = session.query(func.count(Room.id)).scalar() or 1

    habitaciones_reservadas = session.query(func.count(Reservation.id))\
        .filter(extract('month', Reservation.check_in_date) == month)\
        .filter(extract('year', Reservation.check_in_date) == year)\
        .scalar() or 0

    porcentaje_ocupacion = (habitaciones_reservadas / total_habitaciones) * 100

    promedio_dias = session.query(
        func.avg(func.datediff(Reservation.check_out_date, Reservation.check_in_date))
    )\
        .filter(extract('month', Reservation.check_in_date) == month)\
        .filter(extract('year', Reservation.check_in_date) == year)\
        .scalar() or 0

    total_clientes = session.query(func.count(func.distinct(Reservation.client_id)))\
        .filter(extract('month', Reservation.check_in_date) == month)\
        .filter(extract('year', Reservation.check_in_date) == year)\
        .scalar() or 0

    return {
        "total_recaudo": float(total_recaudo),
        "porcentaje_ocupacion": round(porcentaje_ocupacion, 2),
        "promedio_dias": round(promedio_dias, 2),
        "total_clientes": total_clientes
    }

@router.get("/api/dashboard/pdf")
def generate_dashboard_pdf(
    session: SessionDep,
    month: int = Query(default=datetime.now().month, ge=1, le=12),
    year: int = Query(default=datetime.now().year)
):
    dashboard = get_dashboard_data(session, month, year)

    # definir las rutas PDF
    filename = f"dashboard_report_{month:02d}_{year}.pdf"
    filepath = os.path.join("static", filename)
    os.makedirs("static", exist_ok=True)

    # crear PDF
    c = canvas.Canvas(filepath, pagesize=letter)
    width, height = letter
    margin = 50

    # paleta de colores
    PRIMARY_COLOR = colors.Color(0.2, 0.4, 0.6, 1)  
    ACCENT_COLOR = colors.Color(0.8, 0.3, 0.1, 1)  
    TEXT_COLOR = colors.Color(0.1, 0.1, 0.1, 1)     
    LIGHT_GREY = colors.Color(0.95, 0.95, 0.95, 1)  
    BORDER_COLOR = colors.Color(0.7, 0.7, 0.7, 1)   

    # logo
    logo_path = "static/logo.png"
    logo_height = 0
    if os.path.exists(logo_path):
        logo_width = 1.2 * inch
        logo_height = 1.2 * inch
        c.drawImage(logo_path, margin, height - logo_height - 20, width=logo_width, height=logo_height, mask='auto')

    # marca de agua 
    if os.path.exists(logo_path):
        watermark_width = width * 0.6 
        watermark_height = height * 0.6 
        watermark_x = (width - watermark_width) / 2
        watermark_y = (height - watermark_height) / 2

        c.saveState() 
        c.setFillAlpha(0.08) 
        c.drawImage(logo_path, watermark_x, watermark_y,
                    width=watermark_width, height=watermark_height,
                    mask='auto')
        c.restoreState() 

    # seccion del titulo
    title_x = margin + (1.4 * inch if os.path.exists(logo_path) else 0)
    title_y = height - 60
    c.setFont("Helvetica-Bold", 24) 
    c.setFillColor(PRIMARY_COLOR)
    c.drawString(title_x, title_y, f"📊 Informe del Hotel - {month:02d}/{year}")

    #linea decorativa
    line_y = title_y - 65
    c.setStrokeColor(ACCENT_COLOR) 
    c.setLineWidth(2)
    c.line(margin, line_y, width - margin, line_y)

    # seccion de las cards
    y_start_cards = line_y - 70 

    card_width = (width - 2 * margin - 20) / 2
    card_height = 100 
    spacing_x = 20
    spacing_y = 25


    labels = {
        "total_recaudo": "💰 Total Recaudado",
        "porcentaje_ocupacion": "🏨 Porcentaje de Ocupación",
        "promedio_dias": "📅 Promedio de Días Reservados",
        "total_clientes": "👥 Total de Clientes"
    }

    values = {
        "total_recaudo": f"${dashboard['total_recaudo']:,.2f}",
        "porcentaje_ocupacion": f"{dashboard['porcentaje_ocupacion']:.2f}%",
        "promedio_dias": f"{dashboard['promedio_dias']:.0f} días",
        "total_clientes": str(dashboard['total_clientes'])
    }

    x_positions = [margin, margin + card_width + spacing_x]
    y_positions = [y_start_cards - card_height, y_start_cards - 2 * card_height - spacing_y]

    index = 0
    for i in range(2):
        for j in range(2):
            if index >= len(labels):
                break
            key = list(labels.keys())[index]
            label = labels[key]
            value = values[key]

            x = x_positions[j]
            y_card = y_positions[i]

            
            c.setFillColor(LIGHT_GREY)
            c.roundRect(x, y_card, card_width, card_height, 10, fill=1, stroke=0)

            
            c.setStrokeColor(BORDER_COLOR)
            c.setLineWidth(1)
            c.roundRect(x, y_card, card_width, card_height, 10, fill=0, stroke=1)

            
            c.setFont("Helvetica-Bold", 14) 
            c.setFillColor(PRIMARY_COLOR) 
            c.drawString(x + 20, y_card + card_height - 30, label) 

            c.setFont("Helvetica", 16) 
            c.setFillColor(TEXT_COLOR)
            c.drawString(x + 20, y_card + 25, value) 

            index += 1

            #footer 
    c.setStrokeColor(BORDER_COLOR)
    c.setLineWidth(1)
    c.line(margin, 50, width - margin, 50)

    # footer text
    c.setFont("Helvetica-Oblique", 10)
    c.setFillColor(colors.grey)
    generated_text = f"Generado automáticamente - {datetime.now().strftime('%d/%m/%Y %H:%M')} por: Usuario del Sistema" # Added dummy user
    c.drawCentredString(width / 2, 35, generated_text)

    c.save() # guardar el  PDF
    return FileResponse(filepath, media_type="application/pdf", filename=filename)
