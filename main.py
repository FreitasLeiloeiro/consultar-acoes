import requests
from bs4 import BeautifulSoup

def buscar_tjsp(nome):

    url = "https://esaj.tjsp.jus.br/cpopg/search.do"

    params = {
        "conversationId": "",
        "dadosConsulta.localPesquisa.cdLocal": "-1",
        "cbPesquisa": "NMPARTE",
        "dadosConsulta.tipoNuProcesso": "UNIFICADO",
        "dadosConsulta.valorConsulta": nome
    }

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, params=params, headers=headers)

    resultados = []

    if response.status_code == 200:

        soup = BeautifulSoup(response.text, "html.parser")

        blocos = soup.find_all("div", class_="fundocinza1")

        for bloco in blocos[:10]:

            link_tag = bloco.find("a", class_="linkProcesso")

            if link_tag:
                numero = link_tag.text.strip()
                link = "https://esaj.tjsp.jus.br" + link_tag.get("href")

                texto = bloco.get_text(separator=" ").lower()

                # 🔥 EXTRAÇÃO DE PARTES
                autor = ""
                reu = ""

                if "requerente:" in texto:
                    try:
                        autor = texto.split("requerente:")[1].split("requerido:")[0].strip()
                    except:
                        pass

                if "requerido:" in texto:
                    try:
                        reu = texto.split("requerido:")[1].split("\n")[0].strip()
                    except:
                        pass

                resultados.append({
                    "Tribunal": "TJSP",
                    "Processo": numero,
                    "Classe": texto,
                    "Autor": autor,
                    "Réu": reu,
                    "Data": "-",
                    "Link": link
                })

    return resultados
