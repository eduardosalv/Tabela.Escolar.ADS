import sqlite3

def login_funcionario():  # Função para autenticar o funcionário
    cpf = input("CPF: ").strip()  # Solicita o CPF do funcionário
    senha = input("Senha: ").strip()  # Solicita a senha

    try:
        conexao = sqlite3.connect('sistema_nota.db')  # Conecta ao banco SQLite
        cursor = conexao.cursor()

        # Consulta no banco se existe um funcionário com o CPF e senha fornecidos
        query = "SELECT id, nome FROM funcionario WHERE cpf = ? AND senha = ?"
        cursor.execute(query, (cpf, senha))
        resultado = cursor.fetchone()  # Tenta obter o resultado da consulta

        if resultado:
            funcionario_id, nome = resultado  # Extrai o ID e nome do funcionário
            print(f"\nBem-vindo(a), {nome}!")  # Mensagem de boas-vindas
            return funcionario_id  # Retorna o ID para ser usado no sistema
        else:
            print("CPF ou senha incorretos.")  # Mensagem de erro caso não encontre
            return None  # Login falhou

    except Exception as erro:
        print("Erro ao fazer login:", erro)  # Mostra erro em caso de falha
        return None

    finally:
        if conexao:  # Fecha conexão se estiver ativa
            cursor.close()
            conexao.close()
