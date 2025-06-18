import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from functools import partial

class SistemaEscolar:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Escolar")
        self.root.geometry("900x600")
        
        # Criar banco de dados se não existir
        self.criar_banco_dados()
        
        # Tela de login
        self.tela_login()
    
    def criar_banco_dados(self):
        conn = sqlite3.connect('sistema_nota.db')
        cursor = conn.cursor()
        
        # Tabela de funcionários
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS funcionario (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                cpf TEXT UNIQUE NOT NULL,
                senha TEXT NOT NULL
            )
        """)
        
        # Tabela de alunos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS alunos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                cpf TEXT UNIQUE NOT NULL,
                endereco TEXT NOT NULL,
                matricula TEXT UNIQUE
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
                FOREIGN KEY (aluno_id) REFERENCES alunos(id),
                FOREIGN KEY (funcionario_id) REFERENCES funcionario(id)
            )
        """)
        
        # Inserir funcionário padrão se não existir
        cursor.execute("""
            INSERT OR IGNORE INTO funcionario (nome, cpf, senha)
            VALUES ('Administrador', '12345678900', 'admin123')
        """)
        
        conn.commit()
        conn.close()
    
    def tela_login(self):
        """Tela de login do sistema"""
        self.limpar_tela()
        
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(expand=True)
        
        ttk.Label(frame, text="Login do Funcionário", font=('Arial', 16)).grid(row=0, column=0, columnspan=2, pady=10)
        
        ttk.Label(frame, text="CPF:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.cpf_entry = ttk.Entry(frame)
        self.cpf_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(frame, text="Senha:").grid(row=2, column=0, sticky='e', padx=5, pady=5)
        self.senha_entry = ttk.Entry(frame, show="*")
        self.senha_entry.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Button(frame, text="Entrar", command=self.verificar_login).grid(row=3, column=0, columnspan=2, pady=10)
    
    def verificar_login(self):
        cpf = self.cpf_entry.get()
        senha = self.senha_entry.get()
        
        if cpf == "12345678900" and senha == "admin123":
            self.funcionario_id = 1
            self.nome_funcionario = "Administrador"
            self.menu_principal()
        else:
            try:
                conn = sqlite3.connect('sistema_nota.db')
                cursor = conn.cursor()
                
                cursor.execute("SELECT id, nome FROM funcionario WHERE cpf = ? AND senha = ?", (cpf, senha))
                resultado = cursor.fetchone()
                
                if resultado:
                    self.funcionario_id, self.nome_funcionario = resultado
                    self.menu_principal()
                else:
                    messagebox.showerror("Erro", "CPF ou senha incorretos!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao fazer login: {e}")
            finally:
                conn.close()
    
    def menu_principal(self):
        """Menu principal após login"""
        self.limpar_tela()
        
        # Barra de menu
        menubar = tk.Menu(self.root)
        
        # Menu Alunos
        menu_alunos = tk.Menu(menubar, tearoff=0)
        menu_alunos.add_command(label="Cadastrar Aluno", command=self.tela_cadastrar_aluno)
        menu_alunos.add_command(label="Listar/Remover Alunos", command=self.tela_listar_alunos)
        menubar.add_cascade(label="Alunos", menu=menu_alunos)
        
        # Menu Notas
        menu_notas = tk.Menu(menubar, tearoff=0)
        menu_notas.add_command(label="Atribuir Notas", command=self.tela_atribuir_notas)
        menu_notas.add_command(label="Consultar Notas", command=self.tela_consultar_notas)
        menubar.add_cascade(label="Notas", menu=menu_notas)
        
        # Menu Sair
        menubar.add_command(label="Sair", command=self.root.quit)
        
        self.root.config(menu=menubar)
        
        # Área de boas-vindas
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(expand=True)
        
        ttk.Label(frame, text=f"Bem-vindo(a), {self.nome_funcionario}!", font=('Arial', 16)).pack(pady=20)
        ttk.Label(frame, text="Sistema de Gestão Escolar", font=('Arial', 12)).pack(pady=10)
        
        # Botões rápidos
        ttk.Button(frame, text="Cadastrar Aluno", command=self.tela_cadastrar_aluno).pack(fill='x', pady=5)
        ttk.Button(frame, text="Atribuir Notas", command=self.tela_atribuir_notas).pack(fill='x', pady=5)
    
    def tela_cadastrar_aluno(self):
        """Tela para cadastrar novo aluno"""
        self.limpar_tela()
        
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(expand=True)
        
        ttk.Label(frame, text="Cadastrar Novo Aluno", font=('Arial', 16)).grid(row=0, column=0, columnspan=2, pady=10)
        
        # Campos do formulário
        ttk.Label(frame, text="Nome:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.nome_aluno_entry = ttk.Entry(frame, width=40)
        self.nome_aluno_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(frame, text="CPF:").grid(row=2, column=0, sticky='e', padx=5, pady=5)
        self.cpf_aluno_entry = ttk.Entry(frame, width=40)
        self.cpf_aluno_entry.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(frame, text="Endereço:").grid(row=3, column=0, sticky='e', padx=5, pady=5)
        self.endereco_aluno_entry = ttk.Entry(frame, width=40)
        self.endereco_aluno_entry.grid(row=3, column=1, padx=5, pady=5)
        
        ttk.Label(frame, text="Matrícula:").grid(row=4, column=0, sticky='e', padx=5, pady=5)
        self.matricula_aluno_entry = ttk.Entry(frame, width=40)
        self.matricula_aluno_entry.grid(row=4, column=1, padx=5, pady=5)
        
        # Botões
        ttk.Button(frame, text="Cadastrar", command=self.cadastrar_aluno).grid(row=5, column=0, columnspan=2, pady=10)
        ttk.Button(frame, text="Voltar", command=self.menu_principal).grid(row=6, column=0, columnspan=2, pady=5)
    
    def cadastrar_aluno(self):
        """Cadastra um novo aluno no banco de dados"""
        nome = self.nome_aluno_entry.get().strip()
        cpf = self.cpf_aluno_entry.get().strip()
        endereco = self.endereco_aluno_entry.get().strip()
        matricula = self.matricula_aluno_entry.get().strip()
        
        if not nome or not cpf or not endereco or not matricula:
            messagebox.showerror("Erro", "Todos os campos são obrigatórios!")
            return
        
        try:
            conn = sqlite3.connect('sistema_nota.db')
            cursor = conn.cursor()
            
            # Verifica se CPF ou matrícula já existem
            cursor.execute("SELECT id FROM alunos WHERE cpf = ? OR matricula = ?", (cpf, matricula))
            if cursor.fetchone():
                messagebox.showerror("Erro", "CPF ou matrícula já cadastrados!")
                return
            
            # Insere o novo aluno
            cursor.execute("""
                INSERT INTO alunos (nome, cpf, endereco, matricula)
                VALUES (?, ?, ?, ?)
            """, (nome, cpf, endereco, matricula))
            
            conn.commit()
            messagebox.showinfo("Sucesso", "Aluno cadastrado com sucesso!")
            
            # Limpa os campos
            self.nome_aluno_entry.delete(0, tk.END)
            self.cpf_aluno_entry.delete(0, tk.END)
            self.endereco_aluno_entry.delete(0, tk.END)
            self.matricula_aluno_entry.delete(0, tk.END)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao cadastrar aluno: {e}")
        finally:
            conn.close()
    
    def tela_listar_alunos(self):
        """Tela para listar e remover alunos"""
        self.limpar_tela()
        
        frame = ttk.Frame(self.root, padding=10)
        frame.pack(expand=True, fill='both')
        
        ttk.Label(frame, text="Lista de Alunos", font=('Arial', 16)).pack(pady=10)
        
        # Treeview para exibir alunos
        columns = ('id', 'nome', 'cpf', 'matricula', 'endereco')
        self.tree_alunos = ttk.Treeview(frame, columns=columns, show='headings')
        
        # Configurar colunas
        self.tree_alunos.heading('id', text='ID')
        self.tree_alunos.heading('nome', text='Nome')
        self.tree_alunos.heading('cpf', text='CPF')
        self.tree_alunos.heading('matricula', text='Matrícula')
        self.tree_alunos.heading('endereco', text='Endereço')
        
        # Ajustar largura das colunas
        self.tree_alunos.column('id', width=50, anchor='center')
        self.tree_alunos.column('nome', width=200)
        self.tree_alunos.column('cpf', width=120)
        self.tree_alunos.column('matricula', width=100)
        self.tree_alunos.column('endereco', width=250)
        
        # Barra de rolagem
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.tree_alunos.yview)
        self.tree_alunos.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree_alunos.pack(expand=True, fill='both')
        
        # Botões
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Atualizar Lista", command=self.carregar_alunos).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Remover Selecionado", command=self.remover_aluno).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Voltar", command=self.menu_principal).pack(side=tk.LEFT, padx=5)
        
        # Carregar alunos
        self.carregar_alunos()
    
    def carregar_alunos(self):
        """Carrega a lista de alunos do banco de dados"""
        try:
            conn = sqlite3.connect('sistema_nota.db')
            cursor = conn.cursor()
            
            # Limpa a treeview
            for item in self.tree_alunos.get_children():
                self.tree_alunos.delete(item)
            
            # Busca alunos
            cursor.execute("SELECT id, nome, cpf, matricula, endereco FROM alunos ORDER BY nome")
            alunos = cursor.fetchall()
            
            # Insere na treeview
            for aluno in alunos:
                self.tree_alunos.insert('', tk.END, values=aluno)
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar alunos: {e}")
        finally:
            conn.close()
    
    def remover_aluno(self):
        """Remove o aluno selecionado"""
        selected_item = self.tree_alunos.selection()
        if not selected_item:
            messagebox.showwarning("Aviso", "Selecione um aluno para remover!")
            return
        
        aluno_id = self.tree_alunos.item(selected_item)['values'][0]
        aluno_nome = self.tree_alunos.item(selected_item)['values'][1]
        
        if messagebox.askyesno("Confirmar", f"Tem certeza que deseja remover o aluno {aluno_nome}?"):
            try:
                conn = sqlite3.connect('sistema_nota.db')
                cursor = conn.cursor()
                
                # Remove primeiro as notas associadas ao aluno
                cursor.execute("DELETE FROM notas WHERE aluno_id = ?", (aluno_id,))
                
                # Remove o aluno
                cursor.execute("DELETE FROM alunos WHERE id = ?", (aluno_id,))
                
                conn.commit()
                messagebox.showinfo("Sucesso", "Aluno removido com sucesso!")
                self.carregar_alunos()
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao remover aluno: {e}")
            finally:
                conn.close()
    
    def tela_atribuir_notas(self):
        """Tela para atribuir notas aos alunos"""
        self.limpar_tela()
        
        frame = ttk.Frame(self.root, padding=10)
        frame.pack(expand=True, fill='both')
        
        ttk.Label(frame, text="Atribuir Notas", font=('Arial', 16)).pack(pady=10)
        
        # Frame para seleção de aluno
        selecao_frame = ttk.Frame(frame)
        selecao_frame.pack(fill='x', pady=5)
        
        ttk.Label(selecao_frame, text="Selecione o Aluno:").pack(side=tk.LEFT, padx=5)
        
        self.aluno_var = tk.StringVar()
        self.aluno_combobox = ttk.Combobox(selecao_frame, textvariable=self.aluno_var, state='readonly')
        self.aluno_combobox.pack(side=tk.LEFT, padx=5, fill='x', expand=True)
        
        # Carregar alunos no combobox
        self.carregar_alunos_combobox()
        
        # Frame para disciplina e nota
        nota_frame = ttk.Frame(frame)
        nota_frame.pack(fill='x', pady=5)
        
        ttk.Label(nota_frame, text="Disciplina:").pack(side=tk.LEFT, padx=5)
        
        self.disciplina_var = tk.StringVar()
        disciplinas = ['Matemática', 'Português', 'História', 'Geografia', 'Ciências', 'Inglês', 'Artes', 'Educação Física']
        self.disciplina_combobox = ttk.Combobox(nota_frame, textvariable=self.disciplina_var, values=disciplinas)
        self.disciplina_combobox.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(nota_frame, text="Nota (0-10):").pack(side=tk.LEFT, padx=5)
        
        self.nota_entry = ttk.Entry(nota_frame, width=5)
        self.nota_entry.pack(side=tk.LEFT, padx=5)
        
        # Botão para atribuir nota
        ttk.Button(frame, text="Atribuir Nota", command=self.atribuir_nota).pack(pady=10)
        
        # Treeview para exibir notas do aluno selecionado
        columns = ('disciplina', 'nota')
        self.tree_notas = ttk.Treeview(frame, columns=columns, show='headings')
        
        self.tree_notas.heading('disciplina', text='Disciplina')
        self.tree_notas.heading('nota', text='Nota')
        
        self.tree_notas.column('disciplina', width=200)
        self.tree_notas.column('nota', width=100, anchor='center')
        
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.tree_notas.yview)
        self.tree_notas.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree_notas.pack(expand=True, fill='both')
        
        # Botão para atualizar notas
        ttk.Button(frame, text="Atualizar Notas", command=self.carregar_notas_aluno).pack(pady=5)
        
        # Botão para voltar
        ttk.Button(frame, text="Voltar", command=self.menu_principal).pack(pady=5)
        
        # Configurar evento de seleção no combobox
        self.aluno_combobox.bind('<<ComboboxSelected>>', lambda e: self.carregar_notas_aluno())
    
    def carregar_alunos_combobox(self):
        """Carrega a lista de alunos no combobox"""
        try:
            conn = sqlite3.connect('sistema_nota.db')
            cursor = conn.cursor()
            
            cursor.execute("SELECT id, nome, matricula FROM alunos ORDER BY nome")
            alunos = cursor.fetchall()
            
            # Formata como "Nome (Matrícula)"
            alunos_formatados = [f"{aluno[1]} ({aluno[2]})" for aluno in alunos]
            self.aluno_combobox['values'] = alunos_formatados
            
            # Armazena os IDs dos alunos na mesma ordem
            self.alunos_ids = [aluno[0] for aluno in alunos]
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar alunos: {e}")
        finally:
            conn.close()
    
    def carregar_notas_aluno(self):
        """Carrega as notas do aluno selecionado"""
        selected_index = self.aluno_combobox.current()
        if selected_index == -1:
            return
            
        aluno_id = self.alunos_ids[selected_index]
        
        try:
            conn = sqlite3.connect('sistema_nota.db')
            cursor = conn.cursor()
            
            # Limpa a treeview
            for item in self.tree_notas.get_children():
                self.tree_notas.delete(item)
            
            # Busca notas do aluno
            cursor.execute("""
                SELECT disciplina, nota FROM notas 
                WHERE aluno_id = ? 
                ORDER BY disciplina
            """, (aluno_id,))
            
            notas = cursor.fetchall()
            
            # Insere na treeview
            for nota in notas:
                self.tree_notas.insert('', tk.END, values=nota)
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar notas: {e}")
        finally:
            conn.close()
    
    def atribuir_nota(self):
        """Atribui uma nota ao aluno selecionado"""
        selected_index = self.aluno_combobox.current()
        if selected_index == -1:
            messagebox.showwarning("Aviso", "Selecione um aluno!")
            return
            
        aluno_id = self.alunos_ids[selected_index]
        disciplina = self.disciplina_var.get().strip()
        nota_str = self.nota_entry.get().strip()
        
        if not disciplina:
            messagebox.showwarning("Aviso", "Selecione uma disciplina!")
            return
            
        if not nota_str:
            messagebox.showwarning("Aviso", "Digite uma nota!")
            return
            
        try:
            nota = float(nota_str)
            if not (0 <= nota <= 10):
                messagebox.showwarning("Aviso", "A nota deve estar entre 0 e 10!")
                return
        except ValueError:
            messagebox.showwarning("Aviso", "Digite um valor numérico para a nota!")
            return
            
        try:
            conn = sqlite3.connect('sistema_nota.db')
            cursor = conn.cursor()
            
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
                """, (nota, self.funcionario_id, nota_existente[0]))
                mensagem = "Nota atualizada com sucesso!"
            else:
                # Insere nova nota
                cursor.execute("""
                    INSERT INTO notas (aluno_id, disciplina, nota, funcionario_id)
                    VALUES (?, ?, ?, ?)
                """, (aluno_id, disciplina, nota, self.funcionario_id))
                mensagem = "Nota atribuída com sucesso!"
            
            conn.commit()
            messagebox.showinfo("Sucesso", mensagem)
            
            # Limpa os campos e atualiza a lista
            self.disciplina_var.set('')
            self.nota_entry.delete(0, tk.END)
            self.carregar_notas_aluno()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atribuir nota: {e}")
        finally:
            conn.close()
    
    def tela_consultar_notas(self):
        """Tela para consultar notas de todos os alunos"""
        self.limpar_tela()
        
        frame = ttk.Frame(self.root, padding=10)
        frame.pack(expand=True, fill='both')
        
        ttk.Label(frame, text="Consultar Notas", font=('Arial', 16)).pack(pady=10)
        
        # Treeview para exibir notas
        columns = ['aluno', 'matricula', 'matematica', 'portugues', 'historia', 'geografia', 
                  'ciencias', 'ingles', 'artes', 'educacao_fisica']
        self.tree_consulta_notas = ttk.Treeview(frame, columns=columns, show='headings')
        
        # Configurar colunas
        self.tree_consulta_notas.heading('aluno', text='Aluno')
        self.tree_consulta_notas.heading('matricula', text='Matrícula')
        self.tree_consulta_notas.heading('matematica', text='Matemática')
        self.tree_consulta_notas.heading('portugues', text='Português')
        self.tree_consulta_notas.heading('historia', text='História')
        self.tree_consulta_notas.heading('geografia', text='Geografia')
        self.tree_consulta_notas.heading('ciencias', text='Ciências')
        self.tree_consulta_notas.heading('ingles', text='Inglês')
        self.tree_consulta_notas.heading('artes', text='Artes')
        self.tree_consulta_notas.heading('educacao_fisica', text='Educ. Física')
        
        # Ajustar largura das colunas
        for col in columns:
            self.tree_consulta_notas.column(col, width=80, anchor='center')
        self.tree_consulta_notas.column('aluno', width=150, anchor='w')
        self.tree_consulta_notas.column('matricula', width=100, anchor='center')
        
        # Barra de rolagem
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.tree_consulta_notas.yview)
        self.tree_consulta_notas.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree_consulta_notas.pack(expand=True, fill='both')
        
        # Botões
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Atualizar", command=self.carregar_consulta_notas).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Voltar", command=self.menu_principal).pack(side=tk.LEFT, padx=5)
        
        # Carregar notas
        self.carregar_consulta_notas()
    
    def carregar_consulta_notas(self):
        """Carrega a consulta de notas no formato pivot"""
        try:
            conn = sqlite3.connect('sistema_nota.db')
            cursor = conn.cursor()
            
            # Limpa a treeview
            for item in self.tree_consulta_notas.get_children():
                self.tree_consulta_notas.delete(item)
            
            # Consulta pivot de notas
            cursor.execute("""
                SELECT a.nome, a.matricula,
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
                GROUP BY a.id, a.nome, a.matricula
                ORDER BY a.nome
            """)
            
            notas = cursor.fetchall()
            
            # Insere na treeview
            for nota in notas:
                self.tree_consulta_notas.insert('', tk.END, values=nota)
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar notas: {e}")
        finally:
            conn.close()
    
    def limpar_tela(self):
        """Remove todos os widgets da tela principal"""
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaEscolar(root)
    root.mainloop()