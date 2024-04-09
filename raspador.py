from dotenv import load_dotenv, find_dotenv
import os
load_dotenv(find_dotenv())

import requests
from bs4 import BeautifulSoup
from openai import OpenAI
import gspread
from oauth2client.service_account import ServiceAccountCredentials

arquivo_credenciais = "trabalho-final-aa-574920153065.json"
conteudo_credenciais = os.environ["KEY_GOOGLE"]
with open(arquivo_credenciais, mode="w") as arquivo:
    arquivo.write(conteudo_credenciais)
conta = ServiceAccountCredentials.from_json_keyfile_name(arquivo_credenciais)
api = gspread.authorize(conta)
planilha = api.open_by_key(os.environ["SHEET_ID"])
sheet = planilha.worksheet("Página1")


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

    for i, title in enumerate(titles):
        if i>=3:
           break
        # Extrai o texto do título
        title_text = title.a.text.strip()
        # Extrai o link
        link = title.a["href"]

        link_cells = sheet.findall(link, in_column=2)
        if link_cells:
            link_cell=link_cells[0]
            row_values = sheet.row_values(link_cell.row)
            discursos.append({"title": row_values[0], "link": row_values[1], "content":row_values[2]})
            continue

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

        prompt = "Você é um jornalista e está escrevendo uma matéria sobre este discurso do presidente da república. Analise o conteúdo e selecione, sem realizar nenhuma alteração no texto, o trecho de maior relevância para uma matéria jornalística com um limite de 280 caracteres. Este trecho precisa ter relação com a temática principal do discurso. Responda somente com o trecho, não acrescente nenhuma palavra ou justificativa."
        response = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=[{"role": "user", "content": f"{prompt}: {main_text}"}
        ])
        discursos.append({"title": title_text, "link": link, "content":response.choices[0].message.content})            

        
        linha_armazenar = [title_text, link,response.choices[0].message.content] #armazenar título, link e resumo na planilha
        sheet.insert_row(linha_armazenar, 2)
        
    return discursos