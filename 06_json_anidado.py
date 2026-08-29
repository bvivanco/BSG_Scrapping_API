"""
06 · Estructuras anidadas de JSON
==================================
Capítulo 2 · Sesión 2 · Bloque 1

LA REGLA DE ORO:
    corchetes con TEXTO   →  entras a un diccionario (buscas una CLAVE)
    corchetes con NÚMERO  →  entras a una lista      (buscas una POSICIÓN, desde 0)

¿Perdido? Imprime type() y keys() antes de seguir bajando.

    python 06_json_anidado.py
"""

import json
from pathlib import Path

import requests

DATA = Path(__file__).parent / "data"


# ============================================== 1) JSON local anidado ========
print("=" * 70)
print("1) UN JSON ANIDADO DE VERDAD (data/pedido.json)")
print("=" * 70)

with open(DATA / "pedido.json", encoding="utf-8") as f:
    pedido = json.load(f)

print("Estructura de primer nivel:")
for clave, valor in pedido.items():
    tipo = type(valor).__name__
    extra = f" ({len(valor)} elementos)" if isinstance(valor, (list, dict)) else ""
    print(f"   {clave:<12} → {tipo}{extra}")


# ============================================== 2) Navegar paso a paso ======
print("\n" + "=" * 70)
print("2) NAVEGAR PASO A PASO — como una dirección postal")
print("=" * 70)

print("pedido                            → dict")
print("pedido['cliente']                 → dict  (objeto dentro de objeto)")
print("pedido['cliente']['documento']    → dict  (otro nivel más)")
print("pedido['cliente']['documento']['numero'] → str  ← ¡el dato!\n")

print(f"   Nombre     : {pedido['cliente']['nombre']}")
print(f"   Documento  : {pedido['cliente']['documento']['tipo']} "
      f"{pedido['cliente']['documento']['numero']}")
print(f"   Distrito   : {pedido['cliente']['direccion']['distrito']}")
print(f"   País       : {pedido['cliente']['direccion']['pais']}")


# ============================================== 3) Listas de objetos ========
print("\n" + "=" * 70)
print("3) LISTAS DE OBJETOS — primero la POSICIÓN, luego la clave")
print("=" * 70)

print(f"pedido['items']        → {type(pedido['items']).__name__} "
      f"con {len(pedido['items'])} elementos")
print(f"pedido['items'][0]     → {type(pedido['items'][0]).__name__} (el primer producto)")
print(f"pedido['items'][0]['producto'] → '{pedido['items'][0]['producto']}'\n")

print("Recorriendo la lista completa:")
print(f"   {'#':<3} {'PRODUCTO':<32} {'CANT':>5} {'P.UNIT':>10} {'SUBTOTAL':>10}")
print("   " + "-" * 63)

total = 0.0
for i, item in enumerate(pedido["items"], 1):
    subtotal = item["cantidad"] * item["precio_unitario"]
    total += subtotal
    print(f"   {i:<3} {item['producto']:<32} {item['cantidad']:>5} "
          f"{item['precio_unitario']:>10.2f} {subtotal:>10.2f}")

envio = pedido["envio"]["costo"]
print("   " + "-" * 63)
print(f"   {'Subtotal':<42} {total:>20.2f}")
print(f"   {'Envío (' + pedido['envio']['courier'] + ')':<42} {envio:>20.2f}")
print(f"   {'TOTAL':<42} {total + envio:>20.2f}")


# ============================================== 4) Anidamiento profundo =====
print("\n" + "=" * 70)
print("4) NIVELES PROFUNDOS: dict → list → dict → list")
print("=" * 70)

ruta = pedido["items"][2]["categorias"][1]
print("pedido['items'][2]['categorias'][1]")
print("   ↓ dict   ↓ list ↓ dict         ↓ list")
print(f"   resultado: '{ruta}'")
print("\nLéelo de izquierda a derecha y deja de dar miedo.")


# ============================================== 5) Acceso seguro ============
print("\n" + "=" * 70)
print("5) ACCESO SEGURO: .get() evita que tu script se caiga")
print("=" * 70)

# Con corchetes: si la clave no existe → KeyError y el script muere
try:
    pedido["descuento"]
except KeyError as e:
    print(f"   pedido['descuento']              → KeyError: {e}")

# Con .get(): devuelve None, o el valor por defecto que tú indiques
print(f"   pedido.get('descuento')          → {pedido.get('descuento')}")
print(f"   pedido.get('descuento', 0)       → {pedido.get('descuento', 0)}")

# Encadenado seguro para varios niveles
tracking = pedido.get("envio", {}).get("tracking", "sin tracking")
inexistente = pedido.get("factura", {}).get("serie", "sin factura")
print(f"\n   Encadenado seguro:")
print(f"   pedido.get('envio', {{}}).get('tracking')   → {tracking}")
print(f"   pedido.get('factura', {{}}).get('serie')    → {inexistente}")

print("""
   En APIs reales los campos opcionales faltan a cada rato. .get() evita
   que tu script se caiga en el registro 347 de 1000.
""")


# ============================================== 6) API real =================
print("=" * 70)
print("6) LO MISMO, PERO CON UNA API REAL")
print("=" * 70)

r = requests.get("https://dummyjson.com/products", params={"limit": 3}, timeout=10)
r.raise_for_status()
data = r.json()

# PASO CLAVE: explorar antes de asumir
print(f"   type(data)   → {type(data).__name__}")
print(f"   data.keys()  → {list(data.keys())}")
print(f"   len(data['products']) → {len(data['products'])}\n")

for p in data["products"]:
    print(f"   {p['id']:>3}. {p['title']:<38} $ {p['price']:<8} "
          f"[{p.get('brand', 'sin marca')}]")

# Bajando varios niveles en datos reales
primero = data["products"][0]
if primero.get("reviews"):
    review = primero["reviews"][0]
    print(f"\n   Primera reseña de '{primero['title']}':")
    print(f'      "{review["comment"]}"  — {review["reviewerName"]} '
          f'({review["rating"]}/5)')
    print("\n   Ruta usada: data['products'][0]['reviews'][0]['comment']")
    print("               dict     list  dict     list  dict")


# ============================================== 7) Explorador genérico ======
print("\n" + "=" * 70)
print("7) BONUS: función para explorar cualquier JSON desconocido")
print("=" * 70)


def explorar(obj, prefijo="", nivel=0, max_nivel=3):
    """Imprime el 'mapa' de un JSON: qué claves hay y de qué tipo son."""
    sangria = "   " * nivel
    if isinstance(obj, dict):
        for clave, valor in obj.items():
            tipo = type(valor).__name__
            if isinstance(valor, dict):
                print(f"{sangria}{prefijo}{clave}/  (dict, {len(valor)} claves)")
                if nivel < max_nivel:
                    explorar(valor, "", nivel + 1, max_nivel)
            elif isinstance(valor, list):
                print(f"{sangria}{prefijo}{clave}[]  (list, {len(valor)} elementos)")
                if valor and nivel < max_nivel:
                    explorar(valor[0], "[0].", nivel + 1, max_nivel)
            else:
                muestra = str(valor)[:40]
                print(f"{sangria}{prefijo}{clave}: {tipo} = {muestra}")
    else:
        print(f"{sangria}{prefijo}{type(obj).__name__} = {str(obj)[:40]}")


print("Mapa de data/pedido.json:\n")
explorar(pedido)

print("""
=======================================================================
PARA RECORDAR
=======================================================================
  ['texto']  → clave de diccionario
  [0]        → posición en lista (empieza en 0)
  .get(k, d) → acceso seguro con valor por defecto
  type() y .keys() → tus linternas cuando no sabes qué llegó
""")
