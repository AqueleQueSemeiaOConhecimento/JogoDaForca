from flask import Flask, render_template, request, session, jsonify, redirect, url_for
import random
import json

app = Flask(__name__)
app.secret_key = '0000'

@app.route('/secreto')
def secreto():
    return session['palavra']

with open('dados.json', 'r') as file:
    palavras = json.load(file)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/jogo')
def jogo():
    if 'palavra' not in session:
        session['palavra'] = random.choice(palavras)
        session['adivinhadas'] = ['_'] * len(session['palavra'])
        session['vidas'] = 6  # Número de tentativas permitidas
        session['letras_adivinhadas'] = []
    
    return render_template('jogo.html', 
                           palavra=' '.join(session['adivinhadas']), 
                           vidas=session['vidas'], 
                           letras_adivinhadas=session['letras_adivinhadas'])

@app.route('/adivinhar', methods=['POST'])
def adivinhar():
    dados = request.get_json()
    letra = dados['letra'].lower()
    
    if letra in session['letras_adivinhadas']:
        return jsonify({
            'palavra': ' '.join(session['adivinhadas']),
            'vidas': session['vidas'],
            'letras_adivinhadas': session['letras_adivinhadas'],
            'mensagem': 'Letra já adivinhada.'
        })
    
    session['letras_adivinhadas'].append(letra) 
    
    letra_encontrada = False
    for i, char in enumerate(session['palavra']):
        if char == letra:
            session['adivinhadas'][i] = letra
            letra_encontrada = True
            session['vidas'] -= 1
            session['vidas'] += 1
    
    if not letra_encontrada:
        session['vidas'] -= 1

    if '_' not in session['adivinhadas']:
        return jsonify({
            'palavra': ' '.join(session['adivinhadas']),
            'vidas': session['vidas'],
            'letras_adivinhadas': session['letras_adivinhadas'],
            'mensagem': 'Você venceu!'
        })

    if session['vidas'] == 0:
        return jsonify({
            'palavra': ' '.join(session['palavra']),
            'vidas': session['vidas'],
            'letras_adivinhadas': session['letras_adivinhadas'],
            'mensagem': f'Você perdeu! A palavra era {session["palavra"]}'
        })

    return jsonify({
        'palavra': ' '.join(session['adivinhadas']),
        'vidas': session['vidas'],
        'letras_adivinhadas': session['letras_adivinhadas'],
        'mensagem': ''
    })

@app.route('/resetar')
def resetar():
    session.pop('palavra', None)
    session.pop('adivinhadas', None)
    session.pop('vidas', None)
    session.pop('letras_adivinhadas', None)  # Limpa as letras adivinhadas
    return redirect(url_for('jogo'))

@app.route('/adicionar_palavra', methods=['POST'])
def adicionar_palavra():
    nova_palavra = request.form['palavra'].lower()
    if nova_palavra not in palavras:
        palavras.append(nova_palavra)
        return jsonify({'mensagem': 'Palavra adicionada com sucesso!'})
    else:
        return jsonify({'mensagem': 'A palavra já existe no banco de dados!'})
    

@app.route('/listar', methods=['GET'])
def listar_palavras():
    return jsonify(palavras)

if __name__ == '__main__':
    app.run(debug=True)
