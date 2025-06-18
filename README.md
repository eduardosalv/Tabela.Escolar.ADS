Sistema de Cadastro e Consulta de Notas
Projeto em Python com MySQL para cadastrar alunos, lançar notas e permitir login de funcionários.

📁 Arquivos principais
main.py – Menu principal para interação com o sistema
login.py – Login de funcionários
cadastro.py – Cadastro de alunos e notas
conexao.py – Conexão com o banco de dados MySQL
script_sistema_notas.sql – Script para criar o banco de dados e tabelas
⚙️ Como usar
Crie o banco de dados no MySQL executando o script_sistema_notas.sql.
No arquivo conexao.py, configure o usuário e a senha do seu MySQL.
Instale a biblioteca de conexão com MySQL:
pip install mysql-connector-python
No terminal, execute o sistema:
   python main.py
👤 Acesso de funcionário (para testes)

Antes de usar, insira manualmente um funcionário no banco de dados para poder logar.

Exemplo de SQL:

INSERT INTO funcionario (nome, cpf, senha)
VALUES ('Yudy', '12345678900', 'senha4002');
✅ Funções prontas
Login com CPF e senha

Cadastro de aluno e nota

Nota vinculada a uma disciplina e ao funcionário

👥 Equipe do projeto
Maria Eduarda – Estrutura do Projeto e Banco de Dados

Hugo Leonardo – Cadastro de Alunos e Notas

Pessoa 3 – Consulta de Dados (em desenvolvimento)

Pessoa 4 – GitHub, Documentação e Vídeo
