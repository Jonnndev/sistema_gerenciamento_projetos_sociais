import tkinter as tk
from tkinter import ttk, messagebox
from interface.formulario_beneficiario import FormularioBeneficiario

class JanelaPrincipal:
    def __init__(self, sistema):
        self.sistema = sistema
        self.janela = tk.Tk()
        self.configurar_janela()
        self.criar_widgets()
        self.atualizar_lista()
        self.janela.mainloop()
    
    def configurar_janela(self):
        """Configura as propriedades da janela"""
        self.janela.title(f"Sistema de Projeto Social - Usuário: {self.sistema.obter_usuario_logado()}")
        self.janela.geometry("900x600")
        self.janela.configure(bg='#f0f0f0')
        
        # Centralizar a janela
        self.janela.update_idletasks()
        x = (self.janela.winfo_screenwidth() // 2) - (900 // 2)
        y = (self.janela.winfo_screenheight() // 2) - (600 // 2)
        self.janela.geometry(f"900x600+{x}+{y}")
    
    def criar_widgets(self):
        """Cria todos os widgets da interface"""
        # Frame do título
        frame_titulo = tk.Frame(self.janela, bg='#2c3e50', height=60)
        frame_titulo.pack(fill='x')
        frame_titulo.pack_propagate(False)
        
        titulo = tk.Label(
            frame_titulo,
            text="Gerenciamento de Beneficiários",
            font=("Arial", 18, "bold"),
            bg='#2c3e50',
            fg='white'
        )
        titulo.pack(expand=True)
        
        # Frame principal
        frame_principal = tk.Frame(self.janela, bg='#f0f0f0')
        frame_principal.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Frame dos botões
        frame_botoes = tk.Frame(frame_principal, bg='#f0f0f0')
        frame_botoes.pack(fill='x', pady=(0, 10))
        
        # Botões de ação
        self.criar_botoes(frame_botoes)
        
        # Frame da lista
        frame_lista = tk.Frame(frame_principal, bg='#f0f0f0')
        frame_lista.pack(fill='both', expand=True)
        
        # Treeview para lista de beneficiários
        self.criar_treeview(frame_lista)
    
    def criar_botoes(self, frame_pai):
        """Cria os botões de ação"""
        botoes_config = [
            ("Cadastrar", "#27ae60", self.cadastrar_beneficiario),
            ("Editar", "#f39c12", self.editar_beneficiario),
            ("Remover", "#e74c3c", self.remover_beneficiario),
            ("Atualizar Lista", "#3498db", self.atualizar_lista),
            ("Relatórios", "#9b59b6", self.abrir_relatorios),
            ("Sair", "#95a5a6", self.sair)
        ]
        
        for i, (texto, cor, comando) in enumerate(botoes_config):
            botao = tk.Button(
                frame_pai,
                text=texto,
                font=("Arial", 10, "bold"),
                bg=cor,
                fg='white',
                width=12,
                height=2,
                relief='flat',
                cursor='hand2',
                command=comando
            )
            botao.grid(row=0, column=i, padx=5)
    
    def criar_treeview(self, frame_pai):
        """Cria a tabela de beneficiários"""
        # Frame para o Treeview e scrollbar
        frame_tree = tk.Frame(frame_pai, bg='#f0f0f0')
        frame_tree.pack(fill='both', expand=True)
        
        # Colunas
        colunas = ('ID', 'Nome', 'CPF', 'Telefone', 'Endereço', 'Data Cadastro')
        
        self.tree = ttk.Treeview(frame_tree, columns=colunas, show='headings', height=15)
        
        # Configurar cabeçalhos
        for col in colunas:
            self.tree.heading(col, text=col)
            
        # Configurar larguras das colunas
        larguras = [50, 200, 120, 100, 200, 130]
        for i, col in enumerate(colunas):
            self.tree.column(col, width=larguras[i], minwidth=50)
        
        # Scrollbars
        scrollbar_v = ttk.Scrollbar(frame_tree, orient="vertical", command=self.tree.yview)
        scrollbar_h = ttk.Scrollbar(frame_tree, orient="horizontal", command=self.tree.xview)
        
        self.tree.configure(yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set)
        
        # Posicionamento
        self.tree.grid(row=0, column=0, sticky='nsew')
        scrollbar_v.grid(row=0, column=1, sticky='ns')
        scrollbar_h.grid(row=1, column=0, sticky='ew')
        
        # Configurar expansão
        frame_tree.grid_rowconfigure(0, weight=1)
        frame_tree.grid_columnconfigure(0, weight=1)
        
        # Bind para duplo clique
        self.tree.bind('<Double-1>', lambda e: self.editar_beneficiario())
    
    def cadastrar_beneficiario(self):
        """Abre formulário para cadastrar novo beneficiário"""
        FormularioBeneficiario(self, self.sistema.obter_gerenciador_bd())
    
    def editar_beneficiario(self):
        """Abre formulário para editar beneficiário selecionado"""
        item_selecionado = self.tree.selection()
        
        if not item_selecionado:
            messagebox.showwarning("Aviso", "Selecione um beneficiário para editar!")
            return
        
        # Obter dados do item selecionado
        valores = self.tree.item(item_selecionado[0], 'values')
        id_beneficiario = valores[0]
        
        # Buscar dados completos no banco
        gerenciador = self.sistema.obter_gerenciador_bd()
        dados = gerenciador.buscar_beneficiario_por_id(id_beneficiario)
        
        if dados:
            FormularioBeneficiario(self, gerenciador, dados)
        else:
            messagebox.showerror("Erro", "Beneficiário não encontrado!")
    
    def remover_beneficiario(self):
        """Remove o beneficiário selecionado"""
        item_selecionado = self.tree.selection()
        
        if not item_selecionado:
            messagebox.showwarning("Aviso", "Selecione um beneficiário para remover!")
            return
        
        # Obter dados do item selecionado
        valores = self.tree.item(item_selecionado[0], 'values')
        id_beneficiario = valores[0]
        nome = valores[1]
        
        # Confirmar remoção
        resposta = messagebox.askyesno(
            "Confirmar Remoção",
            f"Tem certeza que deseja remover o beneficiário:\n{nome}?"
        )
        
        if resposta:
            gerenciador = self.sistema.obter_gerenciador_bd()
            if gerenciador.remover_beneficiario(id_beneficiario):
                messagebox.showinfo("Sucesso", "Beneficiário removido com sucesso!")
                self.atualizar_lista()
            else:
                messagebox.showerror("Erro", "Erro ao remover beneficiário!")
    
    def atualizar_lista(self):
        """Atualiza a lista de beneficiários"""
        # Limpar itens existentes
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Buscar beneficiários
        gerenciador = self.sistema.obter_gerenciador_bd()
        beneficiarios = gerenciador.listar_beneficiarios()
        
        # Inserir na treeview
        for beneficiario in beneficiarios:
            # Formatar data
            data_cadastro = beneficiario[5][:16] if beneficiario[5] else ""
            
            self.tree.insert('', 'end', values=(
                beneficiario[0],  # ID
                beneficiario[1],  # Nome
                beneficiario[2],  # CPF
                beneficiario[3],  # Telefone
                beneficiario[4],  # Endereço
                data_cadastro     # Data Cadastro
            ))
    
    def abrir_relatorios(self):
        """Abre a janela de relatórios"""
        self.sistema.abrir_janela_relatorios()
    
    def sair(self):
        """Fecha a aplicação"""
        resposta = messagebox.askyesno("Sair", "Tem certeza que deseja sair do sistema?")
        if resposta:
            self.janela.quit()
            self.janela.destroy()