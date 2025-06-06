import tkinter as tk
from tkinter import ttk, messagebox
import re

class FormularioBeneficiario:
    def __init__(self, janela_pai, gerenciador_bd, dados_beneficiario=None):
        self.janela_pai = janela_pai
        self.gerenciador_bd = gerenciador_bd
        self.dados_beneficiario = dados_beneficiario
        self.janela = tk.Toplevel(janela_pai.janela)
        self.configurar_janela()
        self.criar_widgets()
        self.preencher_dados()
        
    def configurar_janela(self):
        """Configura as propriedades da janela"""
        titulo = "Editar Beneficiário" if self.dados_beneficiario else "Cadastrar Beneficiário"
        self.janela.title(titulo)
        self.janela.geometry("500x400")
        self.janela.resizable(False, False)
        self.janela.configure(bg='#f0f0f0')
        
        # Centralizar em relação à janela pai
        self.janela.transient(self.janela_pai.janela)
        self.janela.grab_set()
        
        # Centralizar a janela
        self.janela.update_idletasks()
        x = (self.janela.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.janela.winfo_screenheight() // 2) - (400 // 2)
        self.janela.geometry(f"500x400+{x}+{y}")
    
    def criar_widgets(self):
        """Cria todos os widgets do formulário"""
        # Frame principal
        frame_principal = tk.Frame(self.janela, bg='#f0f0f0')
        frame_principal.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Título
        titulo_texto = "Editar Beneficiário" if self.dados_beneficiario else "Cadastrar Novo Beneficiário"
        titulo = tk.Label(
            frame_principal,
            text=titulo_texto,
            font=("Arial", 16, "bold"),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        titulo.pack(pady=(0, 20))
        
        # Frame do formulário
        frame_form = tk.Frame(frame_principal, bg='#f0f0f0')
        frame_form.pack(fill='both', expand=True)
        
        # Campos do formulário
        self.criar_campos(frame_form)
        
        # Frame dos botões
        frame_botoes = tk.Frame(frame_principal, bg='#f0f0f0')
        frame_botoes.pack(fill='x', pady=(20, 0))
        
        # Botões
        self.criar_botoes(frame_botoes)
    
    def criar_campos(self, frame_pai):
        """Cria os campos do formulário"""
        campos = [
            ("Nome Completo:", "entrada_nome"),
            ("CPF:", "entrada_cpf"),
            ("Telefone:", "entrada_telefone"),
            ("Endereço:", "entrada_endereco")
        ]
        
        for i, (label_texto, nome_var) in enumerate(campos):
            # Label
            label = tk.Label(
                frame_pai,
                text=label_texto,
                font=("Arial", 12),
                bg='#f0f0f0',
                anchor='w'
            )
            label.grid(row=i*2, column=0, sticky='w', pady=(10, 5))
            
            # Entry
            if nome_var == "entrada_endereco":
                # Campo de texto maior para endereço
                entrada = tk.Text(
                    frame_pai,
                    font=("Arial", 11),
                    width=50,
                    height=3,
                    relief='solid',
                    bd=1,
                    wrap='word'
                )
            else:
                entrada = tk.Entry(
                    frame_pai,
                    font=("Arial", 11),
                    width=50,
                    relief='solid',
                    bd=1
                )
            
            entrada.grid(row=i*2+1, column=0, sticky='ew', pady=(0, 5))
            setattr(self, nome_var, entrada)
            
            # Bind para formatação de CPF
            if nome_var == "entrada_cpf":
                entrada.bind('<KeyRelease>', self.formatar_cpf)
            elif nome_var == "entrada_telefone":
                entrada.bind('<KeyRelease>', self.formatar_telefone)
        
        # Configurar expansão da coluna
        frame_pai.grid_columnconfigure(0, weight=1)
        
        # Focar no primeiro campo
        self.entrada_nome.focus()
    
    def criar_botoes(self, frame_pai):
        """Cria os botões do formulário"""
        # Botão Salvar
        botao_salvar = tk.Button(
            frame_pai,
            text="Salvar",
            font=("Arial", 12, "bold"),
            bg='#27ae60',
            fg='white',
            width=15,
            height=2,
            relief='flat',
            cursor='hand2',
            command=self.salvar_beneficiario
        )
        botao_salvar.pack(side='left', padx=(0, 10))
        
        # Botão Cancelar
        botao_cancelar = tk.Button(
            frame_pai,
            text="Cancelar",
            font=("Arial", 12),
            bg='#e74c3c',
            fg='white',
            width=15,
            height=2,
            relief='flat',
            cursor='hand2',
            command=self.cancelar
        )
        botao_cancelar.pack(side='left')
        
        # Bind para Enter
        self.janela.bind('<Return>', lambda e: self.salvar_beneficiario())
        self.janela.bind('<Escape>', lambda e: self.cancelar())
    
    def preencher_dados(self):
        """Preenche os campos com dados existentes para edição"""
        if self.dados_beneficiario:
            self.entrada_nome.insert(0, self.dados_beneficiario[1])
            self.entrada_cpf.insert(0, self.dados_beneficiario[2])
            self.entrada_telefone.insert(0, self.dados_beneficiario[3] or "")
            self.entrada_endereco.insert('1.0', self.dados_beneficiario[4] or "")
    
    def formatar_cpf(self, evento):
        """Formata o CPF durante a digitação"""
        entrada = self.entrada_cpf
        texto = entrada.get().replace('.', '').replace('-', '')
        
        # Manter apenas números
        texto = re.sub(r'[^0-9]', '', texto)
        
        # Limitar a 11 dígitos
        if len(texto) > 11:
            texto = texto[:11]
        
        # Formatar CPF
        if len(texto) > 3:
            texto = texto[:3] + '.' + texto[3:]
        if len(texto) > 7:
            texto = texto[:7] + '.' + texto[7:]
        if len(texto) > 11:
            texto = texto[:11] + '-' + texto[11:]
        
        # Atualizar campo
        posicao_cursor = entrada.index(tk.INSERT)
        entrada.delete(0, tk.END)
        entrada.insert(0, texto)
        
        # Reposicionar cursor
        if posicao_cursor <= len(texto):
            entrada.icursor(posicao_cursor)
    
    def formatar_telefone(self, evento):
        """Formata o telefone durante a digitação"""
        entrada = self.entrada_telefone
        texto = entrada.get().replace('(', '').replace(')', '').replace('-', '').replace(' ', '')
        
        # Manter apenas números
        texto = re.sub(r'[^0-9]', '', texto)
        
        # Limitar a 11 dígitos
        if len(texto) > 11:
            texto = texto[:11]
        
        # Formatar telefone
        if len(texto) > 2:
            texto = '(' + texto[:2] + ') ' + texto[2:]
        if len(texto) > 9:
            texto = texto[:9] + '-' + texto[9:]
        
        # Atualizar campo
        posicao_cursor = entrada.index(tk.INSERT)
        entrada.delete(0, tk.END)
        entrada.insert(0, texto)
        
        # Reposicionar cursor
        if posicao_cursor <= len(texto):
            entrada.icursor(posicao_cursor)
    
    def validar_campos(self):
        """Valida os campos do formulário"""
        nome = self.entrada_nome.get().strip()
        cpf = self.entrada_cpf.get().strip()
        telefone = self.entrada_telefone.get().strip()
        endereco = self.entrada_endereco.get('1.0', tk.END).strip()
        
        if not nome:
            messagebox.showerror("Erro", "O nome é obrigatório!")
            self.entrada_nome.focus()
            return False
        
        if not cpf:
            messagebox.showerror("Erro", "O CPF é obrigatório!")
            self.entrada_cpf.focus()
            return False
        
        # Validar formato do CPF
        cpf_numeros = re.sub(r'[^0-9]', '', cpf)
        if len(cpf_numeros) != 11:
            messagebox.showerror("Erro", "CPF deve ter 11 dígitos!")
            self.entrada_cpf.focus()
            return False
        
        # Validar CPF (algoritmo básico)
        if not self.validar_cpf(cpf_numeros):
            messagebox.showerror("Erro", "CPF inválido!")
            self.entrada_cpf.focus()
            return False
        
        return True
    
    def validar_cpf(self, cpf):
        """Valida o CPF usando o algoritmo oficial"""
        # Remover CPFs inválidos conhecidos
        if cpf in ['00000000000', '11111111111', '22222222222', '33333333333',
                   '44444444444', '55555555555', '66666666666', '77777777777',
                   '88888888888', '99999999999']:
            return False
        
        # Calcular primeiro dígito verificador
        soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
        resto = soma % 11
        digito1 = 0 if resto < 2 else 11 - resto
        
        # Calcular segundo dígito verificador
        soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
        resto = soma % 11
        digito2 = 0 if resto < 2 else 11 - resto
        
        # Verificar se os dígitos estão corretos
        return cpf[9] == str(digito1) and cpf[10] == str(digito2)
    
    def salvar_beneficiario(self):
        """Salva o beneficiário no banco de dados"""
        if not self.validar_campos():
            return
        
        nome = self.entrada_nome.get().strip()
        cpf = self.entrada_cpf.get().strip()
        telefone = self.entrada_telefone.get().strip()
        endereco = self.entrada_endereco.get('1.0', tk.END).strip()
        
        try:
            if self.dados_beneficiario:
                # Editar beneficiário existente
                id_beneficiario = self.dados_beneficiario[0]
                resultado = self.gerenciador_bd.atualizar_beneficiario(
                    id_beneficiario, nome, cpf, telefone, endereco
                )
                
                if resultado is True:
                    messagebox.showinfo("Sucesso", "Beneficiário atualizado com sucesso!")
                    self.janela_pai.atualizar_lista()
                    self.janela.destroy()
                else:
                    messagebox.showerror("Erro", str(resultado))
            else:
                # Cadastrar novo beneficiário
                resultado = self.gerenciador_bd.inserir_beneficiario(
                    nome, cpf, telefone, endereco
                )
                
                if resultado is True:
                    messagebox.showinfo("Sucesso", "Beneficiário cadastrado com sucesso!")
                    self.janela_pai.atualizar_lista()
                    self.janela.destroy()
                else:
                    messagebox.showerror("Erro", str(resultado))
                    
        except Exception as e:
            messagebox.showerror("Erro", f"Erro inesperado: {str(e)}")
    
    def cancelar(self):
        """Cancela a operação e fecha a janela"""
        self.janela.destroy()