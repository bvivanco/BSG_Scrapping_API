"""
12 · XPath: la ruta hasta el dato
==================================
Capítulo 3 · Sesión 1 · Bloque 3

XPath es la "ruta de carpetas" de una página web.
    C:/Usuarios/Bryan/Documentos     ← ruta de archivos
    /html/body/div/p                 ← ruta de etiquetas

    pip install lxml
    python 12_xpath_lxml.py
"""

from pathlib import Path

import requests
from lxml import html as lxml_html

DATA = Path(__file__).parent / "data"


# ============================================== 1) La sintaxis mínima ======
print("=" * 70)
print("1) LA SINTAXIS MÍNIMA (esto es el 95 % de lo que usarás)")
print("=" * 70)

EJEMPLO = """
<body>
  <div id="cabecera"><h1>Curso BSG</h1></div>
  <div class="lista">
    <p class="precio">S/ 120.00</p>
    <p class="precio oferta">S/ 89.90</p>
    <a href="/detalle/1">Ver más</a>
  </div>
</body>
"""

arbol = lxml_html.fromstring(EJEMPLO)

pruebas = [
    ("//p",                              "todos los <p>, estén donde estén"),
    ("//div/p",                          "los <p> que son HIJO DIRECTO de un div"),
    ("//p[@class='precio']",             "los <p> cuyo class es exactamente 'precio'"),
    ("//p[contains(@class,'precio')]",   "los <p> cuyo class CONTIENE 'precio'"),
    ("//h1/text()",                      "el TEXTO del h1"),
    ("//a/@href",                        "el ATRIBUTO href del enlace"),
    ("//p[1]",                           "el primer <p> de cada grupo (¡empieza en 1, no en 0!)"),
    ("//div[@id='cabecera']//text()",    "todo el texto dentro de ese div"),
]

for expr, explicacion in pruebas:
    res = arbol.xpath(expr)
    limpio = [x.text_content().strip() if hasattr(x, "text_content") else str(x).strip()
              for x in res]
    limpio = [x for x in limpio if x]
    print(f"\n   {expr}")
    print(f"      {explicacion}")
    print(f"      → {limpio}")

print("\n   ★ Fíjate en la diferencia clave:")
print("      class='precio'          NO encuentra el que tiene class='precio oferta'")
print("      contains(@class,'precio') SÍ lo encuentra")
print("      En webs modernas un elemento suele tener 4 o 5 clases juntas,")
print("      por eso contains() te salva la vida.")


# ============================================== 2) Tabla de símbolos =======
print("\n" + "=" * 70)
print("2) LOS SÍMBOLOS, EN UNA TABLA")
print("=" * 70)
print("""
   /            hijo directo, un nivel exacto
   //           en cualquier nivel, tan profundo como haga falta   ← el más usado
   @            atributo            //div[@class='titulo']
   [ ]          condición o posición   //tr[2]   //li[last()]
   text()       el texto del nodo    //h1/text()
   contains()   coincidencia parcial //div[contains(@class,'precio')]
   .            el nodo actual (útil cuando ya estás parado en un elemento)
   ..           el padre
""")
print("   ★ XPath NO calcula: solo SELECCIONA. El cálculo va después, en Python.")


# ============================================== 3) La trampa de Chrome =====
print("\n" + "=" * 70)
print("3) LA TRAMPA DEL 'COPY FULL XPATH' DE CHROME")
print("=" * 70)

absoluto = "/body/div[2]/p[1]"
relativo = "//p[@class='precio']"

print(f"   Lo que copia Chrome  : {absoluto}")
print(f"      → {[e.text for e in arbol.xpath(absoluto)]}")
print(f"   Lo que deberías usar : {relativo}")
print(f"      → {[e.text for e in arbol.xpath(relativo)]}")
print("\n   Los dos devuelven lo mismo HOY. Pero si mañana el diseñador agrega")
print("   un <div> arriba, el absoluto apunta a otra cosa y tu scraper miente")
print("   en silencio. El relativo sigue funcionando.")
print("\n   ★ Regla: usa Chrome para DESCUBRIR el elemento, no para copiar la ruta.")


# ============================================== 4) Página real =============
print("\n" + "=" * 70)
print("4) EN LA PÁGINA REAL")
print("=" * 70)

local = DATA / "books_home.html"
if local.exists():
    contenido = local.read_text(encoding="utf-8")
    print(f"   Usando el HTML local ({local.name}).")
else:
    resp = requests.get("https://books.toscrape.com/", timeout=10)
    resp.encoding = resp.apparent_encoding
    contenido = resp.text
    print("   Descargado del servidor (corre antes el script 10 para trabajar offline).")

doc = lxml_html.fromstring(contenido)

titulos = doc.xpath("//article[@class='product_pod']//h3/a/@title")
precios = doc.xpath("//article[@class='product_pod']//p[@class='price_color']/text()")
enlaces = doc.xpath("//article[@class='product_pod']//h3/a/@href")

print(f"\n   //article[@class='product_pod']//h3/a/@title  → {len(titulos)} títulos")
print(f"   //p[@class='price_color']/text()             → {len(precios)} precios")
print(f"   //h3/a/@href                                 → {len(enlaces)} enlaces\n")

for t, p in list(zip(titulos, precios))[:5]:
    print(f"      {t[:45]:<45} {p:>9}")


# ============================================== 5) XPath vs BeautifulSoup ==
print("\n" + "=" * 70)
print("5) ¿XPATH O BEAUTIFULSOUP? LAS DOS SIRVEN")
print("=" * 70)
print("""
   Objetivo                    XPath (lxml)                  BeautifulSoup
   -------------------------   ---------------------------   -------------------------
   todos los <p>               //p                           find_all('p')
   por clase                   //div[@class='caja']          find_all('div', class_='caja')
   por id                      //*[@id='total']              find(id='total')
   el texto                    //h1/text()                   find('h1').text
   un atributo                 //a/@href                     find('a')['href']
   clase parcial               //div[contains(@class,'x')]   select('div[class*=x]')

   · BeautifulSoup se lee más fácil y perdona HTML mal escrito → ideal para empezar.
   · XPath es más potente (puede subir al padre con '..') y es NATIVO en Scrapy.
   · En la práctica se usan los dos. Aprende ambos: son 20 minutos cada uno.
""")

print("=" * 70)
print("SIGUIENTE → 13_scraping_a_tabla.py (del HTML sucio al CSV limpio)")
print("=" * 70)
