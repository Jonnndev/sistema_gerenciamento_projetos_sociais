-- Script SQL para criação do banco de dados do Sistema de Projeto Social

-- Criação da tabela de beneficiários
CREATE TABLE IF NOT EXISTS beneficiarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    cpf TEXT UNIQUE NOT NULL,
    telefone TEXT,
    endereco TEXT,
    data_cadastro TEXT DEFAULT CURRENT_TIMESTAMP,
    ativo INTEGER DEFAULT 1
);

-- Inserção de dados de exemplo (opcional)
INSERT OR IGNORE INTO beneficiarios (nome, cpf, telefone, endereco, data_cadastro, ativo) VALUES
('João da Silva', '123.456.789-01', '(11) 99999-1234', 'Rua das Flores, 123 - Centro', '2024-01-15 10:30:00', 1),
('Maria dos Santos', '987.654.321-02', '(11) 88888-5678', 'Av. Brasil, 456 - Vila Nova', '2024-01-16 14:20:00', 1),
('Pedro Oliveira', '456.789.123-03', '(11) 77777-9012', 'Rua da Paz, 789 - Jardim América', '2024-01-17 09:15:00', 1);

-- Índices para melhor performance
CREATE INDEX IF NOT EXISTS idx_beneficiarios_cpf ON beneficiarios(cpf);
CREATE INDEX IF NOT EXISTS idx_beneficiarios_nome ON beneficiarios(nome);
CREATE INDEX IF NOT EXISTS idx_beneficiarios_ativo ON beneficiarios(ativo);

-- Comentários sobre a estrutura da tabela:
-- id: Chave primária auto-incrementada
-- nome: Nome completo do beneficiário (obrigatório)
-- cpf: CPF único do beneficiário (obrigatório e único)
-- telefone: Telefone de contato (opcional)
-- endereco: Endereço completo (opcional)
-- data_cadastro: Data e hora do cadastro (automático)
-- ativo: Flag para exclusão lógica (1=ativo, 0=removido)