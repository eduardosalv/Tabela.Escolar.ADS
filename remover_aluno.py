#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3

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

def remover_aluno_por_id(aluno_id):
    """Remove um aluno específico por ID"""
    conn = conectar_db()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        
        # Verifica se o aluno existe
        cursor.execute("SELECT nome, matricula, cpf FROM alunos WHERE id = ?", (aluno_id,))
        aluno = cursor.fetchone()
        
        if not aluno:
            print(f"❌ Aluno com ID {aluno_id} não encontrado.")
            return False
        
        nome, matricula, cpf = aluno
        
        # Verifica se o aluno tem notas
        cursor.execute("SELECT COUNT(*) FROM notas WHERE aluno_id = ?", (aluno_id,))
        total_notas = cursor.fetchone()[0]
        
        print(f"\n📋 INFORMAÇÕES DO ALUNO:")
        print(f"Nome: {nome}")
        print(f"Matrícula: {matricula}")
        print(f"CPF: {cpf}")
        
        if total_notas > 0:
            print(f"⚠️ ATENÇÃO: Este aluno possui {total_notas} nota(s) cadastrada(s).")
            print("Todas as notas serão removidas junto com o aluno.")
        
        # Confirma remoção
        confirmacao = input(f"\n❌ Confirma a remoção do aluno {nome}? (s/n): ").lower()
        if confirmacao in ['s', 'sim', 'y', 'yes']:
            # Remove notas primeiro (devido à foreign key)
            cursor.execute("DELETE FROM notas WHERE aluno_id = ?", (aluno_id,))
            notas_removidas = cursor.rowcount
            
            # Remove o aluno
            cursor.execute("DELETE FROM alunos WHERE id = ?", (aluno_id,))
            aluno_removido = cursor.rowcount
            
            conn.commit()
            
            if aluno_removido > 0:
                print(f"✅ Aluno {nome} removido com sucesso!")
                if notas_removidas > 0:
                    print(f"📝 {notas_removidas} nota(s) também foram removida(s).")
                return True
            else:
                print("❌ Erro ao remover aluno.")
                return False
        else:
            print("❌ Operação cancelada.")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao remover aluno: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def remover_aluno_por_nome(nome_busca):
    """Remove um aluno específico por nome"""
    conn = conectar_db()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        
        # Busca alunos com nome similar
        cursor.execute("SELECT id, nome, matricula, cpf FROM alunos WHERE nome LIKE ?", (f"%{nome_busca}%",))
        alunos = cursor.fetchall()
        
        if not alunos:
            print(f"❌ Nenhum aluno encontrado com o nome '{nome_busca}'.")
            return False
        
        if len(alunos) == 1:
            # Apenas um aluno encontrado
            aluno_id, nome, matricula, cpf = alunos[0]
            return remover_aluno_por_id(aluno_id)
        else:
            # Múltiplos alunos encontrados
            print(f"\n🔍 Múltiplos alunos encontrados com '{nome_busca}':")
            print("="*60)
            print(f"{'ID':<4} {'Nome':<20} {'Matrícula':<12} {'CPF':<15}")
            print("-"*60)
            for aluno in alunos:
                print(f"{aluno[0]:<4} {aluno[1]:<20} {aluno[2]:<12} {aluno[3]:<15}")
            print("="*60)
            
            try:
                aluno_id = int(input("\nDigite o ID do aluno a ser removido: "))
                return remover_aluno_por_id(aluno_id)
            except ValueError:
                print("❌ ID inválido.")
                return False
                
    except Exception as e:
        print(f"❌ Erro ao buscar aluno: {e}")
        return False
    finally:
        conn.close()

def remover_aluno_por_cpf(cpf):
    """Remove um aluno específico por CPF"""
    conn = conectar_db()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        
        # Busca aluno por CPF
        cursor.execute("SELECT id, nome, matricula FROM alunos WHERE cpf = ?", (cpf,))
        aluno = cursor.fetchone()
        
        if not aluno:
            print(f"❌ Nenhum aluno encontrado com o CPF '{cpf}'.")
            return False
        
        aluno_id, nome, matricula = aluno
        return remover_aluno_por_id(aluno_id)
        
    except Exception as e:
        print(f"❌ Erro ao buscar aluno por CPF: {e}")
        return False
    finally:
        conn.close()

def menu_remocao():
    """Menu para remoção de alunos"""
    while True:
        print("\n" + "="*50)
        print("🗑️ SISTEMA DE REMOÇÃO DE ALUNOS")
        print("="*50)
        print("1. 📚 Listar todos os alunos")
        print("2. 🔍 Remover por ID")
        print("3. 🔍 Remover por nome")
        print("4. 🔍 Remover por CPF")
        print("0. 🚪 Voltar")
        print("="*50)
        
        opcao = input("Escolha uma opção: ").strip()
        
        if opcao == "1":
            mostrar_alunos()
        elif opcao == "2":
            try:
                aluno_id = int(input("Digite o ID do aluno: "))
                remover_aluno_por_id(aluno_id)
            except ValueError:
                print("❌ ID inválido.")
        elif opcao == "3":
            nome = input("Digite o nome do aluno: ").strip()
            if nome:
                remover_aluno_por_nome(nome)
            else:
                print("❌ Nome não pode estar vazio.")
        elif opcao == "4":
            cpf = input("Digite o CPF do aluno: ").strip()
            if cpf:
                remover_aluno_por_cpf(cpf)
            else:
                print("❌ CPF não pode estar vazio.")
        elif opcao == "0":
            print("👋 Voltando ao menu principal...")
            break
        else:
            print("❌ Opção inválida. Tente novamente.")

def main():
    """Função principal"""
    print("🗑️ SISTEMA DE REMOÇÃO DE ALUNOS")
    print("="*50)
    print("⚠️ ATENÇÃO: Esta operação é irreversível!")
    print("Todas as notas do aluno também serão removidas.")
    print("="*50)
    
    menu_remocao()

if __name__ == "__main__":
    main() 