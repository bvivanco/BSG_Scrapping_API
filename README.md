# Curso APIs y Web Scraping con Python — Ejemplos de clase

Código de apoyo para los **Capítulos 2, 3 y 4**: JSON, Web Scraping y técnicas avanzadas.

> Los ejemplos del **Capítulo 1** (métodos HTTP, anatomía de la petición, códigos de estado,
> Postman) se dictaron en la sesión anterior y están archivados fuera de esta carpeta.

Todos los ejemplos usan **APIs públicas que NO requieren clave**, así que funcionan
apenas los clonas. Solo necesitas Python 3.9+ e internet.

---

## Opción sin instalar nada: Google Colab

Los notebooks de `notebooks/` corren en **Google Colab** sin instalar ni configurar nada:
Colab ya trae `requests`, `beautifulsoup4`, `lxml` y `pandas`. Solo hace falta una cuenta
de Google.

| Notebook | Contenido |
|---|---|
| `demo_clase.ipynb` | Capítulos 1 y 2 — APIs y JSON (para el repaso) |
| `scraping_caps_3_y_4_colab.ipynb` | Capítulos 3 y 4 — scraping, XPath, limpieza, paginación |
| `reto_scraping_colab.ipynb` | El reto, con la solución al final |

**Ábrelos en Colab con un clic** (no hace falta descargar nada):

| Notebook | Enlace directo a Colab |
|---|---|
| Capítulos 1 y 2 (repaso) | [▶ Abrir en Colab](https://colab.research.google.com/github/bvivanco/BSG_Scrapping_API/blob/main/notebooks/demo_clase.ipynb) |
| Capítulos 3 y 4 | [▶ Abrir en Colab](https://colab.research.google.com/github/bvivanco/BSG_Scrapping_API/blob/main/notebooks/scraping_caps_3_y_4_colab.ipynb) |
| Reto | [▶ Abrir en Colab](https://colab.research.google.com/github/bvivanco/BSG_Scrapping_API/blob/main/notebooks/reto_scraping_colab.ipynb) |

> Diles que hagan **Archivo → Guardar una copia en Drive** antes de empezar: si no, sus
> cambios se pierden al cerrar la pestaña.

### Dos diferencias de Colab que conviene saber

- **Colab corre en un servidor de Google, no en tu PC.** Algunos sitios responden `403`
  a las IPs de centros de datos aunque desde tu laptop abran bien. Con `books.toscrape.com`
  y `quotes.toscrape.com` no pasa — y si pasa con otro sitio, es exactamente el bloqueo
  del que habla la diapositiva del 403.
- **Los archivos son temporales.** Para bajar un CSV a tu PC:
  ```python
  from google.colab import files
  files.download("libros.csv")
  ```
- **Scrapy no corre en Colab** (`ReactorNotRestartable`) — que es justo lo que explica la
  diapositiva de "Scrapy: consideraciones especiales". Por eso el notebook muestra los
  comandos y el spider está en `scrapy_demo/` para ejecutarlo desde la terminal.

---

## Instalación rápida

> **¿Primera vez?** Sigue [`INSTALACION.md`](INSTALACION.md): la guía paso a paso, con
> los comandos de Windows y Mac por separado y qué hacer si algo falla.

```bash
git clone https://github.com/bvivanco/BSG_Scrapping_API.git
cd BSG_Scrapping_API

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -r requirements.txt
python 00_verifica_entorno.py
```

Si `00_verifica_entorno.py` te dice **TODO LISTO**, ya puedes seguir la clase.

---

## Estructura

Los archivos están numerados en el mismo orden en que se ven en clase.
Cada uno es independiente y se ejecuta con `python <archivo>.py`.

| Archivo | Capítulo / Bloque | Qué demuestra |
|---|---|---|
| `00_verifica_entorno.py` | — | Comprueba versión de Python, `requests` y conexión a internet |
| `05_json_basico.py` | C2 · S1 · B2-B3 | `dumps` / `loads` / `dump` / `load`, tipos, tildes y `indent` |
| `06_json_anidado.py` | C2 · S2 · B1 | Objetos dentro de objetos, listas de objetos, `.get()` seguro |
| `07_json_a_tabla.py` | C2 · S2 · B3 | De JSON anidado a tabla plana: CSV y pandas |
| `09_reto_clase.py` | C2 · S2 · B3 | **Ejercicio de la sesión** (con TODOs para completar) |
| `10_scraping_primer_html.py` | C3 · S1 · B1 | Pedir HTML, encoding, User-Agent, `robots.txt`, el 403 |
| `11_html_estructura.py` | C3 · S1 · B3 | BeautifulSoup: árbol, `find` / `find_all` / `select`, atributos |
| `12_xpath_lxml.py` | C3 · S1 · B3 | XPath con lxml: `//`, `@`, `[]`, `text()`, `contains()` |
| `13_scraping_a_tabla.py` | C4 · S1 | Limpieza del dato sucio → pandas → CSV / JSON / Excel |
| `14_paginacion_y_detalle.py` | C4 · S1 | Crawling: `li.next`, `urljoin`, `sleep`, reintentos, 429 |
| `15_reto_scraping.py` | C3 + C4 | **Ejercicio de la sesión** (con TODOs para completar) |
| `scrapy_demo/` | C4 · Librerías | El mismo scraping en Scrapy, en 25 líneas (opcional) |
| `soluciones/` | — | Soluciones comentadas de los retos |
| `notebooks/` | — | Versión Jupyter / Google Colab para seguir celda por celda |
| `data/` | — | Archivos JSON de ejemplo usados en los scripts |
| `salidas/` | — | Aquí se escriben los archivos que generan los scripts |

---

## APIs usadas (todas gratuitas y sin registro)

| API | Para qué | URL |
|---|---|---|
| ExchangeRate API | Tipo de cambio USD → PEN | https://open.er-api.com/v6/latest/USD |
| Open-Meteo | Clima actual y pronóstico | https://open-meteo.com |
| JSONPlaceholder | JSON anidado de ejemplo | https://jsonplaceholder.typicode.com |
| books.toscrape | **Sitio hecho para practicar scraping** (catálogo de libros) | https://books.toscrape.com |
| quotes.toscrape | **Sitio hecho para practicar scraping** (frases y autores) | https://quotes.toscrape.com |
| httpbin | Ver qué envía tu petición y simular errores (403, 429) | https://httpbin.org |

> Los dos sitios `toscrape.com` existen justamente para aprender scraping: son sandboxes
> públicos. Practicar ahí en vez de en una web real no es solo más cómodo — es la primera
> aplicación práctica de lo que vimos en el bloque de ética.

---

## Chuleta de la clase

### Los 6 componentes de una petición

```
        método      URL base            endpoint          query params
          ↓            ↓                    ↓                  ↓
GET  https://dummyjson.com  /products/search  ?q=laptop&limit=5
     + headers  (metadatos: Authorization, Content-Type…)
     + body     (solo POST / PUT / PATCH, normalmente JSON)
```

### El patrón de 5 pasos

```python
r = requests.get(url, timeout=10)   # 1. pedir
r.raise_for_status()                # 2. verificar
data = r.json()                     # 3. convertir a dict/list
print(type(data), data.keys())      # 4. explorar
for item in data["products"]: ...   # 5. recorrer
```

### Códigos de estado

| Familia | Significa | Ejemplos |
|---|---|---|
| 2xx | Éxito | 200 OK · 201 Created · 204 No Content |
| 3xx | Redirección | 301 · 302 |
| 4xx | **La culpa es tuya** | 400 · 401 · 403 · 404 · 429 |
| 5xx | **La culpa es del servidor** | 500 · 502 · 503 |

### JSON ↔ Python

| JSON | Python |
|---|---|
| `object { }` | `dict` |
| `array [ ]` | `list` |
| `string` | `str` |
| `number` | `int` / `float` |
| `true` / `false` | `True` / `False` |
| `null` | `None` |

```python
json.dumps(dic, indent=2, ensure_ascii=False)  # Python → texto JSON
json.loads(texto)                              # texto JSON → Python
r.json()                                       # atajo de requests
```

### Regla de oro para navegar JSON

- Corchetes con **texto** → estás entrando a un **diccionario** (buscas una clave).
- Corchetes con **número** → estás entrando a una **lista** (buscas una posición, desde 0).
- ¿Perdido? Imprime `type(dato)` y `dato.keys()` antes de seguir bajando.

---

### Chuleta de Web Scraping

```python
import requests
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "MiScraper/1.0 (contacto@ejemplo.com)"}

r = requests.get(url, headers=HEADERS, timeout=10)   # 1. pedir
r.raise_for_status()                                 # 2. verificar
r.encoding = r.apparent_encoding                     # 3. arreglar tildes
sopa = BeautifulSoup(r.text, "html.parser")          # 4. parsear
for card in sopa.select("article.product_pod"):      # 5. extraer
    titulo = card.h3.a["title"]
    precio = card.select_one("p.price_color").text
```

| Quiero… | BeautifulSoup | XPath (lxml) |
|---|---|---|
| Todos los `<p>` | `find_all("p")` | `//p` |
| Por clase | `find_all("div", class_="caja")` | `//div[@class='caja']` |
| Por id | `find(id="total")` | `//*[@id='total']` |
| El texto | `find("h1").text` | `//h1/text()` |
| Un atributo | `find("a")["href"]` | `//a/@href` |
| Clase parcial | `select("div[class*=precio]")` | `//div[contains(@class,'precio')]` |

**Los tres frenos de todo scraper**

```python
MAX_PAGINAS = 3     # tu bucle SIEMPRE con tope
PAUSA = 1.0         # time.sleep() entre peticiones
timeout=10          # en cada requests.get
```

**Limpieza típica**

| Viene así | Queda así | Cómo |
|---|---|---|
| `"£51.77"` | `51.77` | `float(re.sub(r"[^\d.]", "", texto))` |
| `['star-rating','Three']` | `3` | diccionario `{"Three": 3, ...}` |
| `"\n In stock \n"` | `True` | `"in stock" in texto.strip().lower()` |
| `"catalogue/x.html"` | URL completa | `urljoin(base, href)` |
| tildes rotas en Excel | bien | `to_csv(..., encoding="utf-8-sig")` |

---

## Seguridad: nunca subas tus API Keys

Ningún ejemplo de este repo necesita clave, pero cuando uses una API que sí la pida
(Google Maps, OpenWeather, X…):

1. Copia `.env.example` a `.env` y pon ahí tu clave.
2. `.env` ya está en el `.gitignore`: **nunca** llega a GitHub.
3. Léela en el código con `os.getenv("MI_API_KEY")`.

> Hay bots que rastrean GitHub buscando claves filtradas. La factura llega igual.

---

## Errores frecuentes

| Error | Causa | Solución |
|---|---|---|
| `TypeError: 'Response' object is not subscriptable` | Usaste `r["clave"]` | Es `r.json()["clave"]` |
| `KeyError: 'brand'` | El campo no existe en ese registro | Usa `dato.get("brand", "N/D")` |
| `JSONDecodeError` | La respuesta no era JSON (fue HTML o un error) | Revisa `r.status_code` y `r.text[:200]` |
| `ModuleNotFoundError: requests` | Falta instalar o no activaste el venv | `pip install -r requirements.txt` |
| Tildes rotas (`Perú`) | `ensure_ascii` por defecto | `json.dumps(d, ensure_ascii=False)` |
| El script se queda colgado | Falta `timeout` | `requests.get(url, timeout=10)` |
| `429 Too Many Requests` | Demasiadas llamadas seguidas | `time.sleep()` entre peticiones |

### Errores frecuentes de scraping

| Error | Causa | Solución |
|---|---|---|
| `AttributeError: 'NoneType' object has no attribute 'text'` | `find()` no encontró nada y devolvió `None` | Valida antes: `el = sopa.find(...)` → `if el:` |
| `KeyError: 'class'` al filtrar | Escribiste `class=` | En Python es `class_=` (con guion bajo) |
| Sale `Â£` o `PerÃº` | Encoding mal detectado | `r.encoding = r.apparent_encoding` |
| Encuentra 0 elementos y en Chrome sí están | La página arma el contenido con JavaScript | `r.text` no lo trae → Selenium / Playwright, o busca la API interna |
| `403 Forbidden` | Te detectaron como bot | User-Agent propio, `time.sleep()`, revisar `robots.txt` |
| `429 Too Many Requests` | Vas demasiado rápido | Subir la pausa y reintentar con espera |
| El scraper "funciona" pero trae vacío | Cambió el HTML del sitio | Reinspecciona en Chrome y arregla el selector |
| `ReactorNotRestartable` | Intentaste correr Scrapy en Jupyter | Scrapy va desde la terminal (ver `scrapy_demo/`) |
