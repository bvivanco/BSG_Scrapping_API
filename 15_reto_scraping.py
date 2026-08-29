"""
15 · RETO DE LA SESIÓN — Web Scraping
======================================
Capítulos 3 y 4

Sitio: https://quotes.toscrape.com  (creado para practicar scraping: es legal y
no molesta a nadie).

Objetivo: sacar las frases, su autor y sus etiquetas, y guardarlas limpias en CSV.
Completa los TODO. Si te trabas más de 5 minutos:
    soluciones/15_reto_scraping_solucion.py

    python 15_reto_scraping.py
"""

import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup

SALIDAS = Path(__file__).parent / "salidas"
SALIDAS.mkdir(exist_ok=True)

URL = "https://quotes.toscrape.com/"
HEADERS = {"User-Agent": "BSG-Curso-Scraping/1.0 (ejercicio academico)"}

# PISTA — abre la página en Chrome, clic derecho sobre una frase → Inspeccionar.
# Vas a ver esta estructura:
#
#   <div class="quote">
#       <span class="text">“La frase...”</span>
#       <small class="author">Albert Einstein</small>
#       <div class="tags">
#           <a class="tag" href="/tag/change/">change</a>
#           <a class="tag" href="/tag/thinking/">thinking</a>
#       </div>
#   </div>


# =========================================================== RETO 1 =========
# Pedir la página y confirmar que llegó bien.
# ===========================================================================
print("=" * 70)
print("RETO 1 — Traer el HTML")
print("=" * 70)

# TODO 1.1: haz el GET a URL con headers=HEADERS y timeout=10
# r = ...

# TODO 1.2: imprime el status_code y verifica que sea 200

# TODO 1.3: arregla el encoding  (r.encoding = r.apparent_encoding)

# TODO 1.4: crea la sopa → sopa = BeautifulSoup(r.text, "html.parser")


# =========================================================== RETO 2 =========
# Extraer las 10 frases de la primera página.
# ===========================================================================
print("\n" + "=" * 70)
print("RETO 2 — Frase, autor y etiquetas")
print("=" * 70)

# TODO 2.1: encuentra todos los bloques  div.quote   (select o find_all)
# bloques = ...

# TODO 2.2: para cada bloque, saca:
#             texto  → span.text
#             autor  → small.author
#             tags   → todos los a.tag  (guárdalos separados por ";")
#           y agrégalos a la lista frases como diccionario.
frases = []

# TODO 2.3: imprime cuántas frases encontraste y las 3 primeras


# =========================================================== RETO 3 =========
# Paginación: recorrer las 3 primeras páginas.
#   El botón siguiente está en:  li.next a   y su href es relativo ('/page/2/').
#   Usa urljoin para armar la URL completa, y time.sleep(1) entre páginas.
# ===========================================================================
print("\n" + "=" * 70)
print("RETO 3 — Las 3 primeras páginas")
print("=" * 70)

MAX_PAGINAS = 3

# TODO 3.1: convierte lo del reto 2 en un bucle while con tope MAX_PAGINAS
# TODO 3.2: no olvides el time.sleep(1)
# TODO 3.3: imprime el total de frases acumuladas (deberían ser 30)


# =========================================================== RETO 4 =========
# Limpiar y guardar.
# ===========================================================================
print("\n" + "=" * 70)
print("RETO 4 — Limpiar y guardar en CSV")
print("=" * 70)

# TODO 4.1: quita las comillas tipográficas “ ” del texto de la frase
# TODO 4.2: agrega una columna con el largo de cada frase (len del texto)
# TODO 4.3: guarda todo en salidas/frases.csv con encoding="utf-8-sig"
#           (con pandas: pd.DataFrame(frases).to_csv(...))


# =========================================================== EXTRA ==========
# Si terminaste antes:
#   · ¿Qué autor tiene más frases? (pandas: value_counts)
#   · ¿Cuáles son las 5 etiquetas más repetidas?
#   · Entra al enlace "(about)" de un autor y trae su fecha de nacimiento.
# ===========================================================================
print("\n" + "=" * 70)
print("Cuando termines, compara con soluciones/15_reto_scraping_solucion.py")
print("=" * 70)
