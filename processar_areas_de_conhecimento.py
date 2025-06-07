from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from PIL import Image
import pytesseract
import os

import sqlite3

MODELO = "pierreguillou/byt5-small-qa-squad-v1.1-portuguese"

MAXIMO_IMAGENS = 1_000
CAMINHO_IMAGENS = "C:\\Users\\amand\\Downloads\\bibliotecario-parcial (2)\\bibliotecario\\artigos"
CAMINHO_BD = "C:\\Users\\amand\\Downloads\\bibliotecario-parcial (2)\\bibliotecario"

BD_ARTIGOS = f"{CAMINHO_BD}/artigos.sqlite3"

AREAS_POR_ARTIGO = 7

def inicializar():
    inicializado, corretor_gramatical = False, None

    try:
        tokenizador = AutoTokenizer.from_pretrained(MODELO)
        modelo = AutoModelForSeq2SeqLM.from_pretrained(MODELO)

        corretor_gramatical = pipeline("text2text-generation", model=modelo, tokenizer=tokenizador)

        conexao = sqlite3.connect(BD_ARTIGOS)
        cursor = conexao.cursor()
        cursor.execute("DROP TABLE IF EXISTS areas")
        cursor.execute("CREATE TABLE areas(id_artigo INTEGER, area1 TEXT, area2 TEXT, area3 TEXT, area4 TEXT, area5 TEXT, area6 TEXT, area7 TEXT)")
        conexao.close()

        inicializado = True
    except Exception as e:
        print(f"erro inicializando: {str(e)}")

    return inicializado, corretor_gramatical

def get_areas_de_conhecimento(imagem, corretor_gramatical):
    areas_corrigidas = []

    texto = pytesseract.image_to_string(Image.open(imagem), lang="por")
    areas = texto.split("\n")
    areas = [area for area in areas if area != '']

    for area in areas:
        prompt = f"grammar: {area}"

        resultado = corretor_gramatical(prompt, max_new_tokens=256,clean_up_tokenization_spaces=True)
        texto = resultado[0]["generated_text"]
        if texto and texto not in areas_corrigidas: 
            areas_corrigidas.append(texto)

    return areas_corrigidas

def gravar_areas(id_artigo, areas):
    conexao = sqlite3.connect(BD_ARTIGOS)
    cursor = conexao.cursor()

    while len(areas) < AREAS_POR_ARTIGO:
        areas.append("")

    insert = f"INSERT INTO areas(id_artigo, area1, area2, area3, area4, area5, area6, area7) VALUES ({id_artigo}"
    for contador, area in enumerate(areas):
        contador += 1

        insert += f", '{area.lower()}'"

        if contador == AREAS_POR_ARTIGO:
            break
    insert += ")"

    cursor.execute(insert)
    conexao.commit()
    conexao.close()

def visualizar_areas():
    conexao = sqlite3.connect(BD_ARTIGOS)

    cursor = conexao.cursor()
    cursor.execute("SELECT id, titulo, area1, area2, area3, area4, area5, area6, area7 FROM artigos, areas WHERE areas.id_artigo = artigos.id")

    artigos = cursor.fetchall()
    conexao.close()

    return artigos

if __name__ == "__main__":
    inicializado, corretor_gramatical = inicializar()

    if inicializado:
        for contador in range(1, MAXIMO_IMAGENS):
            imagem = f"{CAMINHO_IMAGENS}/{contador}.disciplinas.png"
            if os.path.exists(imagem):
                print(f"processando a imagem: {imagem}")
                areas = get_areas_de_conhecimento(imagem, corretor_gramatical)

                print(f"áreas encontradas: {areas}")

                gravar_areas(contador, areas)
            else:
                break

    print(f"areas por artigos: {visualizar_areas()}")
