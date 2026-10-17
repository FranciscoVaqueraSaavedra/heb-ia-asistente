import os 
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma


def ini_base_vectorial(directorio_politicas="politicas/", ruta_db="chroma_db"):
    
    print("Procesamiento de politicas")
    
    documentos = []
    
    for archivo in os.listdir(directorio_politicas):
        if archivo.endswith(".pdf"):
            ruta_pdf = os.path.join(directorio_politicas, archivo)
            loader = PyPDFLoader(ruta_pdf)
            documentos.extend(loader.load())
            print(f" Cargado: {archivo}")
            
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators= ["\n\n", "\n", ".", " ", ""]
    )
    fragmentos = text_splitter.split_documents(documentos)
    print (f" Documentos divididos en {len(fragmentos)} fragmentos.")
    
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    vectorstore = Chroma.from_documents(
        documents= fragmentos,
        embedding= embeddings,
        persist_directory= ruta_db
    )
    
    print (f" Base de datos vectorial lista y guardada en: {ruta_db}")
    
if __name__ == "__main__":
    ini_base_vectorial()
             