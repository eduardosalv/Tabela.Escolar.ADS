import sqlite3
from backend import atribuir_nota

def listar_alunos():
    """Lista todos os alunos cadastrados"""
    try:
        conn = sqlite3.connect('sistema_nota.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, nome, matricula FROM alunos ORDER BY nome')
        alunos = cursor.fetchall()
        conn.close()
        
        print("\n=== ALUNOS CADASTRADOS ===")
        for aluno in alunos:
            print(f"ID: {aluno[0]} | Nome: {aluno[1]} | Matrícula: {aluno[2]}")
        print()
        return alunos
    except Exception as e:
        print(f"Erro ao listar alunos: {e}")
        return []

def listar_disciplinas():
    """Lista as disciplinas disponíveis"""
    disciplinas = [
        "Matemática",
        "Português", 
        "História",
        "Geografia",
        "Ciências",
        "Inglês",
        "Artes",
        "Educação Física"
    ]
    print("\n=== DISCIPLINAS DISPONÍVEIS ===")
    for i, disciplina in enumerate(disciplinas, 1):
        print(f"{i}. {disciplina}")
    print()
    return disciplinas

def adicionar_nota_interativo():
    """Interface interativa para adicionar notas"""
    print("🎓 SISTEMA DE ADIÇÃO DE NOTAS")
    print("=" * 40)
    
    # Lista alunos
    alunos = listar_alunos()
    if not alunos:
        print("❌ Nenhum aluno cadastrado. Cadastre um aluno primeiro.")
        return
    
    # Lista disciplinas
    disciplinas = listar_disciplinas()
    
    # Seleciona aluno
    while True:
        try:
            aluno_id = int(input("Digite o ID do aluno: "))
            aluno_encontrado = next((a for a in alunos if a[0] == aluno_id), None)
            if aluno_encontrado:
                print(f"✅ Aluno selecionado: {aluno_encontrado[1]} ({aluno_encontrado[2]})")
                break
            else:
                print("❌ ID de aluno inválido. Tente novamente.")
        except ValueError:
            print("❌ Digite um número válido.")
    
    # Seleciona disciplina
    while True:
        try:
            disciplina_num = int(input("Digite o número da disciplina: "))
            if 1 <= disciplina_num <= len(disciplinas):
                disciplina = disciplinas[disciplina_num - 1]
                print(f"✅ Disciplina selecionada: {disciplina}")
                break
            else:
                print("❌ Número de disciplina inválido. Tente novamente.")
        except ValueError:
            print("❌ Digite um número válido.")
    
    # Digita nota
    while True:
        try:
            nota = float(input("Digite a nota (0 a 10): "))
            if 0 <= nota <= 10:
                print(f"✅ Nota: {nota}")
                break
            else:
                print("❌ Nota deve estar entre 0 e 10.")
        except ValueError:
            print("❌ Digite um número válido.")
    
    # Confirma operação
    print(f"\n📝 RESUMO:")
    print(f"Aluno: {aluno_encontrado[1]}")
    print(f"Disciplina: {disciplina}")
    print(f"Nota: {nota}")
    
    confirmacao = input("\nConfirma a adição desta nota? (s/n): ").lower()
    if confirmacao in ['s', 'sim', 'y', 'yes']:
        # Adiciona a nota (usando ID do funcionário 1 como padrão)
        try:
            atribuir_nota(aluno_id, disciplina, nota, 1)
            print("✅ Nota adicionada com sucesso!")
        except Exception as e:
            print(f"❌ Erro ao adicionar nota: {e}")
    else:
        print("❌ Operação cancelada.")

def ver_notas_aluno():
    """Mostra as notas de um aluno específico"""
    alunos = listar_alunos()
    if not alunos:
        print("❌ Nenhum aluno cadastrado.")
        return
    
    try:
        aluno_id = int(input("Digite o ID do aluno para ver suas notas: "))
        aluno_encontrado = next((a for a in alunos if a[0] == aluno_id), None)
        if not aluno_encontrado:
            print("❌ ID de aluno inválido.")
            return
        
        conn = sqlite3.connect('sistema_nota.db')
        cursor = conn.cursor()
        cursor.execute("""
            SELECT disciplina, nota 
            FROM notas 
            WHERE aluno_id = ? 
            ORDER BY disciplina
        """, (aluno_id,))
        notas = cursor.fetchall()
        conn.close()
        
        print(f"\n📊 NOTAS DO ALUNO: {aluno_encontrado[1]} ({aluno_encontrado[2]})")
        print("=" * 50)
        if notas:
            for disciplina, nota in notas:
                print(f"{disciplina}: {nota}")
        else:
            print("Nenhuma nota cadastrada.")
        print()
        
    except ValueError:
        print("❌ Digite um número válido.")
    except Exception as e:
        print(f"❌ Erro ao buscar notas: {e}")

def menu_principal():
    """Menu principal do sistema"""
    while True:
        print("\n" + "=" * 40)
        print("🎓 SISTEMA DE GESTÃO DE NOTAS")
        print("=" * 40)
        print("1. Adicionar nota")
        print("2. Ver notas de um aluno")
        print("3. Listar alunos")
        print("4. Sair")
        print("=" * 40)
        
        opcao = input("Escolha uma opção: ").strip()
        
        if opcao == "1":
            adicionar_nota_interativo()
        elif opcao == "2":
            ver_notas_aluno()
        elif opcao == "3":
            listar_alunos()
        elif opcao == "4":
            print("👋 Até logo!")
            break
        else:
            print("❌ Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu_principal() 