"""
10 · Tu primer scraping: pedir el HTML
=======================================
Capítulo 3 · Sesión 1 · Bloque 1

Un scraper empieza EXACTAMENTE igual que una API: con requests.get().
La diferencia es lo que llega: en vez de JSON ordenado, llega HTML crudo.

    python 10_scraping_primer_html.py
"""

import time
from pathlib import Path
from urllib.robotparser import RobotFileParser

import requests

DATA = Path(__file__).parent / "data"
DATA.mkdir(exist_ok=True)

URL = "https://books.toscrape.com/"

# Identificarnos es la primera regla de cortesía del scraping.
HEADERS = {
    "User-Agent": "BSG-Curso-Scraping/1.0 (ejercicio academico; contacto@ejemplo.com)"
}


# ============================================== 1) Es la MISMA petición =====
print("=" * 70)
print("1) PEDIR UNA PÁGINA ES LA MISMA PETICIÓN HTTP DEL CAPÍTULO 1")
print("=" * 70)

r = requests.get(URL, headers=HEADERS, timeout=10)

print(f"   URL          : {URL}")
print(f"   status_code  : {r.status_code}  ← si no es 200, ni intentes leer el contenido")
print(f"   Content-Type : {r.headers.get('Content-Type')}")
print(f"   Tamaño       : {len(r.text):,} caracteres")
print("\n   Con una API esperábamos application/json.")
print("   Aquí dice text/html: nos mandaron una PÁGINA, no datos.")


# ============================================== 2) La respuesta es texto ====
print("\n" + "=" * 70)
print("2) LO QUE LLEGA ES TEXTO: LETRAS Y ETIQUETAS")
print("=" * 70)

print("   Primeros 400 caracteres de r.text:\n")
for linea in r.text[:400].splitlines():
    print("   |", linea)

print("\n   Eso es HTML: la misma página bonita que ves en Chrome.")
print("   NO se puede usar r.json(): esto no es JSON. Descomenta para ver el error:")
print("   # r.json()  →  JSONDecodeError")


# ============================================== 3) El encoding =============
print("\n" + "=" * 70)
print("3) TRAMPA CLÁSICA: EL ENCODING (las tildes y símbolos rotos)")
print("=" * 70)

precio_crudo = r.text.split('price_color">')[1].split("<")[0]
print(f"   requests dice que la página es : {r.encoding}")
print(f"   pero mirando el contenido es   : {r.apparent_encoding}")
print(f"   Resultado si no lo corriges    : {precio_crudo!r}   ← 'Â£' en vez de '£'")

r.encoding = r.apparent_encoding          # ← la corrección, una sola línea
precio_ok = r.text.split('price_color">')[1].split("<")[0]
print(f"   Después de r.encoding = r.apparent_encoding: {precio_ok!r}")
print("\n   ★ Si ves 'Ã©', 'Â£' o 'PerÃº', el problema es el encoding, no tu código.")


# ============================================== 4) Identificarse ===========
print("\n" + "=" * 70)
print("4) IDENTIFICARSE: EL USER-AGENT")
print("=" * 70)

sin_ua = requests.get("https://httpbin.org/user-agent", timeout=10).json()
con_ua = requests.get("https://httpbin.org/user-agent", headers=HEADERS, timeout=10).json()

print(f"   Sin headers, el servidor ve : {sin_ua['user-agent']}")
print(f"   Con nuestros headers, ve    : {con_ua['user-agent']}")
print("\n   ★ 'python-requests/2.x' es una bandera roja para cualquier sitio.")
print("     Poner un User-Agent propio no es disfrazarse: es presentarse.")


# ============================================== 5) robots.txt ==============
print("\n" + "=" * 70)
print("5) robots.txt: EL CARTEL DE LA ENTRADA")
print("=" * 70)

def reglas_para_todos(texto):
    """Devuelve las reglas Disallow del bloque 'User-agent: *'.

    Un robots.txt tiene bloques por robot. Las reglas que nos aplican a nosotros
    son las del bloque '*'; las de otros bloques son para Google, Bing, etc.
    """
    reglas, dentro = [], False
    for linea in texto.splitlines():
        limpia = linea.split("#")[0].strip()
        if limpia.lower().startswith("user-agent:"):
            dentro = limpia.split(":", 1)[1].strip() == "*"
        elif dentro and limpia.lower().startswith("disallow:"):
            reglas.append(limpia)
    return reglas


for sitio in ["https://www.gob.pe", "https://www.python.org"]:
    try:
        rb = requests.get(f"{sitio}/robots.txt", headers=HEADERS, timeout=10)
        reglas = reglas_para_todos(rb.text)
        print(f"\n   {sitio}/robots.txt  → {rb.status_code}")
        print(f"      Bloque 'User-agent: *' → {len(reglas)} reglas Disallow:")
        for regla in reglas[:4]:
            print(f"         {regla}")
        if len(reglas) > 4:
            print(f"         ... y {len(reglas) - 4} más")
    except requests.RequestException as e:
        print(f"   {sitio}: no se pudo leer ({type(e).__name__})")

print("\n   ★ Cuidado al leerlo: un robots.txt tiene BLOQUES por robot.")
print("     Un 'Disallow: /' puede estar dirigido a un bot específico, no a ti.")
print("     Lo que te aplica es el bloque 'User-agent: *'.")

print("\n   Python trae un lector de robots.txt en la librería estándar:")
rp = RobotFileParser()
rp.set_url("https://www.python.org/robots.txt")
try:
    rp.read()
    print(f"      ¿Puedo entrar a python.org/downloads/ ?  {rp.can_fetch('*', 'https://www.python.org/downloads/')}")
    print(f"      ¿Puedo entrar a python.org/search/ ?     {rp.can_fetch('*', 'https://www.python.org/search/')}")
except Exception:
    print("      (no se pudo descargar el robots.txt en este momento)")

print("\n   ★ robots.txt NO es un candado: es un cartel. Nada te impide ignorarlo,")
print("     pero ignorarlo prueba que sabías que no debías entrar.")


# ============================================== 6) El 403 ==================
print("\n" + "=" * 70)
print("6) EL 403: CUANDO TE DICEN QUE NO")
print("=" * 70)

bloqueado = requests.get("https://httpbin.org/status/403", timeout=10)
print(f"   status_code : {bloqueado.status_code}")
print(f"   r.ok        : {bloqueado.ok}")
print("\n   El servidor ENTENDIÓ la petición y se negó. No es un error de sintaxis.")
print("   Qué hacer, en orden:")
print("      1. Revisar robots.txt (quizá esa ruta está prohibida)")
print("      2. Identificarte con un User-Agent honesto")
print("      3. Bajar la frecuencia: time.sleep() entre peticiones")
print("      4. Buscar si hay API oficial o descarga en CSV")
print("      5. Escribir y pedir permiso")
print("   ✗ Lo que NO hacemos: rotar IPs, resolver CAPTCHAs, falsear identidad.")


# ============================================== 7) Guardar el HTML =========
print("\n" + "=" * 70)
print("7) BUENA PRÁCTICA: DESCARGA UNA VEZ, PRUEBA MIL")
print("=" * 70)

destino = DATA / "books_home.html"
destino.write_text(r.text, encoding="utf-8")

print(f"   HTML guardado en: {destino.relative_to(Path(__file__).parent)}")
print(f"   Tamaño: {destino.stat().st_size:,} bytes")
print("\n   Mientras armas tus selectores NO necesitas volver a pedir la página 20 veces.")
print("   Descargas una vez, trabajas contra el archivo local y el servidor ni se entera.")
print("   El siguiente script (11) usa justamente este archivo.")

time.sleep(0.2)
print("\n" + "=" * 70)
print("LISTO. Ya tienes el HTML. Falta leerlo → 11_html_estructura.py")
print("=" * 70)
