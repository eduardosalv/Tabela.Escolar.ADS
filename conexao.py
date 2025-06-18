import sqlite3

def conectar():
    """Função para conectar ao banco de dados SQLite"""
    try:
        conexao = sqlite3.connect('sistema_nota.db')
        return conexao
    except Exception as e:
        print(f"Erro ao conectar ao SQLite: {e}")
        return None

def login_funcionario():
    """Função para autenticar funcionário"""
    conexao = None
    cursor = None
    try:
        conexao = conectar()
        if not conexao:
            print("Erro: Não foi possível conectar ao banco de dados.")
            return None
            
        cursor = conexao.cursor()

        cpf = input("CPF: ")
        senha = input("Senha: ")

        cursor.execute("SELECT id, nome FROM funcionario WHERE cpf = ? AND senha = ?", (cpf, senha))
        resultado = cursor.fetchone()

        if resultado:
            funcionario_id, nome = resultado
            print(f"\nBem-vindo(a), {nome}!")
            return funcionario_id
        else:
            print("CPF ou senha incorretos.")
            return None

    except Exception as e:
        print(f"Erro no login: {e}")
        return None

    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()
