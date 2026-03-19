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

        response = requests.get(url, params=params, headers=headers, timeout=10)

        if response.status_code != 200:
            return []

        soup = BeautifulSoup(response.text, "html.parser")

        processos = soup.find_all("a", class_="linkProcesso")

        for p in processos:

            numero = p.text.strip()
            link = "https://esaj.tjsp.jus.br" + p.get("href")

            resultados.append({
                "Tribunal": "TJSP",
                "Processo": numero,
                "Classe": "Processo judicial",
                "Data": "-",
                "Link": link
            })

        return resultados

    except Exception as e:
        print("Erro TJSP:", e)
        return []
