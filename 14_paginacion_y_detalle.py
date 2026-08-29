"""
14 · Paginación y detalle: el crawling
=======================================
Capítulo 4 · Sesión 1 — El paso 5 del ciclo: "volver al paso 2 con nuevas URLs"

Un scraper de una sola página es un ejercicio. Seguir enlaces es lo que lo
convierte en un proyecto... y también lo que puede tumbar un servidor.
Por eso aquí aparecen los tres frenos: LÍMITE, PAUSA y SESIÓN.

    python 14_paginacion_y_detalle.py
"""

import time
from pathlib import Path
from urllib.parse import urljoin

import pandas as pd
import requests
from bs4 import BeautifulSoup

BASE = Path(__file__).parent
SALIDAS = BASE / "salidas"
SALIDAS.mkdir(exist_ok=True)

INICIO = "https://books.toscrape.com/"

# ---- Los tres frenos, arriba y visibles ------------------------------------
MAX_PAGINAS = 3        # nunca dejes un while sin tope
PAUSA = 1.0            # segundos entre peticiones: cortesía mínima
HEADERS = {"User-Agent": "BSG-Curso-Scraping/1.0 (ejercicio academico)"}

# Una Session reutiliza la conexión TCP: más rápido y menos carga para el servidor.
sesion = requests.Session()
sesion.headers.update(HEADERS)


def pedir(url, intentos=3):
    """GET con reintentos. Devuelve la respuesta o None si no se pudo."""
    for intento in range(1, intentos + 1):
        try:
            r = sesion.get(url, timeout=10)
            if r.status_code == 200:
                r.encoding = r.apparent_encoding
                return r
            if r.status_code == 429:                 # nos pidieron ir más despacio
                espera = 5 * intento
                print(f"      429 Too Many Requests → esperando {espera}s")
                time.sleep(espera)
                continue
            print(f"      {r.status_code} en {url} → no insistimos")
            return None
        except requests.RequestException as e:
            print(f"      intento {intento}/{intentos} falló ({type(e).__name__})")
            time.sleep(2 * intento)
    return None


# ============================================== 1) Recorrer páginas ========
print("=" * 70)
print("1) SEGUIR EL BOTÓN 'NEXT' HASTA EL LÍMITE QUE NOSOTROS PONEMOS")
print("=" * 70)

url = INICIO
pagina = 1
libros = []

while url and pagina <= MAX_PAGINAS:
    print(f"\n   Página {pagina}: {url}")
    r = pedir(url)
    if r is None:
        break

    soup = BeautifulSoup(r.text, "html.parser")
    tarjetas = soup.select("article.product_pod")
    print(f"      {len(tarjetas)} libros en esta página")

    for t in tarjetas:
        libros.append({
            "titulo": t.h3.a["title"],
            "precio_gbp": float(t.select_one("p.price_color").text.replace("£", "").strip()),
            "url": urljoin(url, t.h3.a["href"]),      # ← convierte la ruta relativa en absoluta
        })

    siguiente = soup.select_one("li.next a")
    url = urljoin(url, siguiente["href"]) if siguiente else None
    pagina += 1

    if url:
        print(f"      Siguiente: {url}")
        time.sleep(PAUSA)                             # ← la pausa NUNCA se negocia

print(f"\n   Total acumulado: {len(libros)} libros en {pagina - 1} páginas")
print("\n   ★ urljoin() es la pieza que casi todos olvidan: el href del HTML suele ser")
print("     relativo ('catalogue/page-2.html'). urljoin lo convierte en URL completa.")
print("   ★ Si quitas MAX_PAGINAS, este bucle recorre las 50 páginas del sitio.")
print("     En un sitio real, eso son 50 peticiones. Piensa antes de quitar el tope.")


# ============================================== 2) Entrar al detalle =======
print("\n" + "=" * 70)
print("2) DEL LISTADO AL DETALLE: DATOS QUE SOLO ESTÁN ADENTRO")
print("=" * 70)
print("   El listado no trae el UPC ni la descripción. Hay que entrar a cada ficha.")
print(f"   Lo haremos solo con los 3 primeros (nunca pruebes con los {len(libros)}).\n")

for libro in libros[:3]:
    r = pedir(libro["url"])
    if r is None:
        continue
    s = BeautifulSoup(r.text, "html.parser")

    ficha = {tr.th.text.strip(): tr.td.text.strip()
             for tr in s.select("table.table-striped tr")}
    libro["upc"] = ficha.get("UPC", "N/D")
    libro["disponibles"] = ficha.get("Availability", "N/D")

    desc = s.select_one("#product_description ~ p")
    libro["descripcion"] = desc.text.strip()[:80] + "..." if desc else "sin descripción"

    print(f"   {libro['titulo'][:40]:<40} UPC={libro['upc']}  {libro['disponibles']}")
    time.sleep(PAUSA)

print("\n   ★ Fíjate en el costo: 3 páginas de listado + 3 fichas = 6 peticiones.")
print("     Para las 1000 fichas del sitio serían 1050 peticiones y ~18 minutos")
print("     con pausa de 1 segundo. AHÍ es donde Scrapy (concurrencia) se justifica.")


# ============================================== 3) Guardar ================
print("\n" + "=" * 70)
print("3) GUARDAR EL RESULTADO")
print("=" * 70)

df = pd.DataFrame(libros)
salida = SALIDAS / "libros_paginado.csv"
df.to_csv(salida, index=False, encoding="utf-8-sig")

print(f"   {len(df)} filas → {salida.relative_to(BASE)}")
print(f"   Columnas: {list(df.columns)}")
print(f"\n   Precio promedio de las {pagina - 1} páginas: £{df['precio_gbp'].mean():.2f}")


# ============================================== 4) Checklist ==============
print("\n" + "=" * 70)
print("4) CHECKLIST DE UN SCRAPER QUE NO TE VA A DAR VERGÜENZA")
print("=" * 70)
print("""
   [ ] ¿Revisé si hay API antes de escribir esto?
   [ ] ¿Leí el robots.txt?
   [ ] ¿Puse User-Agent identificable?
   [ ] ¿Puse timeout en cada petición?
   [ ] ¿Puse time.sleep() entre peticiones?
   [ ] ¿Mi bucle tiene un tope (MAX_PAGINAS) o puede correr para siempre?
   [ ] ¿Manejo el 403, el 429 y la caída de red sin que el script explote?
   [ ] ¿Guardo el HTML crudo mientras desarrollo, para no repetir peticiones?
   [ ] ¿Documenté qué scrapeé, de dónde y cuándo?
""")

print("=" * 70)
print("SIGUIENTE → 15_reto_scraping.py (ahora te toca a ti)")
print("=" * 70)
