from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.platypus.frames import Frame
from reportlab.platypus.flowables import Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
import random
from itertools import batched
from read_from_excel import read_excel

filename = "lista_canciones.xlsx"

cells_type_qrs = 'qrs'
cells_type_data = 'data'

# Colores disponibles para las tarjetas
card_colors = ['#cf795b', '#e9d87e', '#5fc74b', '#4bc7c6', '#7e86e9', '#dd7ee9', '#e35555']

# Configurar tamaño de la página y márgenes
page_width, page_height = A4
margin = 0 * cm  # Márgenes iguales en ambas páginas

# Configuración de las dimensiones de las celdas
cell_width, cell_height = 7 * cm, 7 * cm  # Tamaño de cada celda
image_width, image_height = 4 * cm, 4 * cm  # Tamaño de las imágenes dentro de las celdas
num_rows, num_cols = 4, 3  # 4 filas y 3 columnas

# Configurar estilos de texto
artist_style = ParagraphStyle(
    name='Normal',
    fontName='Helvetica-Bold',
    fontSize=15,
    leading=20,
    alignment=1,
    textColor="#000000",
)

year_style = ParagraphStyle(
    name='Normal',
    fontName='Helvetica-Bold',
    fontSize=40,
    alignment=1,
    textColor="#000000",
)

title_style = ParagraphStyle(
    name='Normal',
    fontName='Helvetica-Oblique',
    fontSize=15,
    leading=20,
    alignment=1,
    textColor="#000000",
)

def hex_to_rgb(hex_color):
    """Convierte un código hexadecimal (#RRGGBB) en valores RGB normalizados (0-1)."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4))

def build_list_data_order(songs):
    data_list = []

    for songs_row in batched(songs, num_cols):
        data_list.extend(songs_row[::-1])

    return data_list

def create_cells_structure(c, cells_type, songs):
    x_start = margin
    y_start = page_height - margin

    for row in range(num_rows):
        for col in range(num_cols):
            cell_index = row * num_cols + col

            # Coordenadas de la celda actual
            x = x_start + col * cell_width
            y = y_start - (row + 1) * cell_height

            # Dibujar fondo de la celda
            if (cells_type == cells_type_qrs): c.setFillColorRGB(0, 0, 0)
            else: c.setFillColorRGB(*hex_to_rgb(card_colors[random.randint(0, len(card_colors) - 1)]))

            # Dibujar el rectángulo con las dimensiones de la celda, con el color de fondo y sin bordes
            c.rect(x, y, cell_width, cell_height, fill=1, stroke=0)

            # Dibujar el contenido de las celdas
            if (cells_type == cells_type_qrs):
                # Dibujar la imagen centrada dentro de la celda
                img_x = x + (cell_width - image_width) / 2
                img_y = y + (cell_height - image_height) / 2
                c.drawImage(songs[cell_index].qr_filename, img_x, img_y, width=image_width, height=image_height, preserveAspectRatio=True)
            else:
                # Crear párrafos para cada línea
                artist_paragraph = Paragraph(str(songs[cell_index].artist), artist_style)
                year_paragraph = Paragraph(str(songs[cell_index].year), year_style)
                title_paragraph = Paragraph(str(songs[cell_index].title), title_style)

                # Dibujar párrafos en posiciones específicas
                # 1. Artista (parte superior)
                artist_paragraph.wrapOn(c, cell_width - 15, cell_height / 3)
                artist_paragraph.drawOn(c, x + 5, y + cell_height - artist_paragraph.height - 10)

                # 2. Año (línea central)
                year_paragraph.wrapOn(c, cell_width - 10, cell_height / 3)
                year_paragraph.drawOn(c, x + 5, y + (cell_height / 2) + 20)

                # 3. Título canción (parte inferior)
                title_paragraph.wrapOn(c, cell_width - 15, cell_height / 3)
                title_paragraph.drawOn(c, x + 5, y + 10)


def create_pdf(output_filename, songs):
    # Crear el canvas del PDF
    c = canvas.Canvas(output_filename, pagesize=A4)
    page_number = 1

    for songs_page in batched(songs, num_rows*num_cols):
        if page_number > 1: c.showPage()

        # --- Carilla 1: Tabla de qrs ---
        create_cells_structure(c, cells_type_qrs, songs_page)
        # Crear una nueva página
        c.showPage()
        # --- Carilla 2: Tabla de datos con colores de fondo ---
        create_cells_structure(c, cells_type_data, build_list_data_order(songs_page))

        page_number +=1

    c.save()

songs_parsed = read_excel(filename)
create_pdf("metalHitster.pdf", songs_parsed)
