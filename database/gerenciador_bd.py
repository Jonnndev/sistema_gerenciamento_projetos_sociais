import sqlite3
from datetime import datetime
import os

class GerenciadorBancoDados:
    def __init__(self, nome_arquivo='projeto_social.db'):
        self.nome_arquivo = nome_arquivo
        self.conexao = None
    
    def conectar(self):
        """Estabelece conexão com o banco de dados"""
        try:
            self.conexao = sqlite3.connect(self.nome_arquivo)
            return True
        except sqlite3.Error as e:
            print(f"Erro ao conectar com o banco: {e}")
            return False
    
    def desconectar(self):
        """Fecha a conexão com o banco de dados"""
        if self.conexao:
            self.conexao.close()
    
    def inicializar_banco(self):
        """Cria as tabelas necessárias se não existirem"""
        if self.conectar():
            try:
                cursor = self.conexao.cursor()
                
                # Criar tabela de beneficiários
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS beneficiarios (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT NOT NULL,
                        cpf TEXT UNIQUE NOT NULL,
                        telefone TEXT,
                        endereco TEXT,
                        data_cadastro TEXT DEFAULT CURRENT_TIMESTAMP,
                        ativo INTEGER DEFAULT 1
                    )
                ''')
                
                self.conexao.commit()
                print("Banco de dados inicializado com sucesso!")
                
            except sqlite3.Error as e:
                print(f"Erro ao inicializar banco: {e}")
            finally:
                self.desconectar()
    
    def inserir_beneficiario(self, nome, cpf, telefone, endereco):
        """Insere um novo beneficiário no banco"""
        if self.conectar():
            try:
                cursor = self.conexao.cursor()
                data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                cursor.execute('''
                    INSERT INTO beneficiarios (nome, cpf, telefone, endereco, data_cadastro)
                    VALUES (?, ?, ?, ?, ?)
                ''', (nome, cpf, telefone, endereco, data_atual))
                
                self.conexao.commit()
                return True
                
            except sqlite3.IntegrityError:
                return "CPF já cadastrado no sistema!"
            except sqlite3.Error as e:
                return f"Erro ao inserir beneficiário: {e}"
            finally:
                self.desconectar()
        return False
    
    def listar_beneficiarios(self):
        """Lista todos os beneficiários ativos"""
        if self.conectar():
            try:
                cursor = self.conexao.cursor()
                cursor.execute('''
                    SELECT id, nome, cpf, telefone, endereco, data_cadastro 
                    FROM beneficiarios 
                    WHERE ativo = 1 
                    ORDER BY nome
                ''')
                
                resultados = cursor.fetchall()
                return resultados
                
            except sqlite3.Error as e:
                print(f"Erro ao listar beneficiários: {e}")
                return []
            finally:
                self.desconectar()
        return []
    
    def buscar_beneficiario_por_id(self, id_beneficiario):
        """Busca um beneficiário específico pelo ID"""
        if self.conectar():
            try:
                cursor = self.conexao.cursor()
                cursor.execute('''
                    SELECT id, nome, cpf, telefone, endereco, data_cadastro 
                    FROM beneficiarios 
                    WHERE id = ? AND ativo = 1
                ''', (id_beneficiario,))
                
                resultado = cursor.fetchone()
                return resultado
                
            except sqlite3.Error as e:
                print(f"Erro ao buscar beneficiário: {e}")
                return None
            finally:
                self.desconectar()
        return None
    
    def atualizar_beneficiario(self, id_beneficiario, nome, cpf, telefone, endereco):
        """Atualiza os dados de um beneficiário"""
        if self.conectar():
            try:
                cursor = self.conexao.cursor()
                cursor.execute('''
                    UPDATE beneficiarios 
                    SET nome = ?, cpf = ?, telefone = ?, endereco = ?
                    WHERE id = ? AND ativo = 1
                ''', (nome, cpf, telefone, endereco, id_beneficiario))
                
                self.conexao.commit()
                return cursor.rowcount > 0
                
            except sqlite3.IntegrityError:
                return "CPF já existe para outro beneficiário!"
            except sqlite3.Error as e:
                return f"Erro ao atualizar beneficiário: {e}"
            finally:
                self.desconectar()
        return False
    
    def remover_beneficiario(self, id_beneficiario):
        """Remove um beneficiário (marcação lógica)"""
        if self.conectar():
            try:
                cursor = self.conexao.cursor()
                cursor.execute('''
                    UPDATE beneficiarios 
                    SET ativo = 0 
                    WHERE id = ?
                ''', (id_beneficiario,))
                
                self.conexao.commit()
                return cursor.rowcount > 0
                
            except sqlite3.Error as e:
                print(f"Erro ao remover beneficiário: {e}")
                return False
            finally:
                self.desconectar()
        return False
    
    def obter_estatisticas(self):
        """Obtém estatísticas para relatórios"""
        if self.conectar():
            try:
                cursor = self.conexao.cursor()
                
                # Total de beneficiários ativos
                cursor.execute('SELECT COUNT(*) FROM beneficiarios WHERE ativo = 1')
                total_ativos = cursor.fetchone()[0]
                
                # Total de beneficiários removidos
                cursor.execute('SELECT COUNT(*) FROM beneficiarios WHERE ativo = 0')
                total_removidos = cursor.fetchone()[0]
                
                # Beneficiários cadastrados hoje
                hoje = datetime.now().strftime("%Y-%m-%d")
                cursor.execute('''
                    SELECT COUNT(*) FROM beneficiarios 
                    WHERE date(data_cadastro) = ? AND ativo = 1
                ''', (hoje,))
                cadastros_hoje = cursor.fetchone()[0]
                
                return {
                    'total_ativos': total_ativos,
                    'total_removidos': total_removidos,
                    'cadastros_hoje': cadastros_hoje,
                    'total_geral': total_ativos + total_removidos
                }
                
            except sqlite3.Error as e:
                print(f"Erro ao obter estatísticas: {e}")
                return None
            finally:
                self.desconectar()
        return None