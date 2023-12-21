from flask import Flask, render_template, request, send_file
import pandas as pd
from io import BytesIO
from fpdf import FPDF
import tempfile

app = Flask(__name__)

uploaded_file = None  # Variable global para almacenar los datos del archivo cargado

@app.route('/')
def index():
    return render_template('index.html', title='Carga de Calificaciones')

@app.route('/upload', methods=['POST'])
def upload():
    global uploaded_file
    if 'file' not in request.files:
        return render_template('index.html', title='Carga de Calificaciones', error='No se ha seleccionado ningún archivo.')

    file = request.files['file']
    if file.filename == '':
        return render_template('index.html', title='Carga de Calificaciones', error='No se ha seleccionado ningún archivo.')

    if file:
        uploaded_file = pd.read_excel(file)
        return render_template('index.html', title='Carga de Calificaciones', data=uploaded_file.to_html(), filename=file.filename)

@app.route('/download', methods=['POST'])
def download():
    global uploaded_file
    if uploaded_file is None:
        return render_template('index.html', title='Carga de Calificaciones', error='No hay archivo cargado para generar el PDF.')

    # Crear PDF con Reporte de Calificaciones
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', '', 14)  # Aumentar tamaño de letra
    pdf.cell(200, 10, txt='Reporte de Calificaciones', ln=True, align='C')
    pdf.set_font('Arial', '', 12)
    
    # Encabezados de las columnas
    col_widths = [50, 40, 40]  # Anchuras de las columnas
    pdf.set_fill_color(200)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(col_widths[0], 10, txt='Nombre', border=1, ln=False, align='C')  # Centrar el título de Nombre
    pdf.cell(col_widths[1], 10, txt='AA', border=1, ln=False, align='C')
    pdf.cell(col_widths[2], 10, txt='EF', border=1, ln=True, align='C')
    
    # Datos del archivo
    pdf.set_font('Arial', '', 12)
    data_columns = uploaded_file.columns.tolist()
    for index, row in uploaded_file.iterrows():
        pdf.cell(col_widths[0], 10, str(row[data_columns[0]]), border=1, ln=False)
        pdf.cell(col_widths[1], 10, str(row[data_columns[1]]), border=1, ln=False, align='C')
        pdf.cell(col_widths[2], 10, str(row[data_columns[2]]), border=1, ln=True, align='C')

    # Línea para firma
    pdf.ln(10)
    pdf.cell(0, 10, txt='Firma:', ln=True)

    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        pdf_output = tmp_file.name
        pdf.output(pdf_output)

    return send_file(pdf_output, as_attachment=True, download_name='reporte_calificaciones.pdf')

if __name__ == '__main__':
    app.run(debug=True)
