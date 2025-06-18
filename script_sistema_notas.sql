CREATE DATABASE IF NOT EXISTS sistema_nota;
USE sistema_nota;

-- Tabela de funcionários
CREATE TABLE IF NOT EXISTS funcionario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(15) UNIQUE NOT NULL,
    senha VARCHAR(100) NOT NULL
);

-- Tabela de alunos com CPF, endereço e matrícula
CREATE TABLE IF NOT EXISTS alunos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(15) UNIQUE NOT NULL,
    endereco TEXT NOT NULL,
    matricula VARCHAR(20) UNIQUE
);

-- Tabela de notas
CREATE TABLE IF NOT EXISTS notas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    aluno_id INT NOT NULL,
    disciplina VARCHAR(100) NOT NULL,
    nota DECIMAL(5,2) NOT NULL,
    funcionario_id INT NOT NULL,
    FOREIGN KEY (aluno_id) REFERENCES alunos(id),
    FOREIGN KEY (funcionario_id) REFERENCES funcionario(id)
);
