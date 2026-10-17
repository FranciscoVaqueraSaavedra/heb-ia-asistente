import gradio as gr
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_react_agent, Tool
from langchain_core.prompts import PromptTemplate
from langchain_experimental.sql import SQLDatabaseChain
from langchain_community.utilities import SQLDatabase
from dotenv import load_dotenv


load_dotenv()


llm = ChatGoogleGenerativeAI(model="gemini-3.8-flash", temperature=0)

db = SQLDatabase.from_uri("sqlite:///tiendas.db")
sql_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma(persist_directory="chroma_db", embedding_function=embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

def consultar_politicas(query):
    docs = retriever.invoke(query)
    
    fragmentos_fuente = []
    for d in docs:
        fuente = d.metadata.get("source", "Manual Desconocido")
        pagina = d.metadata.get("page", "N/A")
        texto = d.page_content
        fragmentos_fuente.append(f"[FUENTE: {fuente} - Página: {pagina}]\n{texto}")
    
    contexto = "\n\n".join(fragmentos_fuente)
    prompt = f"""
    Basado estrictamente en este contexto de políticas internas de H-E-B, responde a la pregunta. 
    REGLA OBLIGATORIA: En tu respuesta, debes mencionar explícitamente el nombre del manual y la página de donde obtuviste la información, usando el formato (Fuente: [Nombre del Manual], Pág: [Número]).
    
    Contexto: 
    {contexto}
    
    Pregunta: {query}
    """
    return llm.invoke(prompt).content

tools = [
    Tool(
        name="Base_Datos_Tiendas",
        func=sql_chain.run,
        description="Útil para responder preguntas sobre ventas, inventarios, tickets o tiendas. Requiere consultas sobre cifras exactas."
    ),
    Tool(
        name="Manuales_Politicas",
        func=consultar_politicas,
        description="Útil para responder preguntas sobre reglas, políticas de mermas, manuales de apertura, devoluciones y recursos humanos."
    )
]

TEMPLATE_AGENTE = """
Eres un asistente ejecutivo para una gerente de tienda retail de H-E-B.
REGLA 1: Tus respuestas deben ser directas, estructuradas en viñetas y orientadas a la toma de decisiones. Evita párrafos largos.
REGLA 2: Solo tienes datos de ventas de Junio a Agosto de 2026. Si preguntan por periodos fuera de este rango, indica explícitamente que no tienes la información, y ofrece los datos del mes disponible más cercano.

Tienes acceso a las siguientes herramientas:
{tools}

Usa estrictamente este formato en inglés para tu lógica interna (pero responde al usuario en español):
Question: la pregunta del usuario
Thought: piensa paso a paso qué hacer
Action: la acción a tomar, debe ser exactamente una de [{tool_names}]
Action Input: la pregunta o entrada para la acción
Observation: el resultado de la acción
... (este ciclo Thought/Action/Action Input/Observation puede repetirse varias veces)
Thought: Ya tengo la información necesaria para responder
Final Answer: tu respuesta final ejecutiva y en español para la gerente

¡Comienza!
Question: {input}
Thought: {agent_scratchpad}
"""

prompt = PromptTemplate.from_template(TEMPLATE_AGENTE)
agente_react = create_react_agent(llm, tools, prompt)
agente = AgentExecutor(agent=agente_react, tools=tools, verbose=True, handle_parsing_errors=True)

def responder(mensaje, historial):
    try:
        respuesta = agente.invoke({"input": mensaje})
        return respuesta["output"]
    except Exception as e:
        return f"⚠️ Ocurrió un error al procesar la consulta: {str(e)}"

demo = gr.ChatInterface(
    fn=responder,
    title="🛒 Asistente Ejecutivo para Gerencia H-E-B",
    description="Pregúntame sobre ventas, inventarios o políticas operativas de la tienda. El agente decidirá automáticamente si busca en la base de datos (SQL) o en los manuales (PDFs)."
)

if __name__ == "__main__":
    demo.launch()