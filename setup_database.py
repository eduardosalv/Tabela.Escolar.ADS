import mysql.connector
from mysql.connector import Error
import sqlite3
import os

def criar_banco_sqlite():
    """Cria o banco de dados SQLite como alternativa"""
    try:
        # Remove arquivo anterior se existir
        if os.path.exists('sistema_nota.db'):
            os.remove('sistema_nota.db')
        
        conexao = sqlite3.connect('sistema_nota.db')
        cursor = conexao.cursor()
        
        # Cria a tabela de funcionários
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS funcionario (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                cpf TEXT UNIQUE NOT NULL,
                senha TEXT NOT NULL
            )
        """)
        
        # Cria a tabela de alunos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS alunos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                cpf TEXT UNIQUE NOT NULL,
                endereco TEXT NOT NULL,
                matricula TEXT UNIQUE
            )
        """)
        
        # Cria a tabela de notas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                aluno_id INTEGER NOT NULL,
                disciplina TEXT NOT NULL,
                nota REAL NOT NULL,
                funcionario_id INTEGER NOT NULL,
                FOREIGN KEY (aluno_id) REFERENCES alunos(id),
                FOREIGN KEY (funcionario_id) REFERENCES funcionario(id)
            )
        """)
        
        # Insere funcionário de teste
        cursor.execute("""
            INSERT OR IGNORE INTO funcionario (nome, cpf, senha)
            VALUES ('Administrador', '12345678900', 'admin123')
        """)
        
        conexao.commit()
        conexao.close()
        
        print("✅ Banco de dados SQLite criado com sucesso!")
        print("✅ Funcionário de teste criado!")
        print("   CPF: 12345678900")
        print("   Senha: admin123")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar banco SQLite: {e}")
        return False

def criar_banco_mysql():
    """Cria o banco de dados MySQL"""
    conexao = None
    try:
        # Conecta ao MySQL sem especificar banco
        conexao = mysql.connector.connect(
            host='localhost',
            user='root',  # Altere para seu usuário MySQL
            password=''   # Altere para sua senha MySQL
        )
        
        if conexao.is_connected():
            cursor = conexao.cursor()
            
            # Cria o banco de dados
            cursor.execute("CREATE DATABASE IF NOT EXISTS sistema_nota")
            print("✅ Banco de dados 'sistema_nota' criado/verificado com sucesso!")
            
            # Usa o banco de dados
            cursor.execute("USE sistema_nota")
            
            # Cria a tabela de funcionários
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS funcionario (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nome VARCHAR(100) NOT NULL,
                    cpf VARCHAR(15) UNIQUE NOT NULL,
                    senha VARCHAR(100) NOT NULL
                )
            """)
            
            # Cria a tabela de alunos
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS alunos (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nome VARCHAR(100) NOT NULL,
                    cpf VARCHAR(15) UNIQUE NOT NULL,
                    endereco TEXT NOT NULL,
                    matricula VARCHAR(20) UNIQUE
                )
            """)
            
            # Cria a tabela de notas
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS notas (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    aluno_id INT NOT NULL,
                    disciplina VARCHAR(100) NOT NULL,
                    nota DECIMAL(5,2) NOT NULL,
                    funcionario_id INT NOT NULL,
                    FOREIGN KEY (aluno_id) REFERENCES alunos(id),
                    FOREIGN KEY (funcionario_id) REFERENCES funcionario(id)
                )
            """)
            
            print("✅ Tabelas criadas com sucesso!")
            
            # Insere funcionário de teste
            cursor.execute("""
                INSERT IGNORE INTO funcionario (nome, cpf, senha)
                VALUES ('Administrador', '12345678900', 'admin123')
            """)
            
            print("✅ Funcionário de teste criado!")
            print("   CPF: 12345678900")
            print("   Senha: admin123")
            
            conexao.commit()
            return True
            
    except Error as e:
        print(f"❌ Erro ao conectar ao MySQL: {e}")
        return False
        
    finally:
        if conexao and conexao.is_connected():
            cursor.close()
            conexao.close()

def criar_banco_dados():
    """Tenta criar o banco MySQL, se falhar usa SQLite"""
    print("🔧 Configurando banco de dados...")
    
    # Tenta MySQL primeiro
    if criar_banco_mysql():
        print("✅ MySQL configurado com sucesso!")
        return
    
    # Se MySQL falhar, usa SQLite
    print("⚠️  MySQL não disponível. Usando SQLite...")
    if criar_banco_sqlite():
        print("✅ SQLite configurado com sucesso!")
        # Atualiza o arquivo conexao.py para usar SQLite
        atualizar_conexao_sqlite()
    else:
        print("❌ Falha ao configurar banco de dados")

def atualizar_conexao_sqlite():
    """Atualiza o arquivo conexao.py para usar SQLite"""
    try:
        with open('conexao.py', 'w', encoding='utf-8') as f:
            f.write('''import sqlite3

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
            print(f"\\nBem-vindo(a), {nome}!")
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
''')
        print("✅ Arquivo conexao.py atualizado para SQLite!")
    except Exception as e:
        print(f"❌ Erro ao atualizar conexao.py: {e}")

if __name__ == "__main__":
    criar_banco_dados()
    print("\n🎉 Configuração concluída! Agora você pode executar o sistema.") 