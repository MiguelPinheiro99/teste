import mysql.connector 
conexao = mysql.connector.connect( 
    host = 'localhost',
    user = 'root',
    password = 'miguelpinheiro1704',
    database = 'registro'
)
cursor = conexao.cursor() 

import random

class Banco:
    
    def __init__(self):
        comando = 'SELECT * FROM banco'
        cursor.execute(comando)
        self.contas = cursor.fetchall()

    def atualizar_banco(self):
        comando = 'SELECT * FROM banco'
        cursor.execute(comando)
        self.contas = cursor.fetchall()
    
    def criar_conta(self, nome_titular: str, moeda: str, saldo: int) -> None:
        numero = random.randint(00000, 99999)
        comando = f'INSERT INTO banco (nome_titular, numero_conta, moeda, saldo) VALUES ("{nome_titular}", "{numero}", "{moeda}", {saldo})'
        cursor.execute(comando)
        conexao.commit()
        self.atualizar_banco()

    def deposito(self, valor: int, nome: str) -> None:
        for c in self.contas:
            if nome == c[1]:
                if c[4] == 'dolar':
                    valor = valor / moedas[1][1]
                elif c[4] == 'euro':
                    valor = valor / moedas[2][1]
                valor += c[3]
                comando = f'UPDATE banco SET saldo = {valor} WHERE nome_titular = "{nome}";'
                cursor.execute(comando)
                conexao.commit()
                self.atualizar_banco()

    def saque(self, valor: int, nome: str) -> None:
        for c in self.contas:
            if nome == c[1]:
                if c[4] == 'dolar':
                    valor = valor / moedas[1][1]
                elif c[4] == 'euro':
                    valor = valor / moedas[2][1]
                if valor <= c[3]:
                    valor = c[3] - valor
                    comando = f'UPDATE banco SET saldo = {valor} WHERE nome_titular = "{nome}";'
                    cursor.execute(comando)
                    conexao.commit()
                    self.atualizar_banco()
                    print('Saque realizado com sucesso!')
                else:
                    print('Saldo insuficiente!')
                    
    def transferencia(self, valor: int, nome_enviador: str, nome_recebedor: str) -> None:
        for c in self.contas:
            if nome_enviador == c[1]:
                remetente = c
            if nome_recebedor == c[1]:
                destinatario = c

        dolar = valor / moedas[1][1]
        euro = valor / moedas[2][1]

        if remetente[4] == 'dolar':
            valor_novo1 = dolar
        elif remetente[4] == 'euro':
            valor_novo1 = euro
        else:
            valor_novo1 = valor
        if remetente[3] >= valor_novo1:
            valor_remetente = remetente[3] - valor_novo1

        if destinatario[4] == 'dolar':
            valor_novo2 = dolar
        elif destinatario[4] == 'euro':
            valor_novo2 = euro
        else:
            valor_novo2 = valor
        valor_destinatario = destinatario[3] + valor_novo2
        
        comando = f'UPDATE banco SET saldo = {valor_remetente} WHERE nome_titular = "{remetente[1]}";'
        cursor.execute(comando)
        comando = f'UPDATE banco SET saldo = {valor_destinatario} WHERE nome_titular = "{destinatario[1]}";'
        cursor.execute(comando)
        conexao.commit()
        self.atualizar_banco()
        print(f'Transferência efetuada. O titular {remetente[1]} enviou {valor} para {destinatario[1]}')

    def exibir_conta(self, nome: str) -> None:
        for c in self.contas:
            if nome == c[1]:
                if c[4] == 'dolar':
                    m = '$'
                elif c[4] == 'euro':
                    m = '£'
                else:
                    m = 'R$'
                print(f'Nome: {c[1]} / N. Conta: {c[2]} / Saldo: {m} {c[3]},00')
            
    def exibir_tudo(self) -> None:
        for c in self.contas:
            if c[4] == 'dolar':
                m = '$'
            elif c[4] == 'euro':
                m = '£'
            else:
                m = 'R$'
            print(f'Nome: {c[1]} / N. Conta: {c[2]} / Saldo: {m} {c[3]},00')

banco = Banco()
moedas = [['real'],['dolar', 5.66],['euro', 6.15]]

print('Bem vindo ao Banco.')
print('[1] Criar Conta')
print('[2] Exibir Conta')
print('[3] Exibir Todas as Contas')
print('[4] Depósito')
print('[5] Saque')
print('[6] Transferência')
print('[7] Sair')
opc = int(input('O que deseja fazer? '))

while True:
    if opc == 1:
        print('Vamos criar sua conta, apenas precisamos de algumas informações...')
        nome = input('Digite seu nome: ')
        for i,c in enumerate(moedas):
            print(f'{i} = {c[0]}')
        escolha = int(input('Escolha sua moeda: '))
        moeda = moedas[escolha][0]
        saldo = int(input('Diga qual será seu saldo inicial: '))
        banco.criar_conta(nome,moeda,saldo)
        print('Conta criada com sucesso!')
    if opc == 2:
        nome = input('Diga o nome do proprietário da conta: ')
        banco.exibir_conta(nome)
    if opc == 3:
        print('Exibindo todas as contas...')
        banco.exibir_tudo()
    if opc == 4:
        print('Vamos fazer seu depósito')
        nome = input('Diga o nome do proprietário da conta: ')
        valor = int(input('Diga o valor do depósito em real. R$: '))
        banco.deposito(valor, nome)
        print('Depósito realizado com sucesso')
    if opc == 5:
        print('Vamos fazer seu saque')
        nome = input('Diga o nome do proprietário da conta: ')
        valor = int(input('Diga o valor do saque em real. R$: '))
        banco.saque(valor, nome)
    if opc == 6:
        print('Vamos fazer sua transferência')
        enviador = input('Digite o nome do enviador da transferência: ')
        recebedor = input('Digite o nome do recebedor da transferência: ')
        valor = int(input('Digite o valor da transferência em real. R$: '))
        banco.transferencia(valor, enviador, recebedor)
        print('Transferência realizada com sucesso!')
    if opc == 7:
        break
    print('[1] Criar Conta')
    print('[2] Exibir Conta')
    print('[3] Exibir Todas as Contas')
    print('[4] Depósito')
    print('[5] Saque')
    print('[6] Transferência')
    print('[7] Sair')
    opc = int(input('O que deseja fazer? '))

cursor.close() 
conexao.close() 
