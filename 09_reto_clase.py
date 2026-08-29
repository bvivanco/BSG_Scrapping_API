"""
09 · RETO DE LA SESIÓN
=======================
Capítulo 2 · Sesión 2 · Bloque 3

Completa los TODO. Ninguna de las APIs pide clave.
Si te trabas más de 5 minutos, mira soluciones/09_reto_clase_solucion.py

    python 09_reto_clase.py
"""

import json
from pathlib import Path

import requests

SALIDAS = Path(__file__).parent / "salidas"
SALIDAS.mkdir(exist_ok=True)


# =========================================================== RETO 1 =========
# Tipo de cambio: ¿cuántos soles vale hoy 1 dólar?
#
#   URL: https://open.er-api.com/v6/latest/USD
#   La respuesta trae un objeto "rates" y dentro la clave "PEN".
# ===========================================================================
print("=" * 70)
print("RETO 1 — Tipo de cambio USD → PEN")
print("=" * 70)

# TODO 1.1: haz el GET a la URL (recuerda timeout=10)
# r = ...

# TODO 1.2: verifica que salió bien (raise_for_status o r.ok)

# TODO 1.3: convierte la respuesta a diccionario
# datos = ...

# TODO 1.4: extrae el valor de PEN e imprímelo
# pen = ...
# print(f"1 USD = {pen} PEN")

# TODO 1.5 (extra): ¿cuánto son 500 dólares en soles?


# =========================================================== RETO 2 =========
# Clima: ¿qué temperatura hace ahora mismo en Lima?
#
#   URL : https://api.open-meteo.com/v1/forecast
#   params: latitude=-12.0464, longitude=-77.0428,
#           current="temperature_2m", timezone="America/Lima"
#   La temperatura está anidada en  datos["current"]["temperature_2m"]
# ===========================================================================
print("\n" + "=" * 70)
print("RETO 2 — Temperatura actual en Lima")
print("=" * 70)

# TODO 2.1: arma el GET usando params={...} (NO pegues los parámetros a la URL)

# TODO 2.2: extrae la temperatura y la hora de la medición

# TODO 2.3 (extra): repite para Arequipa (-16.4090, -71.5375) y di cuál
#                   de las dos ciudades está más fría


# =========================================================== RETO 3 =========
# Catálogo: guarda un JSON con el título y precio de 10 productos.
#
#   URL: https://dummyjson.com/products?limit=10
#   Estructura: {"products": [ {...}, {...} ], "total": ...}
#   Resultado esperado: salidas/productos_reto.json con una lista así:
#       [{"titulo": "...", "precio": 9.99}, ...]
# ===========================================================================
print("\n" + "=" * 70)
print("RETO 3 — Del catálogo a un archivo JSON")
print("=" * 70)

# TODO 3.1: trae los 10 productos

# TODO 3.2: recorre data["products"] y arma una lista de diccionarios
#           con solo dos claves: "titulo" y "precio"
# catalogo = []

# TODO 3.3: guarda esa lista en salidas/productos_reto.json
#           usando json.dump(..., indent=2, ensure_ascii=False)

# TODO 3.4 (extra): calcula e imprime el precio promedio


# =========================================================== BONUS ==========
# Haz un POST a https://dummyjson.com/products/add con el body
#     {"title": "Curso BSG", "price": 99}
# ¿Qué status code devuelve? ¿Qué id le asignó la API?
# ===========================================================================
print("\n" + "=" * 70)
print("BONUS — Crear un producto con POST")
print("=" * 70)

# TODO B.1: haz el POST con json={...}

# TODO B.2: imprime el status_code y el id que devolvió


print("""
=======================================================================
PISTAS
=======================================================================
  · r.json() convierte la respuesta a dict o list. `r` a secas NO sirve.
  · Corchetes con texto = clave.  Corchetes con número = posición.
  · Si no sabes qué llegó:  print(type(datos));  print(datos.keys())
  · Para guardar con tildes correctas:
        json.dump(obj, f, indent=2, ensure_ascii=False)
    y abre el archivo con  open(ruta, "w", encoding="utf-8")
""")
