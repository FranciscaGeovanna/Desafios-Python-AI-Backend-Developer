menu = '''
Olá, o que deseja fazer?
[d] Depositar
[s] Sacar
[e] Extrato
[x] Sair
'''

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:
    print(menu)
    opcao = input("=> ")
    
    if opcao == "d":
        valor_deposito = float(input("Informe o valor que deseja depositar (xxx.xx): R$ "))
        
        if valor_deposito > 0:
            saldo += valor_deposito
            extrato += f"Depósito de R$ {valor_deposito:.2f}\n"
            print(f"Depósito de R$ {valor_deposito:.2f} realizado com sucesso.")
        else:
            print("Por favor tente novamente, a operação falhou!")
                    
    elif opcao == "s":
        valor_saque = float(input("Informe o valor que deseja sacar (xxx.xx): R$ "))
        
        if numero_saques >= LIMITE_SAQUES:
            print("O saque não pode ser realizado, pois você já excedeu o limite de saques diários.")
        
        elif valor_saque > saldo:
            print("Você não possui saldo suficiente.")
        
        elif valor_saque > 500:
            print("O saque não pode ser realizado, pois exede o valor limite de R$ 500,00 por saque.")
        
        elif valor_saque > 0 :
            saldo -= valor_saque
            extrato += f"Saque de R$ {valor_saque:.2f}\n"
            print(f"Saque de R$ {valor_saque:.2f} realizado com sucesso.")
            numero_saques += 1
        
        else:
            print("Operação falhou!")
        
    elif opcao == "e":
        print("\n================ EXTRATO ================")
        if not extrato:
            print("Não foi realizada nenhuma movimentação.")
        else:
            print(extrato)
            print(f"\nSaldo: R$ {saldo:.2f}")
        print("==========================================")
        
    elif opcao == "x":
        print("Encerrando programa...")
        break
    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")