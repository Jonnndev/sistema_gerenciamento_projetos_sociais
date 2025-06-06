import tkinter as tk
from tkinter import ttk, messagebox
from database.gerenciador_bd import GerenciadorBancoDados
from interface.janela_login import JanelaLogin
from interface.janela_principal import JanelaPrincipal
from interface.janela_relatorios import JanelaRelatorios

class SistemaProjetoSocial:
    def __init__(self):
        self.gerenciador_bd = GerenciadorBancoDados()
        self.usuario_logado = None
        self.janela_principal_obj = None
        
    def iniciar_sistema(self):
        """Inicia o sistema com a tela de login"""
        self.gerenciador_bd.inicializar_banco()
        janela_login = JanelaLogin(self)
        
    def fazer_login(self, nome_usuario):
        """Processa o login do usuário"""
        if nome_usuario.strip():
            self.usuario_logado = nome_usuario
            return True
        return False
    
    def abrir_janela_principal(self):
        """Abre a janela principal do sistema"""
        self.janela_principal_obj = JanelaPrincipal(self)
    
    def abrir_janela_relatorios(self):
        """Abre a janela de relatórios"""
        janela_relatorios = JanelaRelatorios(self)
    
    def obter_gerenciador_bd(self):
        """Retorna o gerenciador de banco de dados"""
        return self.gerenciador_bd
    
    def obter_usuario_logado(self):
        """Retorna o usuário logado"""
        return self.usuario_logado

if __name__ == "__main__":
    sistema = SistemaProjetoSocial()
    sistema.iniciar_sistema()