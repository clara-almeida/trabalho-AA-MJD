import os
import requests
from flask import Flask, render_template, request, redirect, url_for
import raspador

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

@app.route("/raspador-discursos")
def discursos():
    discursos = raspador.get_discursos()
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
         <title> Discursos do presidente </title>
    </head> 
    <body>
        <h1> Veja as principais frases de cada discurso presidencial.</h1>
        <p>
        As aspas encontradas foram: <br />
        {
          "<br />".join([f"Titulo: {discurso["title"]}<br /><a href=\"{discurso["link"]}\">{discurso["content"]}</a>" for discurso in discursos])     
        }
        </p>
    </body>
    </html>
    """
    return html
