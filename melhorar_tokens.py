from inicializar_modelo import *

def melhorar_tokens(lista_parametro):

    prompts = [
        ("system", "A sua missão é melhorar as palavras que serão enviadas para você via prompt, elas estão em uma lista de strings. A tecnologia utilizada no projeto é o python."),
        ("system", "Essas palavras fazem parte do contexto da tecnologia da informação, deve ser removidos erros gramaticais, removidas redundâncias e reajustado o que for necessário, sem perder o sentido da sentença"),
        ("system", "remova palavras repetidas"),
        ("system", "Quando você encontrar palavras que tem a conjunção coordenativa aditiva, o 'e' na sentença, separe em uma nova palavra"),
        ("system", "Retorne apenas a palavra ou sentença melhorada"),
        ("system", "Remova todas as notações ```python e ```"),
        ("system", "Remova todas de markdown`"),
        ("system", "Retorne apenas o que foi pedido sem explicações adicionais e sem notações especiais."),
        ("human", "{lista}")
    ]

    inicializada, IA = iniciar_IA(prompts)

    if inicializada:
        print(f"IA inicializada, processando de melhoria dos tokens...")

        sucesso, resposta = obter_resposta(IA, {"lista": lista_parametro })
        rawContent = resposta.content
        content = rawContent.split('\n')
        print(f"content: {content}")

        return sucesso, content
