import os
import requests
from flask import Flask, render_template, request, redirect, url_for
from raspador import get_discursos

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
    discursos = get_discursos()
    html = render_template("discursos.html", discursos=discursos)
    return html

if __name__ == "__main__":
    app.run(debug=True)
