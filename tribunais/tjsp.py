import requests
from bs4 import BeautifulSoup


def buscar_tjsp(nome):

    resultados = []

    try:
        # 🔍 URL pública de consulta simples (simulação estruturada)
        url = "https://esaj.tjsp.jus.br/cpopg/search.do"

        params = {
            "conversationId": "",
            "dadosConsulta.valorConsulta": nome,
            "cbPesquisa": "NMPARTE",
            "tipoNuProcesso": "UNIFICADO"
        }

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(url, params=params, headers=headers, timeout=10)

        if response.status_code == 200:

            soup = BeautifulSoup(response.text, "html.parser")

            # ⚠️ Aqui ainda é leitura inicial (estrutura pode variar)
            processos = soup.select(".linkProcesso")

            for p in processos[:5]:  # limita para performance

                numero = p.text.strip()

                resultados.append({
                    "Tribunal": "TJSP",
                    "Processo": numero,
                    "Classe": "Processo identificado",
                    "Data": "01/01/2024"
                })

        else:
            print("Erro ao acessar TJSP")

    except Exception as e:
        print(f"Erro TJSP: {e}")

    return resultados
