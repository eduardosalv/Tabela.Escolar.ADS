from conexao import conectar

# Função para consultar alunos com suas notas e disciplinas
def consultar_alunos(nome):
    conexao = conectar()
    if not conexao:
        print("Erro: Não foi possível conectar ao banco de dados.")
        return []
    
    cursor = conexao.cursor()

    try:
        cursor.execute("""
            SELECT a.id, a.nome, a.matricula,
                MAX(CASE WHEN n.disciplina = 'Matemática' THEN n.nota END) AS matematica,
                MAX(CASE WHEN n.disciplina = 'Português' THEN n.nota END) AS portugues,
                MAX(CASE WHEN n.disciplina = 'História' THEN n.nota END) AS historia,
                MAX(CASE WHEN n.disciplina = 'Geografia' THEN n.nota END) AS geografia,
                MAX(CASE WHEN n.disciplina = 'Ciências' THEN n.nota END) AS ciencias,
                MAX(CASE WHEN n.disciplina = 'Inglês' THEN n.nota END) AS ingles,
                MAX(CASE WHEN n.disciplina = 'Artes' THEN n.nota END) AS artes,
                MAX(CASE WHEN n.disciplina = 'Educação Física' THEN n.nota END) AS educacao_fisica
            FROM alunos a
            LEFT JOIN notas n ON a.id = n.aluno_id
            WHERE a.nome LIKE ? OR ? = ''
            GROUP BY a.id, a.nome, a.matricula
            ORDER BY a.nome
        """, (f"%{nome}%", nome))

        # Buscar os resultados e converter para dicionários
        colunas = [desc[0] for desc in cursor.description]
        resultados = []
        for row in cursor.fetchall():
            resultados.append(dict(zip(colunas, row)))
        
        return resultados

    except Exception as e:
        print("Erro ao consultar alunos:", e)
        return []

    finally:
        cursor.close()
        conexao.close()


# Função para atribuir (ou atualizar) uma nota a um aluno
def atribuir_nota(aluno_id, disciplina, nota, funcionario_id):
    conexao = conectar()
    if not conexao:
        print("Erro: Não foi possível conectar ao banco de dados.")
        return
    
    cursor = conexao.cursor()

    try:
        # Verifica se já existe nota para essa disciplina
        cursor.execute("""
            SELECT id FROM notas
            WHERE aluno_id = ? AND disciplina = ?
        """, (aluno_id, disciplina))
        resultado = cursor.fetchone()

        if resultado:
            # Atualiza a nota existente
            cursor.execute("""
                UPDATE notas SET nota = ?, funcionario_id = ?
                WHERE id = ?
            """, (nota, funcionario_id, resultado[0]))
        else:
            # Insere nova nota
            cursor.execute("""
                INSERT INTO notas (aluno_id, disciplina, nota, funcionario_id)
                VALUES (?, ?, ?, ?)
            """, (aluno_id, disciplina, nota, funcionario_id))

        conexao.commit()

    except Exception as e:
        print("Erro ao atribuir nota:", e)
        conexao.rollback()

    finally:
        cursor.close()
        conexao.close()
