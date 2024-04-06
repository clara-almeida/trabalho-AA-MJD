import requests
from bs4 import BeautifulSoup

#captura página "Ultimas Noticias Infomoney"
result = requests.get("https://www.infomoney.com.br/ultimas-noticias/")

#variável result vai receber o codigo da execução da página chamada pela request
soup = BeautifulSoup(result.text)

titles = soup.find_all("span", class_="hl-title hl-title-2")

# Itera sobre as tags encontradas para extrair os títulos e os links
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
    article = link_soup.find("article", class_= "im-article clear-fix")
    if article:
        main_paragraphs = soup.find_all("p")
        main_text = "\n".join(paragraph.get_text().strip() for paragraph in main_paragraphs)

        print(title_text)
        print(link)
        print(main_text)
        print()