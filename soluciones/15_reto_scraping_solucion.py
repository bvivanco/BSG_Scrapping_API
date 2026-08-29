"""
15 · SOLUCIÓN del reto de Web Scraping
=======================================
Capítulos 3 y 4

    python soluciones/15_reto_scraping_solucion.py
"""

import time
from pathlib import Path
from urllib.parse import urljoin

import pandas as pd
import requests
from bs4 import BeautifulSoup

SALIDAS = Path(__file__).resolve().parent.parent / "salidas"
SALIDAS.mkdir(exist_ok=True)

URL = "https://quotes.toscrape.com/"
HEADERS = {"User-Agent": "BSG-Curso-Scraping/1.0 (ejercicio academico)"}
MAX_PAGINAS = 3
PAUSA = 1.0


def extraer_frases(sopa):
    """Devuelve la lista de frases de UNA página ya parseada."""
    resultado = []
    for bloque in sopa.select("div.quote"):
        texto = bloque.select_one("span.text").get_text(strip=True)
        resultado.append({
            "frase": texto.strip("“”\""),                     # RETO 4.1
            "autor": bloque.select_one("small.author").get_text(strip=True),
            "tags": ";".join(a.get_text(strip=True) for a in bloque.select("a.tag")),
            "largo": len(texto.strip("“”\"")),                # RETO 4.2
        })
    return resultado


# ---- RETO 1, 2 y 3: recorrer las páginas -----------------------------------
print("=" * 70)
print("RECORRIENDO EL SITIO")
print("=" * 70)

url = URL
pagina = 1
frases = []

while url and pagina <= MAX_PAGINAS:
    r = requests.get(url, headers=HEADERS, timeout=10)      # RETO 1.1
    print(f"   Página {pagina}: {url} → {r.status_code}")   # RETO 1.2
    r.raise_for_status()
    r.encoding = r.apparent_encoding                        # RETO 1.3

    sopa = BeautifulSoup(r.text, "html.parser")             # RETO 1.4
    nuevas = extraer_frases(sopa)                           # RETO 2
    frases.extend(nuevas)
    print(f"      {len(nuevas)} frases (acumulado: {len(frases)})")

    siguiente = sopa.select_one("li.next a")                # RETO 3.1
    url = urljoin(url, siguiente["href"]) if siguiente else None
    pagina += 1
    if url:
        time.sleep(PAUSA)                                   # RETO 3.2

print(f"\n   TOTAL: {len(frases)} frases")                  # RETO 3.3


# ---- RETO 4: guardar --------------------------------------------------------
print("\n" + "=" * 70)
print("GUARDANDO")
print("=" * 70)

df = pd.DataFrame(frases)
salida = SALIDAS / "frases.csv"
df.to_csv(salida, index=False, encoding="utf-8-sig")        # RETO 4.3

print(f"   {len(df)} filas → salidas/{salida.name}\n")
print(df[["autor", "largo", "tags"]].head(5).to_string(index=False))


# ---- EXTRA ------------------------------------------------------------------
print("\n" + "=" * 70)
print("EXTRA — análisis rápido con pandas")
print("=" * 70)

print("   Autores con más frases:")
for autor, n in df["autor"].value_counts().head(5).items():
    print(f"      {autor:<28} {n}")

etiquetas = df["tags"].str.split(";").explode()
etiquetas = etiquetas[etiquetas != ""]
print("\n   Etiquetas más repetidas:")
for tag, n in etiquetas.value_counts().head(5).items():
    print(f"      {tag:<28} {n}")

print(f"\n   Frase más larga ({df['largo'].max()} caracteres):")
print(f"      {df.loc[df['largo'].idxmax(), 'frase'][:100]}...")
