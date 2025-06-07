from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

import os

API_KEY = "C:/Users/amand/Downloads/bibliotecario-parcial (2)/bibliotecario/genai.key"
# MODELO = "gemini-2.0-flash-001"
MODELO = "gemini-2.5-flash-preview-04-17"

def iniciar_IA(contexto):
    inicializada, IA = False, None
    
    try:
        with open(API_KEY, "r") as arquivo_chave:
            chave = arquivo_chave.read()
            os.environ["GOOGLE_API_KEY"] = chave

            arquivo_chave.close()

        llm = ChatGoogleGenerativeAI(model=MODELO, temperature=0, max_tokens=None, timeout=None, max_retries=4)
        IA = ChatPromptTemplate.from_messages(contexto) | llm

        inicializada = True
    except Exception as e:
        print(f"ocorreu um erro iniciando a IA: {str(e)}")
    
    return inicializada, IA


def obter_resposta(IA, parametros):
    sucesso, resposta = False, None
    
    try:
        resposta = IA.invoke(parametros)

        sucesso = True
    except Exception as e:
        print(f"ocorreu um erro testando o prompt: {str(e)}")

    return sucesso, resposta

# if __name__ == "__main__":
#     prompts = [
#         ("system", "Você é um assistente capaz de traduzir do português para o inglês"),
#         ("system", "Traduza a sentença informada pelo usuário e forneça uma resposta direta, sem qualquer enunciado ou comentário"),
#         ("human", "{sentenca}")
#     ]
#     inicializada, IA = iniciar_IA(prompts)
    
#     if inicializada:
#         sucesso, resposta = obter_resposta(IA, {"sentenca": "estou com fome, quero almoçar"})
#         if sucesso:
#             print(f"Resposta: {resposta.content}") 