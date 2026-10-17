# Asistente Ejecutivo para Gerencia H-E-B

Asistente de IA conversacional para gerentes de tienda de H-E-B. Combina consultas analíticas sobre datos estructurados (ventas e inventarios) con recuperación documental de políticas internas y manuales operativos (RAG), y responde en un formato ejecutivo orientado a la toma de decisiones.

---

## Arquitectura del sistema

El proyecto implementa un agente **ReAct** con LangChain que decide automáticamente entre dos motores especializados:

1. **Motor de datos (SQL):** base SQLite (`tiendas.db`) con datos transaccionales y de inventario de **junio a agosto de 2026**. El agente traduce la pregunta a SQL y responde con cifras exactas.
2. **Motor de políticas (RAG):** base vectorial local en ChromaDB, indexada con embeddings, que busca en los manuales en PDF y cita en la respuesta el nombre del manual y la página de origen.

## Estructura del proyecto

```
heb-ia-asistente/
├── app.py                # Interfaz Gradio y agente ReAct
├── motor_datos.py        # Carga los CSV de datos/ a SQLite (tiendas.db)
├── motor_politicas.py    # Indexa los PDF de politicas/ en ChromaDB
├── datos/                # CSV de origen
├── politicas/            # Manuales y políticas en PDF
├── requirements.txt
└── .env.example
```

---

## Guía de instalación y ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/FranciscoVaqueraSaavedra/heb-ia-asistente.git
cd heb-ia-asistente
```

### 2. Crear y activar el entorno virtual

**Windows (PowerShell)**
```bash
python -m venv venv
.\venv\Scripts\Activate
```
Si PowerShell bloquea la activación, ejecuta antes:
`Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned`

**macOS / Linux**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar las dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar la API key de Google Gemini

Por seguridad, las credenciales no se incluyen en el repositorio.

1. Genera una llave en [Google AI Studio](https://aistudio.google.com/app/apikey).
2. Copia `.env.example` como `.env` en la carpeta raíz.
3. Reemplaza el valor por tu llave real:

```
GOOGLE_API_KEY=tu_api_key_aqui
```

### 5. Construir las bases de datos

Ejecuta una sola vez (la primera vez descarga el modelo de embeddings, por lo que requiere internet):

```bash
python motor_datos.py
python motor_politicas.py
```

Esto genera `tiendas.db` (desde `datos/`) y `chroma_db/` (desde `politicas/`).

### 6. Ejecutar la aplicación

```bash
python app.py
```

La terminal mostrará un enlace local (normalmente `http://127.0.0.1:7860`). Ábrelo en el navegador para usar el asistente.

---

## Stack tecnológico

- **Lenguaje:** Python 3.13
- **Orquestador de IA:** LangChain 0.2.16
- **LLM:** Google Gemini 3.8 Flash (`temperature=0` para respuestas deterministas)
- **Almacenamiento:** SQLite y ChromaDB (vector store local)
- **Embeddings:** HuggingFace `all-MiniLM-L6-v2`
- **Interfaz:** Gradio

## Limitaciones

- Solo hay datos de ventas de junio a agosto de 2026.
- El motor SQL ejecuta consultas generadas por el LLM; es adecuado para un prototipo, pero en producción debería usar una conexión de solo lectura.