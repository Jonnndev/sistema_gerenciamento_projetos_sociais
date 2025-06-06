import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class JanelaRelatorios:
    def __init__(self, sistema):
        self.sistema = sistema
        self.janela = tk.Toplevel()
        self.configurar_janela()
        self.criar_widgets()
        self.carregar_dados()
        
    def configurar_janela(self):
        """Configura as propriedades da janela"""
        self.janela.title("Relatórios - Sistema de Projeto Social")
        self.janela.geometry("800x600")
        self.janela.configure(bg='#f0f0f0')
        
        # Centralizar a janela
        self.janela.update_idletasks()
        x = (self.janela.winfo_screenwidth() // 2) - (800 // 2)
        y = (self.janela.winfo_screenheight() // 2) - (600 // 2)
        self.janela.geometry(f"800x600+{x}+{y}")
        
        # Configurar para não ser redimensionável
        self.janela.resizable(True, True)
    
    def criar_widgets(self):
        """Cria todos os widgets da interface"""
        # Frame do título
        frame_titulo = tk.Frame(self.janela, bg='#34495e', height=60)
        frame_titulo.pack(fill='x')
        frame_titulo.pack_propagate(False)
        
        titulo = tk.Label(
            frame_titulo,
            text="Relatórios do Sistema",
            font=("Arial", 18, "bold"),
            bg='#34495e',
            fg='white'
        )
        titulo.pack(expand=True)
        
        # Frame principal
        frame_principal = tk.Frame(self.janela, bg='#f0f0f0')
        frame_principal.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Notebook para abas
        self.notebook = ttk.Notebook(frame_principal)
        self.notebook.pack(fill='both', expand=True)
        
        # Criar abas
        self.criar_aba_estatisticas()
        self.criar_aba_lista_completa()
        self.criar_aba_informacoes()
        
        # Frame dos botões
        frame_botoes = tk.Frame(frame_principal, bg='#f0f0f0')
        frame_botoes.pack(fill='x', pady=(10, 0))
        
        # Botões
        self.criar_botoes(frame_botoes)
    
    def criar_aba_estatisticas(self):
        """Cria a aba de estatísticas"""
        frame_stats = tk.Frame(self.notebook, bg='#f0f0f0')
        self.notebook.add(frame_stats, text="Estatísticas")
        
        # Título da seção
        titulo_stats = tk.Label(
            frame_stats,
            text="Estatísticas Gerais",
            font=("Arial", 16, "bold"),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        titulo_stats.pack(pady=(20, 30))
        
        # Frame para os cards de estatísticas
        frame_cards = tk.Frame(frame_stats, bg='#f0f0f0')
        frame_cards.pack(expand=True, fill='both', padx=20)
        
        # Configurar grid
        frame_cards.grid_rowconfigure(0, weight=1)
        frame_cards.grid_rowconfigure(1, weight=1)
        frame_cards.grid_columnconfigure(0, weight=1)
        frame_cards.grid_columnconfigure(1, weight=1)
        
        # Cards de estatísticas
        self.card_total_ativos = self.criar_card_estatistica(
            frame_cards, "Beneficiários Ativos", "0", "#27ae60", 0, 0
        )
        
        self.card_total_geral = self.criar_card_estatistica(
            frame_cards, "Total Geral", "0", "#3498db", 0, 1
        )
        
        self.card_cadastros_hoje = self.criar_card_estatistica(
            frame_cards, "Cadastros Hoje", "0", "#f39c12", 1, 0
        )
        
        self.card_removidos = self.criar_card_estatistica(
            frame_cards, "Removidos", "0", "#e74c3c", 1, 1
        )
    
    def criar_card_estatistica(self, frame_pai, titulo, valor, cor, linha, coluna):
        """Cria um card de estatística"""
        frame_card = tk.Frame(frame_pai, bg=cor, relief='raised', bd=2)
        frame_card.grid(row=linha, column=coluna, padx=10, pady=10, sticky='nsew')
        
        # Título
        label_titulo = tk.Label(
            frame_card,
            text=titulo,
            font=("Arial", 12, "bold"),
            bg=cor,
            fg='white'
        )
        label_titulo.pack(pady=(20, 5))
        
        # Valor
        label_valor = tk.Label(
            frame_card,
            text=valor,
            font=("Arial", 24, "bold"),
            bg=cor,
            fg='white'
        )
        label_valor.pack(pady=(5, 20))
        
        return label_valor
    
    def criar_aba_lista_completa(self):
        """Cria a aba com lista completa de beneficiários"""
        frame_lista = tk.Frame(self.notebook, bg='#f0f0f0')
        self.notebook.add(frame_lista, text="Lista Completa")
        
        # Título
        titulo_lista = tk.Label(
            frame_lista,
            text="Lista Completa de Beneficiários",
            font=("Arial", 16, "bold"),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        titulo_lista.pack(pady=(20, 10))
        
        # Frame para a tabela
        frame_tabela = tk.Frame(frame_lista, bg='#f0f0f0')
        frame_tabela.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Treeview
        colunas = ('ID', 'Nome', 'CPF', 'Telefone', 'Data Cadastro')
        
        self.tree_relatorio = ttk.Treeview(frame_tabela, columns=colunas, show='headings', height=15)
        
        # Configurar cabeçalhos
        for col in colunas:
            self.tree_relatorio.heading(col, text=col)
        
        # Configurar larguras
        larguras = [50, 250, 120, 120, 150]
        for i, col in enumerate(colunas):
            self.tree_relatorio.column(col, width=larguras[i], minwidth=50)
        
        # Scrollbars
        scrollbar_v2 = ttk.Scrollbar(frame_tabela, orient="vertical", command=self.tree_relatorio.yview)
        scrollbar_h2 = ttk.Scrollbar(frame_tabela, orient="horizontal", command=self.tree_relatorio.xview)
        
        self.tree_relatorio.configure(yscrollcommand=scrollbar_v2.set, xscrollcommand=scrollbar_h2.set)
        
        # Posicionamento
        self.tree_relatorio.grid(row=0, column=0, sticky='nsew')
        scrollbar_v2.grid(row=0, column=1, sticky='ns')
        scrollbar_h2.grid(row=1, column=0, sticky='ew')
        
        # Configurar expansão
        frame_tabela.grid_rowconfigure(0, weight=1)
        frame_tabela.grid_columnconfigure(0, weight=1)
    
    def criar_aba_informacoes(self):
        """Cria a aba de informações do sistema"""
        frame_info = tk.Frame(self.notebook, bg='#f0f0f0')
        self.notebook.add(frame_info, text="Informações")
        
        # Título
        titulo_info = tk.Label(
            frame_info,
            text="Informações do Sistema",
            font=("Arial", 16, "bold"),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        titulo_info.pack(pady=(20, 30))
        
        # Frame para informações
        frame_detalhes = tk.Frame(frame_info, bg='white', relief='raised', bd=2)
        frame_detalhes.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Informações do sistema
        info_texto = f"""
        Sistema de Gerenciamento de Projeto Social
        
        Versão: 1.0
        Desenvolvido em: Python 3.x
        Interface: Tkinter
        Banco de Dados: SQLite
        
        Usuário Logado: {self.sistema.obter_usuario_logado()}
        Data/Hora Atual: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
        
        Funcionalidades:
        • Cadastro de beneficiários
        • Edição de dados
        • Remoção de registros
        • Relatórios estatísticos
        • Listagem completa
        
        Desenvolvido para auxiliar no gerenciamento
        eficiente de projetos sociais.
        """
        
        label_info = tk.Label(
            frame_detalhes,
            text=info_texto,
            font=("Arial", 11),
            bg='white',
            fg='#2c3e50',
            justify='left',
            anchor='nw'
        )
        label_info.pack(fill='both', expand=True, padx=20, pady=20)
    
    def criar_botoes(self, frame_pai):
        """Cria os botões da janela"""
        # Botão Atualizar
        botao_atualizar = tk.Button(
            frame_pai,
            text="Atualizar Dados",
            font=("Arial", 11, "bold"),
            bg='#3498db',
            fg='white',
            width=15,
            height=2,
            relief='flat',
            cursor='hand2',
            command=self.carregar_dados
        )
        botao_atualizar.pack(side='left', padx=(0, 10))
        
        # Botão Fechar
        botao_fechar = tk.Button(
            frame_pai,
            text="Fechar",
            font=("Arial", 11),
            bg='#95a5a6',
            fg='white',
            width=15,
            height=2,
            relief='flat',
            cursor='hand2',
            command=self.fechar
        )
        botao_fechar.pack(side='left')
    
    def carregar_dados(self):
        """Carrega os dados para os relatórios"""
        try:
            gerenciador = self.sistema.obter_gerenciador_bd()
            
            # Carregar estatísticas
            stats = gerenciador.obter_estatisticas()
            if stats:
                self.card_total_ativos.configure(text=str(stats['total_ativos']))
                self.card_total_geral.configure(text=str(stats['total_geral']))
                self.card_cadastros_hoje.configure(text=str(stats['cadastros_hoje']))
                self.card_removidos.configure(text=str(stats['total_removidos']))
            
            # Carregar lista completa
            self.carregar_lista_completa()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar dados: {str(e)}")
    
    def carregar_lista_completa(self):
        """Carrega a lista completa de beneficiários"""
        # Limpar dados existentes
        for item in self.tree_relatorio.get_children():
            self.tree_relatorio.delete(item)
        
        # Buscar beneficiários
        gerenciador = self.sistema.obter_gerenciador_bd()
        beneficiarios = gerenciador.listar_beneficiarios()
        
        # Inserir na treeview
        for beneficiario in beneficiarios:
            data_cadastro = beneficiario[5][:16] if beneficiario[5] else ""
            
            self.tree_relatorio.insert('', 'end', values=(
                beneficiario[0],  # ID
                beneficiario[1],  # Nome
                beneficiario[2],  # CPF
                beneficiario[3] or "Não informado",  # Telefone
                data_cadastro     # Data Cadastro
            ))
    
    def fechar(self):
        """Fecha a janela de relatórios"""
        self.janela.destroy()