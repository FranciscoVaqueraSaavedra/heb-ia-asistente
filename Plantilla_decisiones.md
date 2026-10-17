# Documento de decisiones

Nombre: Francisco Vaquera Saavedra
Fecha: 16 de Octubre 2026
Repositorio: heb-ia-asistente
Proveedor y modelos usados: Google Gemini 3.8 Flash (via LangChain), HuggingFace Embeddings (all-MiniLM-L6-v2)

## 1. Qué construí y por qué en ese orden
- Desarrollé un asistente conversacional inteligente con arquitectura ReAct para gerentes de tienda H-E-B, aquí se busca priorizar la precisión analítica y operativa.
- Primero tuve que estructurar el motor SQL (SQLite) para que las respuestas sean deterministas y exactas sobre las ventas e inventarios corporativos. 
- Posteriormente tuve que integrar el motor RAG (ChromaDB) con metadatos de orgen para consulta documental de los manuales y políticas que son internas. 
- Finalmente, uní ambos bajo un orquestador de LangChain y una interfaz gráfica en Gradio. 

## 2. Qué decidí no hacer
- Descarté el uso de una base de datos vectorial en la nube (como podria ser Pinecone o Weaviate) para que el proyecto sea local y reproducible en el tiempo acordado. 
- Evite usar modeloes Pro que son más grandes y costosos como el GPT*4, donde seleccione Gemini 3.8 Flash por su velocidad, bajo coste y su desempeño con una temperatura 0. 
- Omití usar algun framework de intefaz gráfica al detectar un bloqueo de dependencias asincronas en mi Windows. 

## 3. Cómo sé que funciona
- Hice pruebas unitarias de integración donde el agente selecciona de manera autónoma la herramientas correcta según la intención de la pregunta. 
- Valide las consultas cuantitativas retornen cifras exactas desde la base de datos SQL donde no presenta alucinaciones numéricas. 
- Comprobe que el sistema RAG extrae los fragmentos correctos de los manuales PDF y los adjunta de una forma transparente el nombre de la fuente y la página. 

## 4. Costo por interacción y cómo lo medí
- El costo por interacción es aproximadamente **$0.00000035 USD por consulta**.
- Para medir esto tuve que calcular un promedio de 1,000 tokes de entrada y 300 tokens de salida por consulta. Donde aplicando las tarifas oficiales de Google Gemini Flash son aprox $0.075 USD por millón de token de entrada y $0.30 USD por millón de salida. 
- De forma adicional, los costos de infraestructura de base de datos (SQLite) y búsqueda vectorial (ChromaDB con embeddings locales) son de **$0 USD**, al ejecutarse enteramente de forma local en el equipo. 

## 5. Qué haría con dos semanas más
- Creó que implmeentaría un sistema de memoria convrsacional avanada para poder retener el contexto multihilo a lo largo de toda la sesión 
- Para algo más técnico añadiría diferentes gráficos dinámicos que esten integrados en la interfaz usando Pandas y Matplot para poder visualizar tendencias de ventas directamente en el chat.
- Colocar la slución en un contenedor Docker que tenga autenticación OAuth para ver la posibilidad de hacer una prueba piloto real en algunas sucursale de H-E-B.