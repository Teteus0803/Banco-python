import sqlite3

banco = sqlite3.connect('banco.db')


# ==================================================
# CRIAÇÃO DAS TABELAS
# ==================================================

banco.execute(
    'CREATE TABLE IF NOT EXISTS contas '
    '(id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, saldo REAL)'
)

banco.commit()


# Adiciona a coluna senha caso ela ainda não exista
try:

    banco.execute(
        'ALTER TABLE contas ADD COLUMN senha TEXT'
    )

    banco.commit()

except sqlite3.OperationalError:

    pass


# Adiciona a coluna pergunta caso ela ainda não exista
try:

    banco.execute(
        'ALTER TABLE contas ADD COLUMN pergunta TEXT'
    )

    banco.commit()

except sqlite3.OperationalError:

    pass


# Adiciona a coluna resposta caso ela ainda não exista
try:

    banco.execute(
        'ALTER TABLE contas ADD COLUMN resposta TEXT'
    )

    banco.commit()

except sqlite3.OperationalError:

    pass


# Tabela de transações
banco.execute(
    'CREATE TABLE IF NOT EXISTS transacoes '
    '(id INTEGER PRIMARY KEY AUTOINCREMENT, '
    'conta_id INTEGER, tipo TEXT, valor REAL)'
)

banco.commit()


# ==================================================
# CRIAR CONTA
# ==================================================

def criar_conta():

    print()
    print('===== CRIAR CONTA =====')

    nome = input('Digite seu nome: ')
    senha = input('Crie sua senha: ')

    pergunta = input(
        'Crie uma pergunta de segurança: '
    )

    resposta = input(
        'Digite a resposta: '
    )

    saldo = 0

    banco.execute(
        'INSERT INTO contas '
        '(nome, senha, saldo, pergunta, resposta) '
        'VALUES (?, ?, ?, ?, ?)',
        (nome, senha, saldo, pergunta, resposta)
    )

    banco.commit()

    resultado = banco.execute(
        'SELECT id FROM contas '
        'WHERE nome = ? AND senha = ? '
        'ORDER BY id DESC',
        (nome, senha)
    )

    conta = resultado.fetchone()

    print()
    print('Conta criada com sucesso!')
    print('Seu ID é:', conta[0])
    print('Guarde esse ID para entrar na conta!')


# ==================================================
# RECUPERAR SENHA
# ==================================================

def recuperar_senha():

    print()
    print('===== RECUPERAR SENHA =====')

    id_busca = int(
        input('Digite o ID da conta: ')
    )

    resultado = banco.execute(
        'SELECT * FROM contas WHERE id = ?',
        (id_busca,)
    )

    conta = resultado.fetchone()

    if conta is None:

        print('Conta não encontrada!')

    else:

        print()
        print('Pergunta de segurança:')
        print(conta[4])

        resposta = input(
            'Digite a resposta: '
        )

        if resposta == conta[5]:

            nova_senha = input(
                'Digite sua nova senha: '
            )

            banco.execute(
                'UPDATE contas SET senha = ? '
                'WHERE id = ?',
                (nova_senha, id_busca)
            )

            banco.commit()

            print()
            print('Senha alterada com sucesso!')

        else:

            print()
            print('Resposta incorreta!')


# ==================================================
# LOGIN
# ==================================================

def login():

    print()
    print('===== LOGIN =====')

    id_busca = int(
        input('Digite o ID da conta: ')
    )

    senha = input(
        'Digite sua senha: '
    )

    resultado = banco.execute(
        'SELECT * FROM contas '
        'WHERE id = ? AND senha = ?',
        (id_busca, senha)
    )

    conta = resultado.fetchone()

    if conta is None:

        print('ID ou senha incorretos!')

    else:

        print()
        print('Login realizado com sucesso!')
        print('Bem-vindo,', conta[1])

        menu_conta(conta)


# ==================================================
# EXTRATO
# ==================================================

def extrato(conta):

    resultado = banco.execute(
        'SELECT tipo, valor '
        'FROM transacoes '
        'WHERE conta_id = ?',
        (conta[0],)
    )

    transacoes = resultado.fetchall()

    print()
    print('========== EXTRATO ==========')

    if not transacoes:

        print('Nenhuma movimentação encontrada.')

    else:

        for transacao in transacoes:

            print(
                transacao[0],
                '- R$',
                transacao[1]
            )


# ==================================================
# MENU DA CONTA
# ==================================================

def menu_conta(conta):

    opcao = ''

    while opcao != '6':

        print()
        print('===== BANCO PYTHON =====')
        print('1 - Ver saldo')
        print('2 - Depositar')
        print('3 - Sacar')
        print('4 - Transferir')
        print('5 - Extrato')
        print('6 - Sair da Conta')

        opcao = input(
            'Escolha uma opção: '
        )


        # ------------------------------------------
        # VER SALDO
        # ------------------------------------------

        if opcao == '1':

            print()
            print('Seu saldo é:', conta[2])


        # ------------------------------------------
        # DEPOSITAR
        # ------------------------------------------

        elif opcao == '2':

            valor = float(
                input(
                    'Quanto deseja depositar? '
                )
            )

            if valor > 0:

                conta = (
                    conta[0],
                    conta[1],
                    conta[2] + valor,
                    conta[3],
                    conta[4],
                    conta[5]
                )

                banco.execute(
                    'UPDATE contas SET saldo = ? '
                    'WHERE id = ?',
                    (conta[2], conta[0])
                )

                banco.execute(
                    'INSERT INTO transacoes '
                    '(conta_id, tipo, valor) '
                    'VALUES (?, ?, ?)',
                    (
                        conta[0],
                        'Deposito',
                        valor
                    )
                )

                banco.commit()

                print()
                print('Depósito realizado!')
                print(
                    'Seu novo saldo é:',
                    conta[2]
                )

            else:

                print('Valor inválido!')


        # ------------------------------------------
        # SACAR
        # ------------------------------------------

        elif opcao == '3':

            valor = float(
                input(
                    'Quanto deseja sacar? '
                )
            )

            if valor > 0 and valor <= conta[2]:

                conta = (
                    conta[0],
                    conta[1],
                    conta[2] - valor,
                    conta[3],
                    conta[4],
                    conta[5]
                )

                banco.execute(
                    'UPDATE contas SET saldo = ? '
                    'WHERE id = ?',
                    (conta[2], conta[0])
                )

                banco.execute(
                    'INSERT INTO transacoes '
                    '(conta_id, tipo, valor) '
                    'VALUES (?, ?, ?)',
                    (
                        conta[0],
                        'Saque',
                        valor
                    )
                )

                banco.commit()

                print()
                print('Saque realizado!')
                print(
                    'Seu novo saldo é:',
                    conta[2]
                )

            else:

                print(
                    'Valor inválido ou '
                    'saldo insuficiente!'
                )


        # ------------------------------------------
        # TRANSFERIR
        # ------------------------------------------

        elif opcao == '4':

            id_destino = int(
                input(
                    'Digite o ID da conta destino: '
                )
            )

            valor = float(
                input(
                    'Digite o valor da transferência: '
                )
            )

            resultado = banco.execute(
                'SELECT * FROM contas WHERE id = ?',
                (id_destino,)
            )

            conta_destino = resultado.fetchone()


            # Conta não existe
            if conta_destino is None:

                print(
                    'Conta destino não encontrada!'
                )


            # Não pode transferir para si mesmo
            elif id_destino == conta[0]:

                print(
                    'Você não pode transferir '
                    'para sua própria conta!'
                )


            # Valor inválido
            elif valor <= 0:

                print('Valor inválido!')


            # Saldo insuficiente
            elif valor > conta[2]:

                print('Saldo insuficiente!')


            # Transferência
            else:

                # Tira o dinheiro da conta atual
                novo_saldo = conta[2] - valor

                banco.execute(
                    'UPDATE contas SET saldo = ? '
                    'WHERE id = ?',
                    (novo_saldo, conta[0])
                )


                # Coloca o dinheiro na conta destino
                novo_saldo_destino = (
                    conta_destino[2] + valor
                )

                banco.execute(
                    'UPDATE contas SET saldo = ? '
                    'WHERE id = ?',
                    (
                        novo_saldo_destino,
                        conta_destino[0]
                    )
                )


                # Registra transferência enviada
                banco.execute(
                    'INSERT INTO transacoes '
                    '(conta_id, tipo, valor) '
                    'VALUES (?, ?, ?)',
                    (
                        conta[0],
                        'Transferencia enviada',
                        valor
                    )
                )


                # Registra transferência recebida
                banco.execute(
                    'INSERT INTO transacoes '
                    '(conta_id, tipo, valor) '
                    'VALUES (?, ?, ?)',
                    (
                        conta_destino[0],
                        'Transferencia recebida',
                        valor
                    )
                )

                banco.commit()


                # Atualiza o saldo da conta atual
                conta = (
                    conta[0],
                    conta[1],
                    novo_saldo,
                    conta[3],
                    conta[4],
                    conta[5]
                )

                print()
                print('Transferência realizada!')
                print(
                    'Valor transferido:',
                    valor
                )
                print(
                    'Novo saldo:',
                    conta[2]
                )


        # ------------------------------------------
        # EXTRATO
        # ------------------------------------------

        elif opcao == '5':

            extrato(conta)


        # ------------------------------------------
        # SAIR DA CONTA
        # ------------------------------------------

        elif opcao == '6':

            print('Saindo da conta...')


        # ------------------------------------------
        # OPÇÃO INVÁLIDA
        # ------------------------------------------

        else:

            print('Opção inválida!')


# ==================================================
# MENU PRINCIPAL
# ==================================================

while True:

    print()
    print('===== BANCO PYTHON =====')
    print('1 - Criar conta')
    print('2 - Entrar')
    print('3 - Esqueci minha senha')
    print('4 - Sair')

    opcao = input(
        'Escolha uma opção: '
    )


    # ----------------------------------------------
    # CRIAR CONTA
    # ----------------------------------------------

    if opcao == '1':

        criar_conta()


    # ----------------------------------------------
    # LOGIN
    # ----------------------------------------------

    elif opcao == '2':

        login()


    # ----------------------------------------------
    # RECUPERAR SENHA
    # ----------------------------------------------

    elif opcao == '3':

        recuperar_senha()


    # ----------------------------------------------
    # SAIR
    # ----------------------------------------------

    elif opcao == '4':

        print(
            'Saindo do Banco Python...'
        )

        break


    # ----------------------------------------------
    # OPÇÃO INVÁLIDA
    # ----------------------------------------------

    else:

        print('Opção inválida!')


# ==================================================
# FECHAR BANCO
# ==================================================

banco.close()