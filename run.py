#!/usr/bin/env python3
"""
Script de inicialização do Sistema de Notas
Permite escolher entre interface gráfica e terminal
"""

import sys
import os

def main():
    print("🎓 Sistema de Cadastro e Consulta de Notas")
    print("=" * 50)
    print("Escolha uma opção:")
    print("1. Interface gráfica (recomendado)")
    print("2. Interface de terminal")
    print("3. Configurar banco de dados")
    print("0. Sair")
    
    while True:
        try:
            opcao = input("\nDigite sua opção: ").strip()
            
            if opcao == "1":
                print("\n🚀 Iniciando interface gráfica...")
                try:
                    import interface
                    print("✅ Interface gráfica iniciada com sucesso!")
                except ImportError as e:
                    print(f"❌ Erro ao importar interface: {e}")
                    print("💡 Execute: pip install -r requirements.txt")
                except Exception as e:
                    print(f"❌ Erro ao iniciar interface: {e}")
                break
                
            elif opcao == "2":
                print("\n🚀 Iniciando interface de terminal...")
                try:
                    import main
                    print("✅ Interface de terminal iniciada com sucesso!")
                except Exception as e:
                    print(f"❌ Erro ao iniciar interface de terminal: {e}")
                break
                
            elif opcao == "3":
                print("\n🔧 Configurando banco de dados...")
                try:
                    import setup_database
                    print("✅ Banco de dados configurado com sucesso!")
                except Exception as e:
                    print(f"❌ Erro ao configurar banco: {e}")
                break
                
            elif opcao == "0":
                print("👋 Saindo...")
                sys.exit(0)
                
            else:
                print("❌ Opção inválida. Digite 1, 2, 3 ou 0.")
                
        except KeyboardInterrupt:
            print("\n👋 Saindo...")
            sys.exit(0)
        except Exception as e:
            print(f"❌ Erro inesperado: {e}")

if __name__ == "__main__":
    main() 