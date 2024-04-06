import os
import requests
from flask import Flask, render_template, request, redirect, url_for
from raspador import raspador_infomoney

app = Flask(__name__) # Cria uma instância do Flask. 


@app.route("/")
def apresentacao():
  return render_template('apresentacao.html')

@app.route("/contato")
def contato():
  return render_template('contato.html') 

@app.route("/materias")
def materias():
  return render_template('materias.html') 

@app.route("/raspador-infomoney")
def infomoney():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
         <title> Raspador Infomoney </title>
    </head> 
    <body>
        <h1> Veja todas as matérias do Infomoney que tem a palavra Petróleo no texto ou no titulo</h1>
        <p>
        As matérias encontradas foram:
        <ul>
      """
    for conteudo in raspador_infomoney():
        if "com" in conteudo:
            html += f'<li> <a href = "{conteudo["link"]}">{conteudo["titulo"]}'
    html += """
        </ul>
        </p>
    </body>
    </html>
    """
    return html
