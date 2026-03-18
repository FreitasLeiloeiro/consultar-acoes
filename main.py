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

        # 🔍 Busca apenas os links de processo (forma mais estável)
        links = soup.find_all("a", class_="linkProcesso")

        for link_tag in links[:10]:

            try:
                numero = link_tag.text.strip()
            except:
                continue

            try:
                link = "https://esaj.tjsp.jus.br" + link_tag.get("href")
            except:
                link = ""

            # ⚠️ Autor e Réu ainda não extraídos (vamos evoluir depois)
            autor = ""
            reu = ""

            resultados.append({
                "Tribunal": "TJSP",
                "Processo": numero,
                "Classe": "Processo judicial",
                "Autor": autor,
                "Réu": reu,
                "Data": "-",
                "Link": link
            })

    except Exception as e:
        # evita quebrar o Streamlit
        return []

    return resultados
