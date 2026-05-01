import os
from dotenv import load_dotenv
import mysql.connector
import cohere
import json

# Carrega as variáveis de ambiente
load_dotenv()

api_key = os.getenv('COHERE_API_KEY')
db_user = os.getenv('DB_PASSWORD')
db_pass = os.getenv('DB_PASSKEY')

# Inicializando o cliente Cohere
co = cohere.Client(api_key)

def buscar_exercicios_do_banco(objetivo_usuario):
    try:
        conexao = mysql.connector.connect(
            host='localhost',
            user=db_user,
            password=db_pass,
            database='personal_ai'
        )
        cursor = conexao.cursor()
        cursor.execute("SELECT nome FROM exercicios;")
        exercicios_disponiveis = [row[0] for row in cursor.fetchall()]


        cursor.execute("SELECT DISTINCT grupamento_muscular FROM exercicios;")
        grupos_possiveis = [row[0] for row in cursor.fetchall()]
        grupos_encontrados =[]
        

        for grupo in grupos_possiveis:
            if grupo.lower() in objetivo_usuario.lower():
                grupos_encontrados.append(grupo)
        if not grupos_encontrados:
            return []        
        format_strings = ','.join(['%s'] * len(grupos_encontrados))
        querry = f"SELECT nome, grupamento_muscular FROM exercicios WHERE grupamento_muscular in ({format_strings})"
        cursor.execute(querry,tuple(grupos_encontrados))
        exercicios = cursor.fetchall()
        conexao.close()
        return exercicios
        
    except Exception as e:
        print(f'Erro ao conectar no banco: {e}')
        return []
    
def salvar_ficha_de_treino_no_banco(objetivo,divisao,treino_texto):
    try:
        conexao = mysql.connector.connect(
            host='localhost',
            user=db_user,
            password=db_pass,
            database='personal_ai'
        )
        cursor = conexao.cursor()
        
        
           
        dados_treino = {
            "objetivo": objetivo,
            "divisao": divisao,
            "treino": treino_texto
        }

        treino_json = json.dumps(dados_treino)

        sql = "INSERT INTO fichas_treino (nome_usuario, objetivo,divisao,treino_json) VALUES (%s, %s, %s, %s)"
        user_name = input("Digite seu nome para salvar a ficha de treino:\n")
        values = (user_name, objetivo, divisao, treino_json)
        cursor.execute(sql, values)
        conexao.commit()
        print("Ficha de treino salva com sucesso!")
        conexao.close()
    except Exception as e:
        print(f'Erro ao salvar ficha de treino: {e}')

def gerar_treino_com_ia():
    
    objetivo = input("Qual seu foco de treino hoje? (EX: Hipertrofia de Peito): ")
    divisao = input("Qual a divisão do treino? (EX: A,B,C, Fullbody): ")
    
    exercicios_filtrados = buscar_exercicios_do_banco(objetivo)
    
    if not exercicios_filtrados:
        print("Não entendi os grupos musculares ou não temos exercícios para eles.")
        return

    lista_texto = ','.join([f"{ex[0]}({ex[1]})" for ex in exercicios_filtrados])
  

    # Engenharia de prompt
    prompt_ia = f"""Você é um Personal Trainer de alto nível.
    O aluno quer treinar: {objetivo}.

    REGRAS OBRIGATÓRIAS:
    1. Use APENAS exercícios desta lista: {lista_texto}
    2. Não inclua exercícios que o aluno NÃO pediu.
    3. Se o aluno pediu 'Peito', não sujira 'Pernas'.

    Formate o treino assim:
    - [Nome do Exercício] | [Séries x Repetições] | [Dica rápida de execução]
    """
    print("\nGerando treino... aguarde...")

    try:
        # Chamada para a API
        response = co.chat(
            model='command-r-08-2024',
            message=prompt_ia
        )

        print("\n--- SEU TREINO GERADO POR IA ---")
        print(response.text)


        salvar_ficha_de_treino_no_banco(objetivo, divisao, response.text)
    except Exception as e:
        print(f"Erro ao gerar treino: {e}")

# Garante que o script rode apenas se executado diretamente
if __name__ == "__main__":
    gerar_treino_com_ia()



