import tkinter as tk
from tkinter import ttk, messagebox

class JanelaLogin:
    def __init__(self, sistema):
        self.sistema = sistema
        self.janela = tk.Tk()
        self.configurar_janela()
        self.criar_widgets()
        self.janela.mainloop()
    
    def configurar_janela(self):
        """Configura as propriedades da janela"""
        self.janela.title("Sistema de Projeto Social - Login")
        self.janela.geometry("400x300")
        self.janela.resizable(False, False)
        
        # Centralizar a janela
        self.janela.update_idletasks()
        x = (self.janela.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.janela.winfo_screenheight() // 2) - (300 // 2)
        self.janela.geometry(f"400x300+{x}+{y}")
        
        # Definir cor de fundo
        self.janela.configure(bg='#f0f0f0')
    
    def criar_widgets(self):
        """Cria todos os widgets da interface"""
        # Frame principal
        frame_principal = tk.Frame(self.janela, bg='#f0f0f0')
        frame_principal.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Título
        titulo = tk.Label(
            frame_principal,
            text="Sistema de Gerenciamento\nProjeto Social",
            font=("Arial", 16, "bold"),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        titulo.pack(pady=(0, 30))
        
        # Frame do formulário
        frame_form = tk.Frame(frame_principal, bg='#f0f0f0')
        frame_form.pack(expand=True)
        
        # Label e campo de usuário
        tk.Label(
            frame_form,
            text="Nome de Usuário:",
            font=("Arial", 12),
            bg='#f0f0f0'
        ).pack(pady=(0, 5))
        
        self.entrada_usuario = tk.Entry(
            frame_form,
            font=("Arial", 12),
            width=25,
            relief='solid',
            bd=1
        )
        self.entrada_usuario.pack(pady=(0, 20))
        self.entrada_usuario.focus()
        
        # Botão de login
        self.botao_login = tk.Button(
            frame_form,
            text="Entrar",
            font=("Arial", 12, "bold"),
            bg='#3498db',
            fg='white',
            width=20,
            height=2,
            relief='flat',
            cursor='hand2',
            command=self.processar_login
        )
        self.botao_login.pack(pady=(0, 10))
        
        # Botão de sair
        botao_sair = tk.Button(
            frame_form,
            text="Sair",
            font=("Arial", 10),
            bg='#e74c3c',
            fg='white',
            width=20,
            relief='flat',
            cursor='hand2',
            command=self.sair
        )
        botao_sair.pack()
        
        # Bind para Enter
        self.janela.bind('<Return>', lambda e: self.processar_login())
    
    def processar_login(self):
        """Processa o login do usuário"""
        nome_usuario = self.entrada_usuario.get().strip()
        
        if not nome_usuario:
            messagebox.showerror("Erro", "Por favor, digite seu nome de usuário!")
            self.entrada_usuario.focus()
            return
        
        if self.sistema.fazer_login(nome_usuario):
            messagebox.showinfo("Sucesso", f"Bem-vindo(a), {nome_usuario}!")
            self.janela.destroy()
            self.sistema.abrir_janela_principal()
        else:
            messagebox.showerror("Erro", "Erro ao fazer login!")
    
    def sair(self):
        """Fecha a aplicação"""
        self.janela.quit()
        self.janela.destroy()