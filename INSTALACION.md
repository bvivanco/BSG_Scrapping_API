# Instalación del entorno — Curso APIs y Web Scraping

Tiempo estimado: **5 minutos**. Hazlo **antes de la clase**.

Al final debes ver el mensaje `TODO LISTO`. Si no lo ves, escríbeme con la captura.

---

## Paso 0 · ¿Tienes Python?

Abre una terminal y escribe:

- **Windows** → abre *PowerShell* (botón inicio → escribe "PowerShell")
  ```powershell
  py --version
  ```
- **Mac** → abre *Terminal* (Cmd + Espacio → escribe "Terminal")
  ```bash
  python3 --version
  ```

Debe decir **3.9 o superior** (por ejemplo `Python 3.12.1`).

> ¿Dice "no se reconoce" o "command not found"? Instala Python desde
> [python.org/downloads](https://www.python.org/downloads/).
> **En Windows, marca la casilla "Add Python to PATH"** en la primera pantalla del
> instalador. Es la que todos olvidan y la que causa el 90 % de los problemas.

---

## Paso 1 · Descargar el material

Si tienes Git:
```bash
git clone https://github.com/bvivanco/BSG_Scrapping_API.git
```

Si no tienes Git: entra a **https://github.com/bvivanco/BSG_Scrapping_API** → botón verde
**Code** → **Download ZIP** → descomprime la carpeta en tu Escritorio.

---

## Paso 2 · Entrar a la carpeta

```bash
cd ruta/hasta/BSG_Scrapping_API
```

> **Truco:** escribe `cd ` (con espacio) y **arrastra la carpeta** a la terminal.
> La ruta se escribe sola.

---

## Paso 3 · Crear el entorno virtual

Un entorno virtual es una "cajita" con las librerías de este curso, para no ensuciar
tu Python del sistema.

**Windows (PowerShell):**
```powershell
py -m venv .venv
.venv\Scripts\activate
```

**Mac / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

Sabrás que funcionó porque tu terminal ahora empieza con `(.venv)`.

> **Windows:** si sale el error rojo *"la ejecución de scripts está deshabilitada"*, corre
> esto una sola vez y vuelve a intentar el `activate`:
> ```powershell
> Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
> ```

---

## Paso 4 · Instalar las librerías

```bash
pip install -r requirements.txt
```

Instala `requests`, `pandas`, `beautifulsoup4` y `lxml`. Tarda 1-2 minutos.

---

## Paso 5 · Verificar

```bash
python 00_verifica_entorno.py
```

Debe terminar así:

```
======================================================================
TODO LISTO — puedes seguir la clase
======================================================================
```

Si dice `HAY PROBLEMAS`, mira qué línea tiene `ERROR` y revisa la tabla de abajo.

---

## Cada vez que vuelvas a trabajar

El entorno se crea **una sola vez**, pero hay que **activarlo** en cada sesión nueva
de terminal:

```bash
cd ruta/hasta/BSG_Scrapping_API
.venv\Scripts\activate      # Windows
source .venv/bin/activate   # Mac / Linux
python 10_scraping_primer_html.py
```

---

## Si algo falla

| Lo que ves | Qué significa | Solución |
|---|---|---|
| `python no se reconoce como comando` | Python no está en el PATH | Reinstala marcando "Add Python to PATH", o usa `py` en vez de `python` |
| `la ejecución de scripts está deshabilitada` | Política de PowerShell | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| `ModuleNotFoundError: requests` | No activaste el entorno | Vuelve a correr el `activate` (debes ver `(.venv)`) |
| `pip no se reconoce` | Igual que arriba | Usa `py -m pip install -r requirements.txt` |
| `No such file or directory: requirements.txt` | Estás en la carpeta equivocada | `cd` hasta la carpeta `repo` |
| La instalación se cuelga o falla por red | Firewall o proxy de tu empresa | Usa tu red personal, o pásate a Colab |

### Plan B: Google Colab (cero instalación)

Si después de 10 minutos sigues trabado, **no te frustres**: abre el notebook
directamente en Colab desde el
[README del repositorio](https://github.com/bvivanco/BSG_Scrapping_API#opción-sin-instalar-nada-google-colab) y sigue la clase desde ahí.
Trae todo preinstalado y solo necesitas tu cuenta de Google.

Lo primero al abrirlo: **Archivo → Guardar una copia en Drive**, o pierdes tu trabajo
al cerrar la pestaña.

---

## Si usas Anaconda

Ya tienes `requests`, `pandas`, `beautifulsoup4` y `lxml` instalados. Sáltate los pasos
3 y 4 y ve directo a:

```bash
python 00_verifica_entorno.py
```

## Si usas VS Code

Después del paso 3: `Ctrl+Shift+P` → *Python: Select Interpreter* → elige el que dice
`.venv`. Así el editor usa el mismo entorno que tu terminal.
