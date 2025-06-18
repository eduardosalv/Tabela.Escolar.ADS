import sqlite3

def cadastrar_aluno(nome, cpf, endereco):
    """Função para cadastrar um novo aluno"""
    if not nome.strip():
        print("Erro: Nome não pode estar vazio.")
        return False

    if not cpf.strip():
        print("Erro: CPF não pode estar vazio.")
        return False

    if not endereco.strip():
        print("Erro: Endereço não pode estar vazio.")
        return False

    try:
        conexao = sqlite3.connect('sistema_nota.db')
        cursor = conexao.cursor()

        # Verifica se o aluno já existe pelo CPF
        cursor.execute("SELECT id FROM alunos WHERE cpf = ?", (cpf,))
        resultado = cursor.fetchone()

        if resultado:
            print("Erro: CPF já cadastrado.")
            return False

        # Insere o novo aluno
        cursor.execute("INSERT INTO alunos (nome, cpf, endereco) VALUES (?, ?, ?)", 
                      (nome, cpf, endereco))
        
        # Gera matrícula
        aluno_id = cursor.lastrowid
        matricula = f"MAT{aluno_id:04d}"
        cursor.execute("UPDATE alunos SET matricula = ? WHERE id = ?", (matricula, aluno_id))

        conexao.commit()
        print(f"✅ Aluno {nome} cadastrado com sucesso. Matrícula: {matricula}")
        return True

    except Exception as erro:
        print("Erro ao cadastrar aluno:", erro)
        if conexao:
            conexao.rollback()
        return False

    finally:
        if conexao:
            cursor.close()
            conexao.close()

def cadastrar_nota(nome, nota, disciplina, funcionario_id):
    """Função para cadastrar nota de aluno"""
    if not nome.strip():
        print("Erro: Nome não pode estar vazio.")
        return False

    if not (0 <= nota <= 10):
        print("Erro: Nota deve estar entre 0 e 10.")
        return False

    if not disciplina.strip():
        print("Erro: Disciplina não pode estar vazia.")
        return False

    try:
        conexao = sqlite3.connect('sistema_nota.db')
        cursor = conexao.cursor()

        # Verifica se o aluno existe
        cursor.execute("SELECT id FROM alunos WHERE nome = ?", (nome,))
        resultado = cursor.fetchone()

        if not resultado:
            print(f"Erro: Aluno '{nome}' não encontrado.")
            return False

        aluno_id = resultado[0]

        # Verifica se já existe nota para essa disciplina
        cursor.execute("""
            SELECT id FROM notas 
            WHERE aluno_id = ? AND disciplina = ?
        """, (aluno_id, disciplina))
        
        nota_existente = cursor.fetchone()
        
        if nota_existente:
            # Atualiza a nota existente
            cursor.execute("""
                UPDATE notas SET nota = ?, funcionario_id = ?
                WHERE id = ?
            """, (nota, funcionario_id, nota_existente[0]))
            print(f"✅ Nota de {disciplina} atualizada para {nome}: {nota}")
        else:
            # Insere nova nota
            cursor.execute("""
                INSERT INTO notas (aluno_id, disciplina, nota, funcionario_id)
                VALUES (?, ?, ?, ?)
            """, (aluno_id, disciplina, nota, funcionario_id))
            print(f"✅ Nota de {disciplina} cadastrada para {nome}: {nota}")

        conexao.commit()
        return True

    except Exception as erro:
        print("Erro ao cadastrar nota:", erro)
        if conexao:
            conexao.rollback()
        return False

    finally:
        if conexao:
            cursor.close()
            conexao.close()
