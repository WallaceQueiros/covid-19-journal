from flask import Flask, render_template, json
from os import path
from datetime import datetime

app = Flask(__name__)

def read_json(filename):
    file = path.join(app.static_folder, filename)
    with open(file) as json_file:
        data = json.load(json_file)    
    return data

@app.route('/')
def homepage():
    noticias = read_json('noticias.json')
    estados = read_json('estados.json')
    
    # 5 noticias mais curtidas do json
    mais_curtidas = sorted(noticias, key=lambda i: i['curtidas'], reverse=True)[:6]

    # 3 noticias mais recentes de cada estado
    for estado in estados:
        estado_noticias = [n for n in noticias if n['estado'] == estado['sigla']]
        estado_noticias = sorted(
            estado_noticias, 
            key=lambda x: datetime.strptime(x['data'], '%d/%m/%Y')
        )
        estado['noticias'] = estado_noticias[-3:]

    # renderiza os templates
    return render_template('homepage.html', mais_curtidas=mais_curtidas, por_estado=estados)


@app.route('/<estado>/<noticia_id>')
def newspage(estado=None, noticia_id=None):
    noticias = read_json('noticias.json')
    noticia_id = int(noticia_id)
    for n in noticias:
        if n['id'] == noticia_id:
            return render_template('newspage.html', noticia=n)
    return '<h1>404 - Pagina nao encontrada</h1>'


if __name__ == '__main__':
    app.run()
