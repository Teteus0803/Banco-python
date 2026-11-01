Banco Python

Sistema bancário simples feito em Python com SQLite, rodando no terminal.
Projeto de estudo para praticar lógica de programação, funções e banco de dados SQL.

Funcionalidades

- Criar conta (nome, senha e pergunta de segurança)
- Login com ID e senha
- Recuperar senha respondendo a pergunta de segurança
- Ver saldo
- Depositar
- Sacar (com validação de saldo)
- Transferir para outra conta (valida se a conta existe, valor e saldo)
- Extrato com o histórico de movimentações

Tecnologias

- Python 3
- SQLite (módulo `sqlite3`, já vem com o Python)

Como rodar

1. Instale o Python 3
2. Clone o repositório:

2. Clone o repositório:

       git clone https://github.com/Teteus0803/Banco-python.git

3. Entre na pasta e execute:

       python banco.py

O arquivo do banco (`banco.db`) é criado automaticamente na primeira execução.

 Como funciona

O banco tem duas tabelas:

- `contas`: id, nome, saldo, senha, pergunta e resposta
- `transacoes`: id, conta_id, tipo e valor

As consultas usam parâmetros (`?`) para evitar SQL Injection.

 Prints

(coloque aqui os prints do terminal)

 Melhorias futuras

- Guardar a senha com hash em vez de texto puro
- Tratar erros de digitação (letras no lugar de números)
- Garantir que a transferência seja atômica (rollback em caso de erro)
- Separar o código em módulos
- Adicionar testes

 Autor

Matheus Guimarães, estudante de Ciências da Computação
