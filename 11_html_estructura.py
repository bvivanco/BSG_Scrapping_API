"""
11 · Leer el HTML con BeautifulSoup
====================================
Capítulo 3 · Sesión 1 · Bloque 3

requests trae el HTML (el cartero). BeautifulSoup lo entiende (la lupa).

    pip install beautifulsoup4 lxml
    python 11_html_estructura.py

Requiere haber corrido antes 10_scraping_primer_html.py (guarda el HTML local).
"""

from pathlib import Path

import requests
from bs4 import BeautifulSoup

DATA = Path(__file__).parent / "data"


# ============================================== 1) El árbol de la clase ====
print("=" * 70)
print("1) EL MISMO EJEMPLO DE LA DIAPOSITIVA: PADRES, HIJOS Y HERMANOS")
print("=" * 70)

HTML_CLASE = """
<body>
  <div id="saludo" class="contenedor">
    <p class="texto">Buenas noches</p>
    <span class="texto">Hola nuevamente!</span>
    <a href="https://bsg.edu.pe/curso">Ver el curso</a>
  </div>
</body>
"""

sopa = BeautifulSoup(HTML_CLASE, "html.parser")

div = sopa.find("div")
print(f"   El <div> es hijo de       : <{div.parent.name}>")
print(f"   Hijos directos del <div>  : {[h.name for h in div.find_all(recursive=False)]}")
print(f"   <p> y <span> son          : HERMANOS (mismo padre)")
print(f"   Texto del <p>             : {sopa.find('p').text!r}")
print(f"   Enlace del <a>            : {sopa.find('a')['href']!r}")

print("\n   ★ Regla: toda etiqueta abre y cierra. Lo que está en medio son sus hijos.")


# ============================================== 2) find vs find_all ========
print("\n" + "=" * 70)
print("2) find() TRAE UNO · find_all() TRAE TODOS")
print("=" * 70)

print(f"   sopa.find('p')                → {sopa.find('p')}")
print(f"   sopa.find_all(class_='texto') → {len(sopa.find_all(class_='texto'))} elementos")
print("\n   ★ OJO: se escribe class_ con guion bajo, porque 'class' es palabra")
print("     reservada de Python. Es el error #1 de los que empiezan.")
print("\n   ★ find() devuelve None si no encuentra nada (no da error).")
print(f"   sopa.find('table') → {sopa.find('table')}   ← None, no explota")
print("     Por eso SIEMPRE valida antes de pedir .text, o tendrás:")
print("     AttributeError: 'NoneType' object has no attribute 'text'")


# ============================================== 3) Atributos ===============
print("\n" + "=" * 70)
print("3) ATRIBUTOS: class (grupo) · id (único) · href (a dónde lleva)")
print("=" * 70)

print(f"   div['id']              → {div['id']!r}          (único en la página)")
print(f"   div['class']           → {div['class']}   (¡es una LISTA!)")
print(f"   div.get('data-precio') → {div.get('data-precio')}   (get no explota si no existe)")
print("\n   ★ Usa siempre .get() con atributos que quizá no estén.")


# ============================================== 4) Página real =============
print("\n" + "=" * 70)
print("4) AHORA EN UNA PÁGINA REAL: books.toscrape.com")
print("=" * 70)

local = DATA / "books_home.html"
if local.exists():
    html = local.read_text(encoding="utf-8")
    print(f"   Usando el HTML local ({local.name}) — cero peticiones al servidor.")
else:
    print("   No hay HTML local; lo pido al servidor (corre antes el script 10).")
    resp = requests.get("https://books.toscrape.com/", timeout=10)
    resp.encoding = resp.apparent_encoding
    html = resp.text

soup = BeautifulSoup(html, "html.parser")

libros = soup.find_all("article", class_="product_pod")
print(f"\n   Libros encontrados con find_all('article', class_='product_pod'): {len(libros)}")
print("\n   ★ ¿Por qué funciona? Porque los 20 libros COMPARTEN la misma clase.")
print("     Eso es exactamente para lo que sirve 'class': marcar un grupo.\n")

print(f"   {'#':<3} {'TÍTULO':<42} {'PRECIO':>9}  {'STOCK':<9}")
print("   " + "-" * 68)
for i, libro in enumerate(libros[:5], 1):
    titulo = libro.h3.a["title"]                       # el título completo está en el atributo
    precio = libro.find("p", class_="price_color").text
    stock = libro.find("p", class_="instock").get_text(strip=True)
    print(f"   {i:<3} {titulo[:42]:<42} {precio:>9}  {stock:<9}")
print(f"   ... ({len(libros)} en total)")


# ============================================== 5) select() con CSS ========
print("\n" + "=" * 70)
print("5) LA OTRA FORMA: select() CON SELECTORES CSS")
print("=" * 70)

print("   Lo mismo de arriba, escrito como CSS:\n")
print("   soup.select('article.product_pod')          → todos los libros")
print("   soup.select('article.product_pod h3 a')     → los enlaces del título")
print("   soup.select_one('p.price_color')            → el primer precio\n")

titulos_css = soup.select("article.product_pod h3 a")
print(f"   select() encontró {len(titulos_css)} títulos. El primero: {titulos_css[0]['title']!r}")
print(f"   select_one('p.price_color') → {soup.select_one('p.price_color').text!r}")

print("\n   Chuleta de traducción:")
print("      etiqueta      →  'div'            find('div')")
print("      .clase        →  '.precio'        find(class_='precio')")
print("      #id           →  '#total'         find(id='total')")
print("      descendiente  →  'div p'          (un p dentro de un div)")
print("      combinado     →  'article.product_pod h3 a'")


# ============================================== 6) Los enlaces =============
print("\n" + "=" * 70)
print("6) href: EL ATRIBUTO QUE PERMITE SEGUIR NAVEGANDO")
print("=" * 70)

enlaces = [a["href"] for a in soup.select("article.product_pod h3 a")]
print(f"   Enlaces al detalle de cada libro (primeros 3):")
for e in enlaces[:3]:
    print(f"      {e}")

siguiente = soup.select_one("li.next a")
print(f"\n   Enlace a la página siguiente: {siguiente['href'] if siguiente else 'no hay'}")
print("\n   ★ Sin href no hay crawling. Con href puedes pasar del listado al detalle,")
print("     y de la página 1 a la 2. Eso lo hacemos en el script 14.")

print("\n" + "=" * 70)
print("SIGUIENTE → 12_xpath_lxml.py (la otra forma de apuntar al dato)")
print("=" * 70)
