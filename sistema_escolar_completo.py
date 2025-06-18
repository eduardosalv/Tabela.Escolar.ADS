import sqlite3
from datetime import datetime
import os

def limpar_tela():
    """Limpa a tela do terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')

def conectar():
    """Conecta ao banco de dados SQLite"""
    try:
        conexao = sqlite3.connect('escola.db')
        return conexao
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

def conectar_db():
    """Alias para conectar() - mantém compatibilidade"""
    return conectar()

def criar_tabelas():
    """Cria as tabelas necessárias se não existirem"""
    conexao = conectar()
    if not conexao:
        return
    
    cursor = conexao.cursor()
    
    try:
        # Habilita foreign keys
        cursor.execute("PRAGMA foreign_keys = ON")
        
        # Tabela de alunos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS alunos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                matricula TEXT UNIQUE NOT NULL,
                cpf TEXT UNIQUE NOT NULL,
                data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Tabela de notas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                aluno_id INTEGER NOT NULL,
                disciplina TEXT NOT NULL,
                nota REAL NOT NULL,
                funcionario_id INTEGER NOT NULL,
                data_atribuicao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (aluno_id) REFERENCES alunos (id) ON DELETE CASCADE
            )
        """)
        
        conexao.commit()
        print("✅ Tabelas criadas/verificadas com sucesso!")
        
    except Exception as e:
        print(f"Erro ao criar tabelas: {e}")
        conexao.rollback()
    finally:
        conexao.close()

def listar_alunos():
    """Retorna lista de todos os alunos"""
    conexao = conectar()
    if not conexao:
        return []
    
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT id, nome, matricula, cpf FROM alunos ORDER BY nome")
        return cursor.fetchall()
    except Exception as e:
        print(f"Erro ao listar alunos: {e}")
        return []
    finally:
        conexao.close()

def mostrar_alunos():
    """Exibe lista formatada de alunos"""
    alunos = listar_alunos()
    if not alunos:
        print("❌ Nenhum aluno cadastrado.")
        return
    
    print("\n👥 ALUNOS CADASTRADOS:")
    print("-" * 60)
    print(f"{'ID':<4} {'Nome':<25} {'Matrícula':<12} {'CPF':<14}")
    print("-" * 60)
    
    for aluno in alunos:
        print(f"{aluno[0]:<4} {aluno[1]:<25} {aluno[2]:<12} {aluno[3]:<14}")

def validar_cpf(cpf):
    """Valida formato do CPF"""
    # Remove caracteres não numéricos
    cpf = ''.join(filter(str.isdigit, cpf))
    
    if len(cpf) != 11:
        return False
    
    # Verifica se todos os dígitos são iguais
    if cpf == cpf[0] * 11:
        return False
    
    # Validação do primeiro dígito verificador
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    resto = soma % 11
    digito1 = 0 if resto < 2 else 11 - resto
    
    if int(cpf[9]) != digito1:
        return False
    
    # Validação do segundo dígito verificador
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    resto = soma % 11
    digito2 = 0 if resto < 2 else 11 - resto
    
    if int(cpf[10]) != digito2:
        return False
    
    return True

def cadastrar_novo_aluno():
    """Interface para cadastrar novo aluno"""
    print("\n👤 CADASTRAR NOVO ALUNO")
    print("="*40)
    
    nome = input("Digite o nome completo: ").strip()
    if not nome:
        print("❌ Nome é obrigatório.")
        return
    
    matricula = input("Digite a matrícula: ").strip()
    if not matricula:
        print("❌ Matrícula é obrigatória.")
        return
    
    cpf = input("Digite o CPF (apenas números): ").strip()
    if not cpf:
        print("❌ CPF é obrigatório.")
        return
    
    # Validações do CPF
    if not validar_cpf(cpf):
        print("❌ CPF inválido. Digite um CPF válido.")
        return
    
    conexao = conectar()
    if not conexao:
        return
    
    cursor = conexao.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO alunos (nome, matricula, cpf)
            VALUES (?, ?, ?)
        """, (nome, matricula, cpf))
        
        conexao.commit()
        print("✅ Aluno cadastrado com sucesso!")
        
    except sqlite3.IntegrityError:
        print("❌ Erro: Matrícula ou CPF já cadastrado.")
    except Exception as e:
        print(f"❌ Erro ao cadastrar aluno: {e}")
        conexao.rollback()
    finally:
        conexao.close()

def atribuir_nota(aluno_id, disciplina, nota, funcionario_id):
    """Atribui ou atualiza nota de um aluno"""
    conexao = conectar()
    if not conexao:
        print("Erro: Não foi possível conectar ao banco de dados.")
        return False
    
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
                UPDATE notas SET nota = ?, funcionario_id = ?, data_atribuicao = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (nota, funcionario_id, resultado[0]))
            print("📝 Nota atualizada com sucesso!")
        else:
            # Insere nova nota
            cursor.execute("""
                INSERT INTO notas (aluno_id, disciplina, nota, funcionario_id)
                VALUES (?, ?, ?, ?)
            """, (aluno_id, disciplina, nota, funcionario_id))
            print("✅ Nova nota adicionada com sucesso!")

        conexao.commit()
        return True

    except Exception as e:
        print("Erro ao atribuir nota:", e)
        conexao.rollback()
        return False

    finally:
        cursor.close()
        conexao.close()

def adicionar_nota():
    """Interface para adicionar nota"""
    print("\n📝 ADICIONAR NOTA")
    print("="*40)
    
    # Mostra alunos disponíveis
    alunos = listar_alunos()
    if not alunos:
        print("❌ Nenhum aluno cadastrado. Cadastre um aluno primeiro.")
        input("\nPressione ENTER para continuar...")
        return
    
    mostrar_alunos()
    
    # Seleciona aluno
    try:
        aluno_id = int(input("\nDigite o ID do aluno: "))
        aluno_encontrado = next((a for a in alunos if a[0] == aluno_id), None)
        if not aluno_encontrado:
            print("❌ ID de aluno inválido.")
            input("\nPressione ENTER para continuar...")
            return
    except ValueError:
        print("❌ Digite um número válido.")
        input("\nPressione ENTER para continuar...")
        return
    
    # Lista disciplinas
    disciplinas = [
        "Matemática", "Português", "História", "Geografia",
        "Ciências", "Inglês", "Artes", "Educação Física"
    ]
    
    print("\n📚 DISCIPLINAS DISPONÍVEIS:")
    for i, disciplina in enumerate(disciplinas, 1):
        print(f"{i}. {disciplina}")
    
    # Seleciona disciplina
    try:
        disciplina_num = int(input("\nDigite o número da disciplina: "))
        if 1 <= disciplina_num <= len(disciplinas):
            disciplina = disciplinas[disciplina_num - 1]
        else:
            print("❌ Número de disciplina inválido.")
            input("\nPressione ENTER para continuar...")
            return
    except ValueError:
        print("❌ Digite um número válido.")
        input("\nPressione ENTER para continuar...")
        return
    
    # Digita nota
    try:
        nota = float(input("Digite a nota (0 a 10): "))
        if not (0 <= nota <= 10):
            print("❌ Nota deve estar entre 0 e 10.")
            input("\nPressione ENTER para continuar...")
            return
    except ValueError:
        print("❌ Digite um número válido.")
        input("\nPressione ENTER para continuar...")
        return
    
    # Confirma e adiciona
    print(f"\n📋 RESUMO:")
    print(f"Aluno: {aluno_encontrado[1]} ({aluno_encontrado[2]})")
    print(f"Disciplina: {disciplina}")
    print(f"Nota: {nota}")
    
    confirmacao = input("\nConfirma a adição desta nota? (s/n): ").lower()
    if confirmacao in ['s', 'sim', 'y', 'yes']:
        try:
            if atribuir_nota(aluno_id, disciplina, nota, 1):  # ID do funcionário 1
                print("✅ Operação realizada com sucesso!")
            else:
                print("❌ Erro ao processar a nota.")
        except Exception as e:
            print(f"❌ Erro ao adicionar nota: {e}")
    else:
        print("❌ Operação cancelada.")
    
    input("\nPressione ENTER para continuar...")

def consultar_notas():
    """Consulta notas de um aluno específico"""
    print("\n🔍 CONSULTAR NOTAS")
    print("="*40)
    
    alunos = listar_alunos()
    if not alunos:
        print("❌ Nenhum aluno cadastrado.")
        return
    
    mostrar_alunos()
    
    try:
        aluno_id = int(input("\nDigite o ID do aluno: "))
        aluno_encontrado = next((a for a in alunos if a[0] == aluno_id), None)
        if not aluno_encontrado:
            print("❌ ID de aluno inválido.")
            return
    except ValueError:
        print("❌ Digite um número válido.")
        return
    
    conexao = conectar()
    if not conexao:
        return
    
    cursor = conexao.cursor()
    
    try:
        cursor.execute("""
            SELECT disciplina, nota, data_atribuicao
            FROM notas
            WHERE aluno_id = ?
            ORDER BY disciplina
        """, (aluno_id,))
        
        notas = cursor.fetchall()
        
        if notas:
            print(f"\n📊 NOTAS DE {aluno_encontrado[1].upper()}:")
            print("-" * 50)
            print(f"{'Disciplina':<15} {'Nota':<8} {'Data'}")
            print("-" * 50)
            
            for nota in notas:
                data = datetime.fromisoformat(nota[2]).strftime("%d/%m/%Y")
                print(f"{nota[0]:<15} {nota[1]:<8.1f} {data}")
            
            # Calcula média
            media = sum(n[1] for n in notas) / len(notas)
            print("-" * 50)
            print(f"MÉDIA GERAL: {media:.2f}")
        else:
            print(f"❌ Nenhuma nota encontrada para {aluno_encontrado[1]}.")
            
    except Exception as e:
        print(f"❌ Erro ao consultar notas: {e}")
    finally:
        conexao.close()

def ver_notas_detalhadas():
    """Mostra todas as notas de todos os alunos"""
    print("\n📋 NOTAS DETALHADAS")
    print("="*60)
    
    conexao = conectar()
    if not conexao:
        return
    
    cursor = conexao.cursor()
    
    try:
        cursor.execute("""
            SELECT a.nome, a.matricula, n.disciplina, n.nota, n.data_atribuicao
            FROM alunos a
            LEFT JOIN notas n ON a.id = n.aluno_id
            ORDER BY a.nome, n.disciplina
        """)
        
        resultados = cursor.fetchall()
        
        if not resultados:
            print("❌ Nenhum dado encontrado.")
            return
        
        aluno_atual = None
        for resultado in resultados:
            if resultado[0] != aluno_atual:
                if aluno_atual:
                    print("-" * 60)
                aluno_atual = resultado[0]
                print(f"\n👤 {aluno_atual} ({resultado[1]})")
                print(f"{'Disciplina':<15} {'Nota':<8} {'Data'}")
                print("-" * 40)
            
            if resultado[2]:  # Se tem nota
                data = datetime.fromisoformat(resultado[4]).strftime("%d/%m/%Y")
                print(f"{resultado[2]:<15} {resultado[3]:<8.1f} {data}")
            else:
                print("Nenhuma nota cadastrada")
                
    except Exception as e:
        print(f"❌ Erro ao buscar notas detalhadas: {e}")
    finally:
        conexao.close()

def estatisticas():
    """Mostra estatísticas do sistema"""
    print("\n📈 ESTATÍSTICAS")
    print("="*40)
    
    conexao = conectar()
    if not conexao:
        return
    
    cursor = conexao.cursor()
    
    try:
        # Total de alunos
        cursor.execute("SELECT COUNT(*) FROM alunos")
        total_alunos = cursor.fetchone()[0]
        
        # Total de notas
        cursor.execute("SELECT COUNT(*) FROM notas")
        total_notas = cursor.fetchone()[0]
        
        # Média geral
        cursor.execute("SELECT AVG(nota) FROM notas")
        media_geral = cursor.fetchone()[0]
        
        # Melhor nota
        cursor.execute("SELECT MAX(nota) FROM notas")
        melhor_nota = cursor.fetchone()[0]
        
        # Pior nota
        cursor.execute("SELECT MIN(nota) FROM notas")
        pior_nota = cursor.fetchone()[0]
        
        print(f"👥 Total de alunos: {total_alunos}")
        print(f"📝 Total de notas: {total_notas}")
        if media_geral:
            print(f"📊 Média geral: {media_geral:.2f}")
            print(f"🏆 Melhor nota: {melhor_nota}")
            print(f"📉 Pior nota: {pior_nota}")
        else:
            print("📊 Nenhuma nota cadastrada ainda.")
            
    except Exception as e:
        print(f"❌ Erro ao calcular estatísticas: {e}")
    finally:
        conexao.close()

def remover_aluno():
    """Interface para remover aluno"""
    print("\n🗑️ REMOVER ALUNO")
    print("="*40)
    
    # Mostra alunos disponíveis
    alunos = listar_alunos()
    if not alunos:
        print("❌ Nenhum aluno cadastrado.")
        input("\nPressione ENTER para continuar...")
        return
    
    mostrar_alunos()
    
    # Seleciona aluno
    try:
        aluno_id = int(input("\nDigite o ID do aluno a ser removido: "))
        aluno_encontrado = next((a for a in alunos if a[0] == aluno_id), None)
        if not aluno_encontrado:
            print("❌ ID de aluno inválido.")
            input("\nPressione ENTER para continuar...")
            return
    except ValueError:
        print("❌ Digite um número válido.")
        input("\nPressione ENTER para continuar...")
        return
    
    # Mostra informações do aluno
    print(f"\n📋 INFORMAÇÕES DO ALUNO:")
    print(f"Nome: {aluno_encontrado[1]}")
    print(f"Matrícula: {aluno_encontrado[2]}")
    print(f"CPF: {aluno_encontrado[3]}")
    
    # Verifica se o aluno tem notas
    conn = conectar_db()
    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM notas WHERE aluno_id = ?", (aluno_id,))
        total_notas = cursor.fetchone()[0]
        
        if total_notas > 0:
            print(f"⚠️ ATENÇÃO: Este aluno possui {total_notas} nota(s) cadastrada(s).")
            print("Todas as notas serão removidas junto com o aluno.")
        
        # Confirma remoção
        confirmacao = input(f"\n❌ Confirma a remoção do aluno {aluno_encontrado[1]}? (s/n): ").lower()
        if confirmacao in ['s', 'sim', 'y', 'yes']:
            # Remove notas primeiro (devido à foreign key)
            cursor.execute("DELETE FROM notas WHERE aluno_id = ?", (aluno_id,))
            notas_removidas = cursor.rowcount
            
            # Remove o aluno
            cursor.execute("DELETE FROM alunos WHERE id = ?", (aluno_id,))
            aluno_removido = cursor.rowcount
            
            conn.commit()
            
            if aluno_removido > 0:
                print(f"✅ Aluno removido com sucesso!")
                if notas_removidas > 0:
                    print(f"📝 {notas_removidas} nota(s) também foram removida(s).")
            else:
                print("❌ Erro ao remover aluno.")
        else:
            print("❌ Operação cancelada.")
            
    except Exception as e:
        print(f"❌ Erro ao remover aluno: {e}")
        conn.rollback()
    finally:
        conn.close()
    
    input("\nPressione ENTER para continuar...")

def menu_principal(funcionario_id):
    """Menu principal do sistema"""
    while True:
        limpar_tela()
        print("="*50)
        print("🎓 SISTEMA DE GESTÃO DE NOTAS ESCOLARES")
        print("="*50)
        print("1. 📚 Listar alunos")
        print("2. 👤 Cadastrar novo aluno")
        print("3. 📝 Adicionar nota")
        print("4. 🔍 Consultar notas")
        print("5. 📋 Ver notas detalhadas")
        print("6. 📈 Estatísticas")
        print("7. 🗑️ Remover aluno")
        print("0. 🚪 Sair")
        print("="*50)
        
        opcao = input("Escolha uma opção: ").strip()
        
        if opcao == "1":
            mostrar_alunos()
            input("\nPressione ENTER para continuar...")
        elif opcao == "2":
            cadastrar_novo_aluno()
            input("\nPressione ENTER para continuar...")
        elif opcao == "3":
            adicionar_nota()
        elif opcao == "4":
            consultar_notas()
            input("\nPressione ENTER para continuar...")
        elif opcao == "5":
            ver_notas_detalhadas()
            input("\nPressione ENTER para continuar...")
        elif opcao == "6":
            estatisticas()
            input("\nPressione ENTER para continuar...")
        elif opcao == "7":
            remover_aluno()
        elif opcao == "0":
            print("👋 Obrigado por usar o sistema!")
            break
        else:
            print("❌ Opção inválida. Tente novamente.")
            input("\nPressione ENTER para continuar...")

def main():
    """Função principal que inicia o sistema"""
    print("🎓 SISTEMA DE GESTÃO DE NOTAS ESCOLARES")
    print("Inicializando...")
    
    # Cria as tabelas se não existirem
    criar_tabelas()
    
    # Inicia o menu principal
    menu_principal(1)  # ID do funcionário 1

if __name__ == "__main__":
    main() 