import mysql.connector


def conectar():
    try:
        conexao = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='personal_ai'
        )
        if conexao.is_connected():
            print(f'A conexao com o banco de dados: {conexao.database} foi concluida!')
            return conexao
    except Exception as e:
        print(f'Erro ao conectar: {e}')
if __name__ == "__main__":
    conectar()

   