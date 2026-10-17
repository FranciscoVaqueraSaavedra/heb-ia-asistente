# Documento de decisiones

**Nombre:** Francisco Vaquera Saavedra
**Fecha:** 16 de octubre de 2026
**Repositorio:** heb-ia-asistente
**Proveedor y modelos:** Google Gemini 3.8 Flash (vía LangChain) y HuggingFace Embeddings (all-MiniLM-L6-v2)

## 1. Qué construí y por qué en ese orden
- Construí un asistente conversacional con arquitectura ReAct para gerentes de tienda de H-E-B, priorizando la precisión analítica y operativa.
- Primero estructuré el motor SQL (SQLite), porque las preguntas sobre ventas e inventarios requieren cifras exactas y es la parte más fácil de validar contra los CSV originales.
- Después integré el motor RAG (ChromaDB), con metadatos de fuente y página, para consultar los manuales y políticas internas.
- Por último los unifiqué bajo un agente de LangChain que decide qué herramienta usar, y agregué la interfaz en Gradio.

## 2. Qué decidí no hacer
- No usé una base vectorial en la nube (Pinecone, Weaviate) para mantener el proyecto local, reproducible y sin costo de infraestructura.
- No usé un modelo más grande y costoso (por ejemplo, de tipo Pro). Elegí Gemini 3.8 Flash por su velocidad y bajo costo, con `temperature=0` para respuestas consistentes.
- Descarté Chainlit como interfaz por conflictos de dependencias asíncronas en Windows, y usé Gradio por su estabilidad. 
- No implementé memoria conversacional ni autenticación en esta versión, para acotar el alcance.

## 3. Cómo sé que funciona
- Probé manualmente el agente con las preguntas de `ejemplos_prueba.md` y verifiqué que elige la herramienta correcta (SQL o manuales) según la intención. 
- Contrasté las cifras que devuelve el motor SQL contra los CSV originales y no encontré discrepancias en las preguntas probadas. 
- Comprobé que el motor RAG recupera fragmentos relevantes y cita el nombre del manual y la página en la respuesta.
- Limitación: no tengo un conjunto de pruebas automatizado, y el SQL lo genera el LLM, por lo que puede equivocarse en preguntas complejas.

## 4. Costo por interacción y cómo lo medí
- Medí el consumo real con un callback propio de LangChain (`ContadorTokens`) que suma los tokens de todas las llamadas al LLM dentro de cada consulta. Probé 10 consultas representativas (7 distintas, 2 repetidas), mezclando preguntas de SQL y de manuales.
- Resultados: **4.0 llamadas al LLM por consulta**, **≈ 15,172 tokens de entrada** y **≈ 2,043 tokens de salida** en promedio. El rango fue de 6,586 a 41,801 tokens de entrada.
- Con las tarifas de Gemini Flash usadas en este proyecto ($0.075 USD por millón de tokens de entrada y $0.30 USD por millón de salida), el costo promedio es de **≈ $0.00175 USD por consulta** (rango: $0.0007 a $0.0047). Equivale a unos $1.75 USD por cada 1,000 consultas. Las tarifas deben confirmarse en la página oficial de precios de Google, porque cambian.
- SQLite, ChromaDB y los embeddings corren en local, por lo que su costo es $0 USD.
- Limitación: la muestra es pequeña (9 consultas). Con más volumen o preguntas más complejas el promedio puede variar.

## 5. Qué haría con dos semanas más
Ordenado por prioridad, según lo que aprendí al medir el sistema:

1. **Optimizar el consumo de tokens.** El agente promedia 4 llamadas y ≈15,000 tokens de entrada por consulta. Reduciría el esquema SQL que ve el modelo (`include_tables`, menos filas de muestra), bajaría los fragmentos recuperados de 3 a 2 y limitaría las iteraciones del agente. Mediría el efecto con el mismo contador de tokens.
2. **Pruebas automatizadas.** Convertir `ejemplos_prueba.md` en un conjunto de preguntas con respuestas esperadas (cifras contra los CSV y citas contra los manuales). Con eso podría evaluar con datos si un modelo más barato mantiene la calidad antes de cambiarlo.
3. **Seguridad del motor SQL.** Usar una conexión de solo lectura, porque hoy el LLM genera las consultas.
4. **Gráficas de tendencias de ventas** (Pandas y Matplotlib) integradas en el chat.
5. **Memoria conversacional**, una vez optimizado el consumo, porque agregar historial aumenta los tokens de entrada en cada llamada.
6. **Piloto controlado:** contenerizar con Docker y agregar autenticación OAuth para probarlo en pocas sucursales.