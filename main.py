import os
from dotenv import load_dotenv
import mysql.connector
import cohere

# Carrega as variáveis de ambiente
load_dotenv()

api_key = os.getenv('COHERE_API_KEY')
db_user = os.getenv('DB_PASSWORD')
db_pass = os.getenv('DB_PASSKEY')

# Inicializando o cliente Cohere
co = cohere.Client(api_key)

def buscar_exercicios_do_banco():
    try:
        conexao = mysql.connector.connect(
            host='localhost',
            user=db_user,
            password=db_pass,
            database='personal_ai'
        )
        cursor = conexao.cursor()
        cursor.execute("SELECT nome FROM exercicios")
        
        # Pega a primeira coluna de cada linha (o nome)
        exercicios = [row[0] for row in cursor.fetchall()]
        
        cursor.close()
        conexao.close()
        return exercicios
    except Exception as e:
        print(f'Erro ao conectar no banco: {e}')
        return []
    
def gerar_treino_com_ia():
    # Pegando dados do MySQL
    lista_disponivel = buscar_exercicios_do_banco()
    
    if not lista_disponivel:
        print("Nenhum exercício encontrado. Verifique seu banco de dados.")
        return

    exercicios_str = ", ".join(lista_disponivel)

    # Input do usuário
    objetivo = input("Qual seu foco de treino hoje? (EX: Hipertrofia de Peito): ")

    # Engenharia de prompt
    prompt_ia = f"""Você é um personal trainer de alto nível.
    O aluno quer: {objetivo}.
    Você só pode usar exercícios dessa lista: {exercicios_str}.
    Monte a ficha com:
    - Nome do Exercício
    - Séries e Repetições
    - Dica rápida de execução"""

    print("\nGerando treino... aguarde...")

    try:
        # Chamada para a API
        response = co.chat(
            model='command-r-08-2024',
            message=prompt_ia
        )

        print("\n--- SEU TREINO GERADO POR IA ---")
        print(response.text)
    except Exception as e:
        print(f"Erro ao gerar treino: {e}")

# Garante que o script rode apenas se executado diretamente
if __name__ == "__main__":
    gerar_treino_com_ia()