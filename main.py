from flask import Flask, render_template, request, redirect, url_for, flash
import os
import json

app = Flask(__name__)
app.secret_key = 'secreto123'  # Necessário para usar flash (pode ser qualquer coisa)

# Configuração do caminho para salvar os PDFs
UPLOAD_FOLDER = 'pdfs'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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
            pdf_filename = pdf.filename
            pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_filename)

            pdf.save(pdf_path)

            novo_registro = {
                'curso': curso,
                'disciplina': disciplina,
                'semestre': semestre,
                'professor': professor,
                'unidade': unidade,
                'arquivo': pdf_path.replace("\\", "/")
            }

            try:
                with open('dados.json', 'r', encoding='utf-8') as f:
                    dados = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                dados = []

            dados.append(novo_registro)

            with open('dados.json', 'w', encoding='utf-8') as f:
                json.dump(dados, f, ensure_ascii=False, indent=4)

            flash('Prova cadastrada com sucesso!')
            return redirect(url_for('cadastrar_prova'))
        else:
            flash('Erro: Envie um arquivo PDF válido.')
            return redirect(url_for('cadastrar_prova'))

    return render_template('cadastrar_prova.html')

if __name__ == '__main__':
    app.run(debug=True)
