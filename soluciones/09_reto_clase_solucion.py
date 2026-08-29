"""
09 · SOLUCIÓN del reto de la sesión
====================================
Comentada paso a paso. Intenta primero con 09_reto_clase.py.

    python soluciones/09_reto_clase_solucion.py
"""

import json
from pathlib import Path

import requests

# El archivo vive en soluciones/, así que subimos un nivel para llegar a salidas/
SALIDAS = Path(__file__).resolve().parent.parent / "salidas"
SALIDAS.mkdir(exist_ok=True)


# =========================================================== RETO 1 =========
print("=" * 70)
print("RETO 1 — Tipo de cambio USD → PEN")
print("=" * 70)

# 1.1 Petición
r = requests.get("https://open.er-api.com/v6/latest/USD", timeout=10)

# 1.2 Verificar ANTES de leer los datos
r.raise_for_status()

# 1.3 Convertir a diccionario de Python
datos = r.json()

# Cuando no conoces la estructura, explórala primero:
print(f"   type(datos)  → {type(datos).__name__}")
print(f"   datos.keys() → {list(datos.keys())}")

# 1.4 El dato está anidado: datos → "rates" (dict) → "PEN"
pen = datos["rates"]["PEN"]
print(f"\n   1 USD = {pen} PEN")
print(f"   Actualizado: {datos['time_last_update_utc']}")

# 1.5 Extra
monto = 500
print(f"   {monto} USD = S/ {monto * pen:,.2f}")


# =========================================================== RETO 2 =========
print("\n" + "=" * 70)
print("RETO 2 — Temperatura actual")
print("=" * 70)


def temperatura_actual(nombre, lat, lon):
    """Devuelve (temperatura, hora) de la ciudad indicada."""
    r = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={                       # params, NUNCA concatenando strings
            "latitude": lat,
            "longitude": lon,
            "current": "temperature_2m",
            "timezone": "America/Lima",
        },
        timeout=10,
    )
    r.raise_for_status()
    datos = r.json()
    actual = datos["current"]          # ← el objeto anidado
    return actual["temperature_2m"], actual["time"]


temp_lima, hora = temperatura_actual("Lima", -12.0464, -77.0428)
print(f"   Lima     : {temp_lima}°C   (medición: {hora})")

# 2.3 Extra — comparación
temp_aqp, _ = temperatura_actual("Arequipa", -16.4090, -71.5375)
print(f"   Arequipa : {temp_aqp}°C")

mas_fria = "Lima" if temp_lima < temp_aqp else "Arequipa"
print(f"\n   Está más fría: {mas_fria} "
      f"(diferencia de {abs(temp_lima - temp_aqp):.1f}°C)")


# =========================================================== RETO 3 =========
print("\n" + "=" * 70)
print("RETO 3 — Del catálogo a un archivo JSON")
print("=" * 70)

# 3.1 Traer los productos. params={"limit": 10} en vez de "?limit=10"
r = requests.get("https://dummyjson.com/products",
                 params={"limit": 10}, timeout=10)
r.raise_for_status()
data = r.json()

print(f"   Recibidos {len(data['products'])} de {data['total']} productos")

# 3.2 Aplanar: nos quedamos solo con dos campos de cada producto.
#     Versión con for clásico (la más legible al aprender):
catalogo = []
for p in data["products"]:
    catalogo.append({"titulo": p["title"], "precio": p["price"]})

#     Versión equivalente con lista por comprensión (más pythónica):
# catalogo = [{"titulo": p["title"], "precio": p["price"]}
#             for p in data["products"]]

print("\n   Catálogo generado:")
for item in catalogo:
    print(f"      {item['titulo']:<40} $ {item['precio']}")

# 3.3 Guardar en disco
ruta = SALIDAS / "productos_reto.json"
with open(ruta, "w", encoding="utf-8") as f:      # encoding para las tildes
    json.dump(catalogo, f, indent=2, ensure_ascii=False)

print(f"\n   Guardado en: {ruta}  ({ruta.stat().st_size} bytes)")

# 3.4 Extra — precio promedio
precios = [item["precio"] for item in catalogo]
print(f"   Precio promedio: $ {sum(precios) / len(precios):.2f}")
print(f"   Más caro       : $ {max(precios)}")
print(f"   Más barato     : $ {min(precios)}")

# Comprobamos que se puede volver a leer (ida y vuelta completa)
with open(ruta, encoding="utf-8") as f:
    recuperado = json.load(f)
print(f"   Releído del archivo: {len(recuperado)} items "
      f"— ¿idéntico? {recuperado == catalogo}")


# =========================================================== BONUS ==========
print("\n" + "=" * 70)
print("BONUS — Crear un producto con POST")
print("=" * 70)

nuevo = {"title": "Curso BSG", "price": 99}

# json={...} serializa el dict y pone el Content-Type automáticamente
r = requests.post("https://dummyjson.com/products/add", json=nuevo, timeout=10)

print(f"   Status code : {r.status_code}")
print(f"   ¿OK?        : {r.ok}")

creado = r.json()
print(f"   id asignado : {creado['id']}")
print(f"   Respuesta   : {json.dumps(creado, ensure_ascii=False)}")

print("""
   Nota: DummyJSON simula la creación. Si haces un GET a ese id nuevo,
   no existe. En una API real sí quedaría guardado.
""")


print("""
=======================================================================
LO QUE PRACTICASTE
=======================================================================
  1. requests.get() con params           → petición bien armada
  2. raise_for_status()                  → verificar antes de leer
  3. r.json()                            → de texto JSON a dict/list
  4. datos["a"]["b"] y datos["l"][0]     → navegar estructuras anidadas
  5. json.dump(..., ensure_ascii=False)  → guardar sin romper tildes
  6. requests.post(url, json={...})      → enviar datos al servidor
""")
