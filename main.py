import sqlite3
from backend import consultar_alunos, atribuir_nota
from cadastro import cadastrar_aluno
from login import login_funcionario

def conectar_db():
    """Conecta ao banco de dados SQLite"""
    try:
        return sqlite3.connect('sistema_nota.db')
    except Exception as e:
        print(f"Erro ao conectar ao banco: {e}")
        return None

def listar_alunos():
    """Lista todos os alunos cadastrados"""
    conn = conectar_db()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT id, nome, matricula, cpf FROM alunos ORDER BY nome')
        alunos = cursor.fetchall()
        return alunos
    except Exception as e:
        print(f"Erro ao listar alunos: {e}")
        return []
    finally:
        conn.close()

def mostrar_alunos():
    """Mostra a lista de alunos de forma organizada"""
    alunos = listar_alunos()
    if not alunos:
        print("❌ Nenhum aluno cadastrado.")
        return
    
    print("\n" + "="*60)
    print("📚 LISTA DE ALUNOS CADASTRADOS")
    print("="*60)
    print(f"{'ID':<4} {'Nome':<20} {'Matrícula':<12} {'CPF':<15}")
    print("-"*60)
    for aluno in alunos:
        print(f"{aluno[0]:<4} {aluno[1]:<20} {aluno[2]:<12} {aluno[3]:<15}")
    print("="*60)

def cadastrar_novo_aluno():
    """Interface para cadastrar novo aluno"""
    print("\n🎓 CADASTRO DE NOVO ALUNO")
    print("="*40)
    
    nome = input("Nome completo: ").strip()
    if not nome:
        print("❌ Nome é obrigatório.")
        return
    
    cpf = input("CPF: ").strip()
    if not cpf:
        print("❌ CPF é obrigatório.")
        return
    
    endereco = input("Endereço: ").strip()
    if not endereco:
        print("❌ Endereço é obrigatório.")
        return
    
    try:
        if cadastrar_aluno(nome, cpf, endereco):
            print("✅ Aluno cadastrado com sucesso!")
        else:
            print("❌ Erro ao cadastrar aluno.")
    except Exception as e:
        print(f"❌ Erro: {e}")

def remover_aluno():
    """Interface para remover aluno"""
    print("\n🗑️ REMOVER ALUNO")
    print("="*40)
    
    # Mostra alunos disponíveis
    alunos = listar_alunos()
    if not alunos:
        print("❌ Nenhum aluno cadastrado.")
        return
    
    mostrar_alunos()
    
    # Seleciona aluno
    try:
        aluno_id = int(input("\nDigite o ID do aluno a ser removido: "))
        aluno_encontrado = next((a for a in alunos if a[0] == aluno_id), None)
        if not aluno_encontrado:
            print("❌ ID de aluno inválido.")
            return
    except ValueError:
        print("❌ Digite um número válido.")
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

def adicionar_nota():
    """Interface para adicionar nota"""
    print("\n📝 ADICIONAR NOTA")
    print("="*40)
    
    # Mostra alunos disponíveis
    alunos = listar_alunos()
    if not alunos:
        print("❌ Nenhum aluno cadastrado. Cadastre um aluno primeiro.")
        return
    
    mostrar_alunos()
    
    # Seleciona aluno
    try:
        aluno_id = int(input("\nDigite o ID do aluno: "))
        aluno_encontrado = next((a for a in alunos if a[0] == aluno_id), None)
        if not aluno_encontrado:
            print("❌ ID de aluno inválido.")
            return
    except ValueError:
        print("❌ Digite um número válido.")
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
            return
    except ValueError:
        print("❌ Digite um número válido.")
        return
    
    # Digita nota
    try:
        nota = float(input("Digite a nota (0 a 10): "))
        if not (0 <= nota <= 10):
            print("❌ Nota deve estar entre 0 e 10.")
            return
    except ValueError:
        print("❌ Digite um número válido.")
        return
    
    # Confirma e adiciona
    print(f"\n📋 RESUMO:")
    print(f"Aluno: {aluno_encontrado[1]} ({aluno_encontrado[2]})")
    print(f"Disciplina: {disciplina}")
    print(f"Nota: {nota}")
    
    confirmacao = input("\nConfirma a adição desta nota? (s/n): ").lower()
    if confirmacao in ['s', 'sim', 'y', 'yes']:
        try:
            atribuir_nota(aluno_id, disciplina, nota, 1)  # ID do funcionário 1
            print("✅ Nota adicionada com sucesso!")
        except Exception as e:
            print(f"❌ Erro ao adicionar nota: {e}")
    else:
        print("❌ Operação cancelada.")

def consultar_notas():
    """Consulta notas de alunos"""
    print("\n🔍 CONSULTA DE NOTAS")
    print("="*40)
    
    nome_busca = input("Digite o nome do aluno (ou deixe vazio para todos): ").strip()
    
    try:
        resultados = consultar_alunos(nome_busca)
        
        if not resultados:
            print("❌ Nenhum aluno encontrado.")
            return
        
        print(f"\n📊 RESULTADOS DA CONSULTA")
        print("="*80)
        print(f"{'Matrícula':<12} {'Nome':<20} {'Mat.':<6} {'Port.':<6} {'Hist.':<6} {'Geo.':<6} {'Ciên.':<6} {'Ing.':<6} {'Artes':<6} {'Ed.Fís.':<6}")
        print("-"*80)
        
        for aluno in resultados:
            print(f"{aluno['matricula']:<12} {aluno['nome']:<20} "
                  f"{aluno['matematica'] or '-':<6} {aluno['portugues'] or '-':<6} "
                  f"{aluno['historia'] or '-':<6} {aluno['geografia'] or '-':<6} "
                  f"{aluno['ciencias'] or '-':<6} {aluno['ingles'] or '-':<6} "
                  f"{aluno['artes'] or '-':<6} {aluno['educacao_fisica'] or '-':<6}")
        
        print("="*80)
        
    except Exception as e:
        print(f"❌ Erro ao consultar notas: {e}")

def ver_notas_detalhadas():
    """Mostra notas detalhadas de um aluno específico"""
    print("\n📋 NOTAS DETALHADAS")
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
        
        conn = conectar_db()
        if not conn:
            return
        
        cursor = conn.cursor()
        cursor.execute("""
            SELECT disciplina, nota, f.nome as funcionario
            FROM notas n
            LEFT JOIN funcionario f ON n.funcionario_id = f.id
            WHERE n.aluno_id = ?
            ORDER BY disciplina
        """, (aluno_id,))
        notas = cursor.fetchall()
        conn.close()
        
        print(f"\n📊 NOTAS DO ALUNO: {aluno_encontrado[1]} ({aluno_encontrado[2]})")
        print("="*50)
        
        if notas:
            total_notas = 0
            for disciplina, nota, funcionario in notas:
                print(f"📚 {disciplina}: {nota:.1f} (Lançada por: {funcionario or 'N/A'})")
                total_notas += nota
            
            media = total_notas / len(notas)
            print(f"\n📈 MÉDIA GERAL: {media:.2f}")
            print(f"📊 TOTAL DE DISCIPLINAS: {len(notas)}")
        else:
            print("Nenhuma nota cadastrada.")
        
        print("="*50)
        
    except ValueError:
        print("❌ Digite um número válido.")
    except Exception as e:
        print(f"❌ Erro ao buscar notas: {e}")

def estatisticas():
    """Mostra estatísticas do sistema"""
    print("\n📈 ESTATÍSTICAS DO SISTEMA")
    print("="*40)
    
    conn = conectar_db()
    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        
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
        
        # Notas por disciplina
        cursor.execute("""
            SELECT disciplina, COUNT(*), AVG(nota)
            FROM notas
            GROUP BY disciplina
            ORDER BY disciplina
        """)
        notas_por_disciplina = cursor.fetchall()
        
        print(f"👥 Total de alunos: {total_alunos}")
        print(f"📝 Total de notas: {total_notas}")
        if media_geral:
            print(f"📊 Média geral: {media_geral:.2f}")
            print(f"🏆 Melhor nota: {melhor_nota}")
            print(f"📉 Pior nota: {pior_nota}")
        
        if notas_por_disciplina:
            print(f"\n📚 NOTAS POR DISCIPLINA:")
            print("-"*40)
            for disciplina, quantidade, media in notas_por_disciplina:
                print(f"{disciplina}: {quantidade} notas, média {media:.2f}")
        
    except Exception as e:
        print(f"❌ Erro ao gerar estatísticas: {e}")
    finally:
        conn.close()

def menu_principal(funcionario_id):
    """Menu principal do sistema"""
    while True:
        print("\n" + "="*50)
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
        elif opcao == "2":
            cadastrar_novo_aluno()
        elif opcao == "3":
            adicionar_nota()
        elif opcao == "4":
            consultar_notas()
        elif opcao == "5":
            ver_notas_detalhadas()
        elif opcao == "6":
            estatisticas()
        elif opcao == "7":
            remover_aluno()
        elif opcao == "0":
            print("👋 Obrigado por usar o sistema!")
            break
        else:
            print("❌ Opção inválida. Tente novamente.")

def main():
    """Função principal do sistema"""
    print("🎓 SISTEMA DE GESTÃO DE NOTAS ESCOLARES")
    print("="*50)
    
    # Login do funcionário
    funcionario_id = login_funcionario()
    
    if not funcionario_id:
        print("❌ Acesso negado. CPF ou senha incorretos.")
        return
    
    print("✅ Login realizado com sucesso!")
    
    # Menu principal
    menu_principal(funcionario_id)

if __name__ == "__main__":
    main()
