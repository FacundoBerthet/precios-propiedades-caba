# Precios de propiedades en CABA

Scraping y análisis de precios de propiedades en venta en Ciudad Autónoma de Buenos Aires. Los datos se obtienen de ZonaProp y se analizan en notebooks de Jupyter.

## Qué hace el proyecto

1. Scrapea todas las propiedades en venta de ZonaProp para CABA (~38k registros)
2. Limpia y convierte los datos a un formato utilizable
3. Analiza la distribución de precios, metros, expensas y su relación con el barrio

## Dataset

Las columnas que se extraen son:

| Columna | Descripción |
|---|---|
| precio | Precio de venta en USD |
| expensas | Expensas mensuales en ARS (puede ser 0 si no figura) |
| metros | Superficie total en m² |
| ambientes | Cantidad de ambientes |
| banos | Cantidad de baños |
| barrio | Barrio según nomenclatura del GCBA |
| comuna | Comuna a la que pertenece el barrio |

## Estructura

```
scraping/
    zonaprop.py         # script de scraping
notebooks/
    01-exploracion.ipynb    # exploración del dataset crudo
    02-limpieza.ipynb       # limpieza y transformación
    03-eda.ipynb            # análisis exploratorio
data/
    raw/                # datos crudos (no versionados)
    processed/          # datos limpios (no versionados)
```

## Cómo ejecutar

Instalar dependencias:

```bash
pip install -r requirements.txt
```

Correr el scraping (guarda en `data/raw/zonaprop_raw.csv`):

```bash
python scraping/zonaprop.py
```

Después abrir los notebooks en orden.

## Algunos resultados

- Puerto Madero tiene la mediana de precio más alta (~USD 630k), casi 7 veces más que Floresta o La Boca
- Los metros cuadrados tienen la correlación más alta con el precio (0.68), seguido por baños (0.63) y ambientes (0.50)
- El 42% de las propiedades no tiene expensas publicadas

## Tecnologías

- Python 3
- pandas, numpy, matplotlib
- requests, BeautifulSoup4
- Jupyter
