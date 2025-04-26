# main.py
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
import os
import json

app = Flask(__name__)
app.secret_key = 'secreto123'

UPLOAD_FOLDER = 'pdfs'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

DATA_FILE = 'dados.json'

# Rota para cadastrar prova
@app.route('/cadastrar_prova/', methods=['GET', 'POST'])
def cadastrar_prova():
    if request.method == 'POST':
        curso = request.form.get('curso')
        disciplina = request.form.get('disciplina')
        semestre = request.form.get('semestre')
        professor = request.form.get('professor')
        unidade = request.form.get('unidade')
        pdf = request.files.get('pdf_prova')

        if pdf and pdf.filename.endswith('.pdf'):
            # Limpar espaços no nome do arquivo
            pdf_filename = pdf.filename.replace(" ", "_")
            pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_filename)
            pdf.save(pdf_path)

            novo_registro = {
                'curso': curso,
                'disciplina': disciplina,
                'semestre': semestre,
                'professor': professor,
                'unidade': unidade,
                'arquivo': f"pdfs/{pdf_filename}"
            }

            try:
                with open(DATA_FILE, 'r', encoding='utf-8') as f:
                    dados = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                dados = []

            dados.append(novo_registro)

            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(dados, f, ensure_ascii=False, indent=4)

            flash('Prova cadastrada com sucesso!')
            return redirect(url_for('cadastrar_prova'))
        else:
            flash('Erro: Envie um arquivo PDF válido.')
            return redirect(url_for('cadastrar_prova'))

    return render_template('cadastrar_prova.html')

# Rota para listar provas
@app.route('/provas/')
def show_provas():
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            provas = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        provas = []

    # Ajustar a URL de download para cada prova
    for p in provas:
        if 'arquivo' in p:
            # pega só o nome do arquivo, sem o "pdfs/"
            filename = os.path.basename(p['arquivo'])
            p['url'] = url_for('download_pdf', filename=filename)

    return render_template('provas.html', provas=provas)

# Rota para baixar PDFs
@app.route('/pdfs/<path:filename>')
def download_pdf(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)