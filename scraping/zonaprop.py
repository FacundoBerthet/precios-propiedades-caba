import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# ── Configuración ──────────────────────────────────────────
URL_BASE = "https://www.zonaprop.com.ar/inmuebles-venta-capital-federal"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:150.0) Gecko/20100101 Firefox/150.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Referer": "https://www.zonaprop.com.ar/",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
}
PAUSA_ENTRE_PAGINAS = 2  # segundos


# ── Funciones ──────────────────────────────────────────────
def obtener_url(pagina):
    if pagina == 1:
        return f"{URL_BASE}.html"
    return f"{URL_BASE}-pagina-{pagina}.html"


def obtener_html(url):
    respuesta = requests.get(url, headers=HEADERS)
    if respuesta.status_code != 200:
        print(f"Error {respuesta.status_code} en {url}")
        return None
    return respuesta.text


def parsear_features(card):
    """Extrae m², ambientes y baños del bloque de features"""
    metros, ambientes, banos = None, None, None
    features = card.find("h3", {"data-qa": "POSTING_CARD_FEATURES"})
    if features:
        spans = features.find_all("span")
        for span in spans:
            texto = span.text.strip()
            if "m²" in texto:
                metros = texto
            elif "amb" in texto:
                ambientes = texto
            elif "baño" in texto:
                banos = texto
    return metros, ambientes, banos


def parsear_card(card):
    """Extrae todos los datos de una card"""

    # Precio
    precio_tag = card.find("h2", {"data-qa": "POSTING_CARD_PRICE"})
    precio = precio_tag.text.strip() if precio_tag else None

    # Expensas
    expensas_tag = card.find("h2", {"data-qa": "expensas"})
    expensas = expensas_tag.text.strip() if expensas_tag else None

    # Features
    metros, ambientes, banos = parsear_features(card)

    # Dirección
    direccion_tag = card.find("h4", class_="postingLocations-module__location-address")
    direccion = direccion_tag.text.strip() if direccion_tag else None

    # Barrio
    barrio_tag = card.find("h4", {"data-qa": "POSTING_CARD_LOCATION"})
    barrio = barrio_tag.text.strip() if barrio_tag else None

    return {
        "precio": precio,
        "expensas": expensas,
        "metros": metros,
        "ambientes": ambientes,
        "banos": banos,
        "direccion": direccion,
        "barrio": barrio,
    }


def scrapear_pagina(html):
    """Extrae todas las cards de una página"""
    soup = BeautifulSoup(html, "html.parser")

    # Solo cards de tipo PROPERTY (no DEVELOPMENT)
    cards = soup.find_all(
        "div",
        {"data-qa": lambda x: x and "posting PROPERTY" in x}
    )

    resultados = []
    for card in cards:
        datos = parsear_card(card)
        resultados.append(datos)

    return resultados


def scrapear_todo():
    todos = []
    pagina = 1

    while True:
        url = obtener_url(pagina)
        print(f"Scrapeando página {pagina}: {url}")

        html = obtener_html(url)
        if html is None:
            print("Error en la request, cortando.")
            break

        resultados = scrapear_pagina(html)
        
        # Si no hay cards, llegamos al final
        if len(resultados) == 0:
            print(f"Sin resultados en página {pagina}, fin del scraping.")
            break

        todos.extend(resultados)

        # Guardado incremental
        pd.DataFrame(todos).to_csv("data/raw/zonaprop_raw.csv", index=False)
        
        print(f"  → {len(resultados)} propiedades | Total acumulado: {len(todos)}")
        
        pagina += 1
        time.sleep(PAUSA_ENTRE_PAGINAS)

    return pd.DataFrame(todos)


# ── Main ───────────────────────────────────────────────────
if __name__ == "__main__":
    df = scrapear_todo()
    print(f"\nTotal: {len(df)} propiedades")
    print(df.head())
    df.to_csv("../data/raw/zonaprop_raw.csv", index=False)
    print("Guardado en data/raw/zonaprop_raw.csv")