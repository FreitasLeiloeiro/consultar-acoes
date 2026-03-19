import requests
from bs4 import BeautifulSoup

def buscar_tjsp(nome):

    resultados = []

    try:
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

        soup = BeautifulSoup(response.text, "html.parser")

        processos = soup.find_all("a", class_="linkProcesso")

        for processo in processos:

            numero = processo.text.strip()
            link = "https://esaj.tjsp.jus.br" + processo.get("href")

            resultados.append({
                "Tribunal": "TJSP",
                "Processo": numero,
                "Classe": "Processo judicial",
                "Data": "-",
                "Link": link
            })

        return resultados

    except:
        return []
