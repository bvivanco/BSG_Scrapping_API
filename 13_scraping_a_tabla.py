"""
13 · Del HTML sucio a la tabla limpia
======================================
Capítulo 4 · Sesión 1 — Limpieza y almacenamiento

Este es el paso que no aparece en los tutoriales y se lleva la mitad del tiempo
de cualquier proyecto real: el dato scrapeado SIEMPRE llega sucio.

    "£51.77"              →  51.77   (float)
    "star-rating Three"   →  3       (int)
    "\\n\\n  In stock  \\n"  →  True    (bool)

    python 13_scraping_a_tabla.py
"""

import json
import re
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup

BASE = Path(__file__).parent
SALIDAS = BASE / "salidas"
SALIDAS.mkdir(exist_ok=True)

URL = "https://books.toscrape.com/"
HEADERS = {"User-Agent": "BSG-Curso-Scraping/1.0 (ejercicio academico)"}


# ============================================== 1) Extraer en crudo ========
print("=" * 70)
print("1) PRIMERO EXTRAEMOS TAL CUAL VIENE (sin limpiar nada)")
print("=" * 70)

r = requests.get(URL, headers=HEADERS, timeout=10)
r.raise_for_status()
r.encoding = r.apparent_encoding          # ← acuérdate del encoding

soup = BeautifulSoup(r.text, "html.parser")
crudos = []

for libro in soup.select("article.product_pod"):
    crudos.append({
        "titulo": libro.h3.a["title"],
        "precio": libro.select_one("p.price_color").text,
        "rating": libro.select_one("p.star-rating")["class"],
        "stock": libro.select_one("p.instock").text,
        "enlace": libro.h3.a["href"],
    })

print(f"   {len(crudos)} libros extraídos. Así se ve el primero:\n")
for k, v in crudos[0].items():
    print(f"      {k:<8} = {v!r}")

print("\n   ★ Mira los tipos: TODO es texto. El precio no se puede sumar,")
print("     el rating es una lista de clases CSS y el stock trae saltos de línea.")


# ============================================== 2) Funciones de limpieza ===
print("\n" + "=" * 70)
print("2) UNA FUNCIÓN DE LIMPIEZA POR CAMPO")
print("=" * 70)

PALABRAS_RATING = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


def precio_a_float(texto):
    """'£51.77' → 51.77 · quita moneda, comas y espacios."""
    numero = re.sub(r"[^\d.]", "", texto)      # deja solo dígitos y el punto
    return float(numero) if numero else None


def rating_a_numero(clases):
    """['star-rating', 'Three'] → 3"""
    for c in clases:
        if c in PALABRAS_RATING:
            return PALABRAS_RATING[c]
    return None


def hay_stock(texto):
    """'\\n In stock \\n' → True"""
    return "in stock" in texto.strip().lower()


def url_absoluta(href):
    """'catalogue/x/index.html' → 'https://books.toscrape.com/catalogue/x/index.html'"""
    from urllib.parse import urljoin
    return urljoin(URL, href)


ejemplo = crudos[0]
print(f"   precio_a_float({ejemplo['precio']!r}) → {precio_a_float(ejemplo['precio'])}")
print(f"   rating_a_numero({ejemplo['rating']}) → {rating_a_numero(ejemplo['rating'])}")
print(f"   hay_stock({ejemplo['stock']!r}) → {hay_stock(ejemplo['stock'])}")
print("\n   ★ Funciones cortas y con nombre claro. Así, cuando el sitio cambie,")
print("     arreglas UNA función y no 300 líneas.")


# ============================================== 3) Aplicar la limpieza =====
print("\n" + "=" * 70)
print("3) APLICAR LA LIMPIEZA A TODO")
print("=" * 70)

limpios = [{
    "titulo": c["titulo"].strip(),
    "precio_gbp": precio_a_float(c["precio"]),
    "rating": rating_a_numero(c["rating"]),
    "en_stock": hay_stock(c["stock"]),
    "url": url_absoluta(c["enlace"]),
} for c in crudos]

print("   El primer libro, ya limpio:\n")
for k, v in limpios[0].items():
    print(f"      {k:<11} = {v!r:<50} {type(v).__name__}")


# ============================================== 4) A pandas ================
print("\n" + "=" * 70)
print("4) A UN DataFrame — igual que hicimos con el JSON en el capítulo 2")
print("=" * 70)

df = pd.DataFrame(limpios)

print(f"   Dimensiones: {df.shape[0]} filas × {df.shape[1]} columnas\n")
print(df[["titulo", "precio_gbp", "rating", "en_stock"]].head(8).to_string(index=False))

print("\n   Tipos de dato (esto es lo que ganamos al limpiar):")
for col, tipo in df.dtypes.items():
    print(f"      {col:<12} → {tipo}")

print("\n   Y ahora YA se puede analizar:")
print(f"      Precio promedio  : £{df['precio_gbp'].mean():.2f}")
print(f"      Precio máximo    : £{df['precio_gbp'].max():.2f}  ({df.loc[df['precio_gbp'].idxmax(), 'titulo'][:40]})")
print(f"      Rating promedio  : {df['rating'].mean():.2f} estrellas")
print(f"      Con stock        : {int(df['en_stock'].sum())} de {len(df)}")


# ============================================== 5) Puente con el cap. 2 ====
print("\n" + "=" * 70)
print("5) PUENTE CON EL CAPÍTULO 2: SCRAPING + API JUNTOS")
print("=" * 70)
print("   Los precios están en libras. Para pasarlos a soles NO se scrapea:")
print("   se usa una API. Cada herramienta para lo suyo.\n")

try:
    tc = requests.get("https://open.er-api.com/v6/latest/GBP", timeout=10)
    tc.raise_for_status()
    gbp_pen = tc.json()["rates"]["PEN"]
    df["precio_pen"] = (df["precio_gbp"] * gbp_pen).round(2)
    print(f"   1 GBP = {gbp_pen} PEN  (API open.er-api.com)\n")
    print(df[["titulo", "precio_gbp", "precio_pen"]].head(5).to_string(index=False))
except requests.RequestException as e:
    print(f"   (No se pudo consultar el tipo de cambio: {type(e).__name__})")

print("\n   ★ Este es el patrón profesional: el HTML da lo que no tiene API,")
print("     la API da lo que no debería scrapearse. Se combinan.")


# ============================================== 6) Guardar ================
print("\n" + "=" * 70)
print("6) ALMACENAR: CSV, JSON Y EXCEL")
print("=" * 70)

csv_path = SALIDAS / "libros.csv"
json_path = SALIDAS / "libros.json"

df.to_csv(csv_path, index=False, encoding="utf-8-sig")
print(f"   CSV   → {csv_path.relative_to(BASE)}")
print("           ★ utf-8-sig, NO utf-8: es lo que hace que Excel muestre bien las tildes.")

json_path.write_text(
    json.dumps(limpios, indent=2, ensure_ascii=False), encoding="utf-8"
)
print(f"   JSON  → {json_path.relative_to(BASE)}   (ensure_ascii=False para las tildes)")

try:
    xlsx_path = SALIDAS / "libros.xlsx"
    df.to_excel(xlsx_path, index=False, sheet_name="libros")
    print(f"   Excel → {xlsx_path.relative_to(BASE)}")
except ImportError:
    print("   Excel → (opcional: pip install openpyxl)")

print("\n   Para una base de datos sería igual de corto:")
print("      df.to_sql('libros', con=engine, if_exists='append', index=False)")

print("\n" + "=" * 70)
print("SIGUIENTE → 14_paginacion_y_detalle.py (20 libros está bien... ¿y 1000?)")
print("=" * 70)
