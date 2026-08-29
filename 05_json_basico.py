"""
05 · Fundamentos de JSON en Python
===================================
Capítulo 2 · Sesión 1 · Bloques 2 y 3

Las 4 funciones del módulo json, y el truco para no confundirlas:

    CON la "s" final  →  trabaja con Strings
        json.dumps(obj)     Python  → texto JSON     (serializar)
        json.loads(texto)   texto JSON → Python      (deserializar)

    SIN la "s" final  →  trabaja con Files (archivos)
        json.dump(obj, f)   Python  → archivo
        json.load(f)        archivo → Python

    python 05_json_basico.py
"""

import json
from pathlib import Path

SALIDAS = Path(__file__).parent / "salidas"
SALIDAS.mkdir(exist_ok=True)


# ============================================== 1) Diccionario de Python =====
print("=" * 70)
print("1) PARTIMOS DE UN DICCIONARIO DE PYTHON")
print("=" * 70)

usuario = {
    "nombre": "Ana Torres",
    "edad": 30,
    "correo": "ana@example.com",
    "activo": True,          # booleano de Python: mayúscula
    "saldo": 1250.75,        # float
    "cupon": None,           # None de Python
    "roles": ["admin", "editor"],
    "perfil": {"pais": "Perú", "idioma": "es"},
}

print(f"Tipo: {type(usuario)}")
for clave, valor in usuario.items():
    print(f"   {clave:<10}: {str(valor):<30} ({type(valor).__name__})")


# ============================================== 2) dumps: Python → JSON ======
print("\n" + "=" * 70)
print("2) json.dumps() — SERIALIZAR: de Python a texto JSON")
print("=" * 70)

texto_json = json.dumps(usuario)
print(f"Tipo resultante: {type(texto_json)}   ← ¡ahora es un STRING!\n")
print(texto_json)

print("\n--- El mismo dato, pero legible (indent + tildes) ---")
bonito = json.dumps(usuario, indent=2, ensure_ascii=False)
print(bonito)

print("\n--- ¿Qué pasa SIN ensure_ascii=False? ---")
print(json.dumps({"pais": "Perú", "ciudad": "Cañete"}))
print("   ↑ las tildes y la ñ se escapan. Casi nunca es lo que quieres.")

print("\n--- Traducción automática de tipos ---")
print("   Python True  → JSON true")
print("   Python None  → JSON null")
print("   Python dict  → JSON object { }")
print("   Python list  → JSON array  [ ]")


# ============================================== 3) loads: JSON → Python ======
print("\n" + "=" * 70)
print("3) json.loads() — DESERIALIZAR: de texto JSON a Python")
print("=" * 70)

recibido = '''
{
  "producto": "Laptop",
  "precio": 3200.50,
  "disponible": true,
  "descuento": null,
  "etiquetas": ["oferta", "nuevo"]
}
'''

datos = json.loads(recibido)
print(f"Tipo resultante: {type(datos)}   ← de vuelta a diccionario\n")
for clave, valor in datos.items():
    print(f"   {clave:<12}: {str(valor):<25} ({type(valor).__name__})")

print("\n   Fíjate: JSON true → Python True,  JSON null → Python None")


# ============================================== 4) Errores típicos ===========
print("\n" + "=" * 70)
print("4) LOS 4 ERRORES DE SINTAXIS MÁS COMUNES")
print("=" * 70)

malos = [
    ("{'nombre': 'Ana'}",                "comillas SIMPLES — JSON solo acepta dobles"),
    ('{"activo": True}',                 "True en mayúscula — en JSON va 'true'"),
    ('{"lista": [1, 2, 3,]}',            "coma final (trailing comma) — prohibida"),
    ('{"a": 1} // comentario',           "comentarios — JSON no los admite"),
]

for texto_malo, motivo in malos:
    try:
        json.loads(texto_malo)
        print(f"   OK inesperado: {texto_malo}")
    except json.JSONDecodeError as e:
        print(f"   ERROR  {texto_malo:<30} → {motivo}")
        print(f"          ({e.msg}, columna {e.colno})")


# ============================================== 5) dump: guardar archivo =====
print("\n" + "=" * 70)
print("5) json.dump() — GUARDAR EN UN ARCHIVO (sin la 's')")
print("=" * 70)

ruta = SALIDAS / "usuario.json"

with open(ruta, "w", encoding="utf-8") as f:
    json.dump(usuario, f, indent=2, ensure_ascii=False)

print(f"Guardado en: {ruta}")
print(f"Tamaño     : {ruta.stat().st_size} bytes")
print("\nOJO con encoding='utf-8': sin él, en Windows las tildes se rompen.")


# ============================================== 6) load: leer archivo ========
print("\n" + "=" * 70)
print("6) json.load() — LEER DESDE UN ARCHIVO (sin la 's')")
print("=" * 70)

with open(ruta, encoding="utf-8") as f:
    recuperado = json.load(f)

print(f"Tipo: {type(recuperado)}")
print(f"Nombre recuperado: {recuperado['nombre']}")
print(f"País (anidado)   : {recuperado['perfil']['pais']}")
print(f"¿Es idéntico al original? {recuperado == usuario}")


# ============================================== 7) Modificar y reescribir ====
print("\n" + "=" * 70)
print("7) OPERACIONES BÁSICAS: acceder, modificar, agregar, iterar")
print("=" * 70)

# Acceder
print(f"Acceder    : usuario['nombre']          → {usuario['nombre']}")
print(f"Anidado    : usuario['perfil']['pais']  → {usuario['perfil']['pais']}")
print(f"De lista   : usuario['roles'][0]        → {usuario['roles'][0]}")

# Acceso seguro
print(f"Seguro     : usuario.get('telefono', 'N/D')  → {usuario.get('telefono', 'N/D')}")

# Modificar
usuario["edad"] = 31
print(f"Modificar  : usuario['edad'] = 31       → {usuario['edad']}")

# Agregar
usuario["telefono"] = "+51 999 888 777"
print(f"Agregar    : nueva clave 'telefono'     → {usuario['telefono']}")

# Agregar a una lista
usuario["roles"].append("lector")
print(f"A la lista : roles                      → {usuario['roles']}")

# Eliminar
del usuario["cupon"]
print(f"Eliminar   : del usuario['cupon']       → claves: {list(usuario.keys())}")

# Iterar
print("\nIterar sobre las claves:")
for clave, valor in usuario.items():
    if not isinstance(valor, (dict, list)):
        print(f"   {clave:<10} = {valor}")

# Guardar los cambios
with open(SALIDAS / "usuario_modificado.json", "w", encoding="utf-8") as f:
    json.dump(usuario, f, indent=2, ensure_ascii=False)
print(f"\nCambios guardados en: {SALIDAS / 'usuario_modificado.json'}")


print("""
=======================================================================
CHULETA
=======================================================================
  json.dumps(obj, indent=2, ensure_ascii=False)   Python  → texto
  json.loads(texto)                                texto  → Python
  json.dump(obj, archivo, indent=2, ...)           Python  → archivo
  json.load(archivo)                               archivo → Python

  respuesta.json()   ← atajo de requests: hace el loads por ti

  Tip de terminal:  python -m json.tool archivo.json
""")
