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

        # 🔥 TIMEOUT CURTO (ESSENCIAL)
        response = requests.get(url, params=params, headers=headers, timeout=8)

        # 🔥 SE NÃO RESPONDER CERTO → ABORTA
        if response.status_code != 200:
            return []

        soup = BeautifulSoup(response.text, "html.parser")

        processos = soup.find_all("a", class_="linkProcesso")

        for processo in processos[:20]:  # 🔥 LIMITE PARA EVITAR LENTIDÃO

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

    except requests.exceptions.Timeout:
        print("Timeout TJSP")
        return []

    except Exception as e:
        print("Erro TJSP:", e)
        return []
