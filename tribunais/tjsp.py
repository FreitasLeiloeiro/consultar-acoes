def buscar_tjsp(nome):

    resultados = []

    # ⚠️ Simulação com link real estruturado
    processos_exemplo = [
        "1001234-22.2024.8.26.0100",
        "1005678-55.2023.8.26.0100"
    ]

    for numero in processos_exemplo:

        link = f"https://esaj.tjsp.jus.br/cpopg/show.do?processo.codigo={numero}"

        resultados.append({
            "Tribunal": "TJSP",
            "Processo": numero,
            "Link": link,
            "Classe": "Ação Revisional",
            "Data": "01/01/2024"
        })

    return resultados
