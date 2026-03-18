import requests
from bs4 import BeautifulSoup

def extrair_partes(link):

    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(link, headers=headers, timeout=10)

        if response.status_code != 200:
            return "", ""

        soup = BeautifulSoup(response.text, "html.parser")

        texto = soup.get_text(" ").lower()

        autor = ""
        reu = ""

        if "requerente:" in texto and "requerido:" in texto:
            try:
                autor = texto.split("requerente:")[1].split("requerido:")[0].strip()
                reu = texto.split("requerido:")[1].split("advogado")[0].strip()
            except:
                pass

        return autor, reu

    except:
        return "", ""


def buscar_tjsp(nome):

    resultados = []

    try:
        url = "https://esaj.tjsp.jus.br/cpopg/search.do"

        params = {
            "dadosConsulta.valorConsulta": nome
        }

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(url, params=params, headers=headers, timeout=10)

        if response.status_code != 200:
            return []

        soup = BeautifulSoup(response.text, "html.parser")

        links = soup.find_all("a", class_="linkProcesso")

        for link_tag in links[:5]:  # ⚠️ LIMITADO (importante)

            numero = link_tag.text.strip()
            link = "https://esaj.tjsp.jus.br" + link_tag.get("href")

            # 🔥 EXTRAÇÃO REAL
            autor, reu = extrair_partes(link)

            resultados.append({
                "Tribunal": "TJSP",
                "Processo": numero,
                "Classe": "Processo judicial",
                "Autor": autor,
                "Réu": reu,
                "Data": "-",
                "Link": link
            })

        return resultados

    except:
        return []
