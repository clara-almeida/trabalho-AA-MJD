from dotenv import load_dotenv, find_dotenv
import os
load_dotenv(find_dotenv())

import requests
from bs4 import BeautifulSoup
from openai import OpenAI

def get_discursos():

    chave_api = os.environ.get("OPENAI_API_KEY")
    client = OpenAI(api_key=chave_api)

    #captura página "Últimos discursos e pronunciamentos"
    result = requests.get("https://www.gov.br/planalto/pt-br/acompanhe-o-planalto/discursos-e-pronunciamentos")

    #variável result vai receber o codigo da execução da página chamada pela request
    soup = BeautifulSoup(result.text)

    titles = soup.find_all("h2", class_="tileHeadline")

    # Itera sobre as tags encontradas para extrair os títulos e os links
    discursos = []

    for title in titles:
        # Extrai o texto do título
        title_text = title.a.text.strip()
        # Extrai o link
        link = title.a["href"]

        # Faz uma solicitação HTTP para obter o conteúdo da página do link
        link_response = requests.get(link)
        link_html = link_response.text

        # Cria um objeto BeautifulSoup para a página do link
        link_soup = BeautifulSoup(link_html, "html.parser")

        # Extrai o conteúdo dos parágrafos principais
        main_paragraphs = link_soup.find_all("p", attrs={'class': None})


        # Concatena o texto dos parágrafos principais
        main_text = "\n".join(paragraph.get_text().strip() for paragraph in main_paragraphs)

    #Integração com a OpenAI

        prompt = "Você é um jornalita e está escrevendo uma matéria sobre este discurso do presidente da república. Analise o conteúdo e selecione, sem realizar nenhuma alteração no texto, o trecho de maior relevância para uma matéria jornalística com um limite de 280 caracteres. Este trecho precisa ter relação com a temática principal do discurso. Responda somente com o trecho, não acrescente nenhuma palavra ou justificativa."
        response = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=[{"role": "user", "content": f"{prompt}: {main_text}"}
        ])
        discursos.append({"title": title_text, "link": link, "content":response.choices[0].message.content})
        break
    
    return discursos