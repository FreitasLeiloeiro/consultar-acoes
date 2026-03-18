import requests

API_KEY = " eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiNDMwMDAwYzNlOGZjYmY5N2U4MzlmYzQwMzNjZDc0YWQxNTJmYjE1YWM5MzliNjI4NGZiZmFiZTliNjEyODY1YzkwMDgxMmJkY2EyNjIyMmYiLCJpYXQiOjE3NzM4NTc4NTIuNTA5MTQ2LCJuYmYiOjE3NzM4NTc4NTIuNTA5MTQ3LCJleHAiOjIwODk0NzcwNTIuNTA3NzE0LCJzdWIiOiIzMzA4MzI2Iiwic2NvcGVzIjpbImFjZXNzYXJfYXBpX3BhZ2EiLCJhY2Vzc2FyX2FwaV9wbGF5Z3JvdW5kIl19.CDGKSdktp_ruBD1j669zy_KZemjtyK7h7xGgSBQyJrXDxta6SqOnUoD9NoXZbuJLcuLgpniloa-1TRUuQJtQTAGa_xequys99MSIxf4MNVviTERaXrAS1w9ecluGt9J-9FPpj6ffphLwMTO6T1fEDPk_-hngcqf1pxY7hq4844zpct8Hka68cGk13WaE4CgvKRsmIkEj6WFLNM_h_XDw4Fjjz2-qRu3duhFOP0JP4Sy7hRzYPjUwD1o5wAomoD2fcyFfeLXmD46INcvgE4dAqzRMOJgLlZz7ZJgkAaDyVrLiUjhyiFRtGlhjLQZaRlKlZNHP31m9KFUIbj9L6esP4-nxIfDNKJErcnrmC5riamy_WAR1Ehz-jsUnr5JkPtFT5G9Vkf_YO2QTAbsnZ9vTZJjybWmki4ecHVH3cbmwdKwsLEgeJoiUJ9781fKO2A1ceanxlmYpvkQf0P2psDv7U_ngXILsjsgNmX2hKtG4ujRgn-sEO9gnTbRnYDLEMzLwGQjo7Yw0OJe8Tt75ZlA2SEpR--LaMP-ShJQt3pyYHgV2AkgX6D08JyQUl5wSJtWh_Gii7206VdTgY2rw0iHPxFa61mVrRpCriBVDN-lld8cCaS9_eOjIWoBPNFZX80Wz3k5HGUKLTb-chNxcRxUgWV4vxAR5ry7qnMHuijcVYG4
"

def buscar_tjsp(nome):

    url = f"https://api.escavador.com/api/v2/pessoas?nome={nome}"

    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }

    response = requests.get(url, headers=headers)

    resultados = []

    if response.status_code == 200:

        data = response.json()

        for pessoa in data.get("items", []):

            for processo in pessoa.get("processos", []):

                numero = processo.get("numero_cnj", "")

                resultados.append({
                    "Tribunal": processo.get("tribunal", "TJSP"),
                    "Processo": numero,
                    "Classe": processo.get("classe", "Processo judicial"),
                    "Data": processo.get("data_inicio", ""),
                    "Link": f"https://www.escavador.com/processos/{numero}"
                })

    return resultados
