"""
00 · Verifica tu entorno
=========================
Ejecuta esto ANTES de la clase. Comprueba que tienes todo lo necesario
para los 4 capítulos: APIs, JSON y Web Scraping.

    python 00_verifica_entorno.py

Si algo sale ERROR, la solución casi siempre es:
    pip install -r requirements.txt
"""

import sys

print("=" * 70)
print("VERIFICACIÓN DEL ENTORNO — Curso APIs y Web Scraping")
print("=" * 70)

ok = True

# 1) Versión de Python -------------------------------------------------------
v = sys.version_info
print(f"\n1. Python {v.major}.{v.minor}.{v.micro}")
if (v.major, v.minor) >= (3, 9):
    print("   OK — versión suficiente (se requiere 3.9 o superior)")
else:
    print("   ERROR — necesitas Python 3.9 o superior")
    ok = False

# 2) Librería requests -------------------------------------------------------
print("\n2. Librería requests")
try:
    import requests

    print(f"   OK — requests {requests.__version__} instalado")
except ImportError:
    print("   ERROR — no está instalada. Ejecuta: pip install -r requirements.txt")
    ok = False
    requests = None

# 3) Conexión a las APIs de la clase ----------------------------------------
print("\n3. Conexión a las APIs que usaremos")
if requests:
    apis = {
        "DummyJSON": "https://dummyjson.com/products/1",
        "JSONPlaceholder": "https://jsonplaceholder.typicode.com/users/1",
        "Tipo de cambio": "https://open.er-api.com/v6/latest/USD",
        "Open-Meteo (clima)": "https://api.open-meteo.com/v1/forecast"
                              "?latitude=-12.05&longitude=-77.04&current=temperature_2m",
    }
    for nombre, url in apis.items():
        try:
            r = requests.get(url, timeout=10)
            estado = "OK" if r.ok else f"responde {r.status_code}"
            print(f"   {estado:<14} {nombre}  ({r.elapsed.total_seconds():.2f} s)")
            if not r.ok:
                ok = False
        except Exception as e:
            print(f"   ERROR         {nombre}  →  {type(e).__name__}")
            ok = False

# 4) Librerías de Web Scraping (capítulos 3 y 4) -----------------------------
print("\n4. Librerías de Web Scraping")
for modulo, paquete in [("bs4", "beautifulsoup4"), ("lxml", "lxml"), ("pandas", "pandas")]:
    try:
        m = __import__(modulo)
        version = getattr(m, "__version__", "instalado")
        print(f"   OK — {paquete} {version}")
    except ImportError:
        print(f"   ERROR — falta {paquete}.  Ejecuta:  pip install {paquete}")
        ok = False

# 5) Conexión a los sitios de práctica ---------------------------------------
print("\n5. Conexión a los sitios de práctica de scraping")
if requests:
    sitios = {
        "books.toscrape": "https://books.toscrape.com/",
        "quotes.toscrape": "https://quotes.toscrape.com/",
        "httpbin": "https://httpbin.org/user-agent",
    }
    for nombre, url in sitios.items():
        try:
            r = requests.get(url, timeout=10,
                             headers={"User-Agent": "BSG-Curso-Scraping/1.0"})
            estado = "OK" if r.ok else f"responde {r.status_code}"
            print(f"   {estado:<14} {nombre}  ({r.elapsed.total_seconds():.2f} s)")
            if not r.ok:
                ok = False
        except Exception as e:
            print(f"   ERROR         {nombre}  →  {type(e).__name__}")
            ok = False

print("\n" + "=" * 70)
print("TODO LISTO — puedes seguir la clase" if ok else
      "HAY PROBLEMAS — revisa los ERROR de arriba antes de empezar")
print("=" * 70)
