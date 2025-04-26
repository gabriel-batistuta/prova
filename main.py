# app.py
from flask import Flask, render_template, send_from_directory, url_for
import os
import json

app = Flask(__name__, template_folder='templates', static_folder='static')
DATA_FILE = os.path.join(os.getcwd(), 'dados.json')
PDF_FOLDER = os.path.join(app.static_folder, 'pdfs')

# Helper to load provas list from JSON
def load_provas():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data.get('provas', [])

@app.route('/provas/')
def show_provas():
    provas = load_provas()
    # ajusta cada link para a rota de download
    for p in provas:
        if 'link' in p:
            p['url'] = url_for('download_pdf', filename=p['link'])
    return render_template('provas.html', provas=provas)

@app.route('/provas/pdf/<path:filename>')
def download_pdf(filename):
    # envia o arquivo PDF da pasta static/pdfs
    return send_from_directory(PDF_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)