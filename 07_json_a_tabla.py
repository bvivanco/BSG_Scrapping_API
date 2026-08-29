"""
07 · De JSON anidado a tabla (CSV / Excel)
===========================================
Capítulo 2 · Sesión 2 · Bloque 3

El paso que casi siempre falta en los tutoriales: la API te da JSON anidado,
pero tu jefe quiere un Excel. Aquí se aplana.

    python 07_json_a_tabla.py
"""

import csv
import json
from pathlib import Path

import requests

BASE = Path(__file__).parent
SALIDAS = BASE / "salidas"
SALIDAS.mkdir(exist_ok=True)


# ============================================== 1) Traer los datos ==========
print("=" * 70)
print("1) TRAEMOS 30 PRODUCTOS DE LA API")
print("=" * 70)

r = requests.get("https://dummyjson.com/products", params={"limit": 30}, timeout=10)
r.raise_for_status()
data = r.json()
productos = data["products"]

print(f"Recibidos: {len(productos)} de {data['total']} productos")
print(f"Claves de cada producto: {list(productos[0].keys())}")


# ============================================== 2) Aplanar ==================
print("\n" + "=" * 70)
print("2) APLANAR — de JSON anidado a filas planas")
print("=" * 70)

filas = []
for p in productos:
    filas.append({
        "id": p["id"],
        "titulo": p["title"],
        # .get() porque no todos los productos traen marca
        "marca": p.get("brand", "Sin marca"),
        "categoria": p["category"],
        "precio_usd": p["price"],
        "descuento_pct": p.get("discountPercentage", 0),
        # Campo calculado: el precio final tras el descuento
        "precio_final": round(
            p["price"] * (1 - p.get("discountPercentage", 0) / 100), 2),
        "rating": p["rating"],
        "stock": p["stock"],
        # Una lista anidada convertida a texto separado por ";"
        "etiquetas": "; ".join(p.get("tags", [])),
        # Un valor de dos niveles abajo
        "envio": p.get("shippingInformation", ""),
        "n_resenas": len(p.get("reviews", [])),
    })

print(f"Filas generadas: {len(filas)}")
print(f"Columnas       : {list(filas[0].keys())}\n")

print(f"{'ID':<4} {'PRODUCTO':<34} {'CATEGORÍA':<18} {'PRECIO':>8} {'FINAL':>8}")
print("-" * 76)
for f in filas[:8]:
    print(f"{f['id']:<4} {f['titulo'][:33]:<34} {f['categoria'][:17]:<18} "
          f"{f['precio_usd']:>8.2f} {f['precio_final']:>8.2f}")
print(f"... y {len(filas) - 8} filas más")


# ============================================== 3) Guardar CSV ==============
print("\n" + "=" * 70)
print("3) GUARDAR COMO CSV (sin librerías extra)")
print("=" * 70)

ruta_csv = SALIDAS / "productos.csv"

# newline="" es obligatorio en Windows para que no salgan líneas en blanco.
# encoding="utf-8-sig" hace que Excel muestre bien las tildes.
with open(ruta_csv, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=list(filas[0].keys()))
    writer.writeheader()
    writer.writerows(filas)

print(f"Guardado: {ruta_csv}  ({ruta_csv.stat().st_size} bytes)")
print("\nDetalles que evitan dolores de cabeza:")
print("   newline=''            → sin filas vacías intercaladas en Windows")
print("   encoding='utf-8-sig'  → Excel muestra bien tildes y ñ")


# ============================================== 4) Guardar JSON =============
print("\n" + "=" * 70)
print("4) GUARDAR TAMBIÉN COMO JSON LIMPIO")
print("=" * 70)

ruta_json = SALIDAS / "productos.json"
with open(ruta_json, "w", encoding="utf-8") as f:
    json.dump(filas, f, indent=2, ensure_ascii=False)
print(f"Guardado: {ruta_json}  ({ruta_json.stat().st_size} bytes)")


# ============================================== 5) Con pandas ===============
print("\n" + "=" * 70)
print("5) LO MISMO CON PANDAS (mucho más corto)")
print("=" * 70)

try:
    import pandas as pd

    df = pd.DataFrame(filas)

    print(f"DataFrame: {df.shape[0]} filas × {df.shape[1]} columnas\n")
    print(df[["id", "titulo", "categoria", "precio_usd", "rating"]].head(8)
          .to_string(index=False))

    print("\n--- Análisis rápido: precio promedio por categoría ---")
    resumen = (df.groupby("categoria")
                 .agg(productos=("id", "count"),
                      precio_promedio=("precio_usd", "mean"),
                      rating_promedio=("rating", "mean"))
                 .round(2)
                 .sort_values("precio_promedio", ascending=False))
    print(resumen.to_string())

    print("\n--- Los 5 más caros ---")
    print(df.nlargest(5, "precio_usd")[["titulo", "marca", "precio_usd"]]
          .to_string(index=False))

    ruta_xlsx = SALIDAS / "productos.xlsx"
    try:
        df.to_excel(ruta_xlsx, index=False)
        print(f"\nExcel guardado: {ruta_xlsx}")
    except Exception:
        print("\n(Para exportar a Excel: pip install openpyxl)")

    # pandas también sabe aplanar solo, con json_normalize
    print("\n--- Bonus: pd.json_normalize aplana JSON anidado automáticamente ---")
    plano = pd.json_normalize(productos, sep="_")
    print(f"Columnas detectadas automáticamente: {len(plano.columns)}")
    print(f"Primeras 10: {list(plano.columns[:10])}")

except ImportError:
    print("pandas no está instalado. Instálalo con:  pip install pandas")
    print("(El CSV del paso 3 ya quedó generado igual.)")


print("""
=======================================================================
EL FLUJO COMPLETO
=======================================================================
  API  →  requests.get()  →  .json()  →  aplanar  →  CSV / Excel / BD
                                             ↑
                              aquí decides qué columnas necesitas
                              y creas los campos calculados
""")
