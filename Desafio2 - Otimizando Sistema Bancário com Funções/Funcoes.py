def menu():
    menu = """
Olá, o que deseja fazer?
[d] Depositar
[s] Sacar
[c] Nova Conta
[l] Listar Contas
[u] Novo Usuário
[e] Extrato
[x] Sair
=> """
    return input(menu)

def depositar(saldo, valor_deposito, extrato):        
    if valor_deposito > 0:
        saldo += valor_deposito
        extrato += f"Depósito de R$ {valor_deposito:.2f}\n"
        print(f"Depósito de R$ {valor_deposito:.2f} realizado com sucesso.")
    else:
        print("\nPor favor tente novamente, a operação falhou!")
    
    return saldo, extrato

def sacar(saldo, valor_saque, extrato, num_saques, limite_saques, limite):
    if num_saques >= limite_saques:
        print("\nO saque não pode ser realizado, pois você já excedeu o limite de saques diários.")
        
    elif valor_saque > saldo:
        print("\nVocê não possui saldo suficiente.")
    
    elif valor_saque > limite:
        print("\nO saque não pode ser realizado, pois exede o valor limite de R$ 500,00 por saque.")
    
    elif valor_saque > 0 :
        saldo -= valor_saque
        extrato += f"Saque de R$ {valor_saque:.2f}\n"
        print(f"Saque de R$ {valor_saque:.2f} realizado com sucesso.")
        num_saques += 1
    
    else:
        print("Operação falhou!")

    return saldo, extrato, num_saques

def mostrar_extrato(saldo, extrato):
    print("\n================ EXTRATO ================")
    if not extrato:
        print("Não foi realizada nenhuma movimentação.")
    else:
        print(extrato)
        print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")

def criar_usuario(usuarios):
    cpf = input("Informe seu CPF (apenas números): ")
    usuario = usuario_existente(cpf, usuarios)

    if usuario:
        print("\nEste CPF já pertence a um usuário!")
        return

    nome = input("Informe seu nome completo: ")
    data_nascimento = input("Informe sua data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe seu endereço (logradouro, número, bairro, cidade e estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

    print("\n-> O usuário foi criado com sucesso")

def usuario_existente(cpf, usuarios):
    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            return usuario  
        
    return None

def criar_conta(agencia, num_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = usuario_existente(cpf, usuarios)

    if usuario:
        print("\n-> Conta criada com sucesso!")
        return {"agencia": agencia, "numero_conta": num_conta, "usuario": usuario}
    else:
        print("\nNão foi possível criar conta. Usuário não encontrado")
        return None
    
def listar_contas(contas):
    for conta in contas:
        listar = f"""
        Agência: {conta['agencia']}
        C/C: {conta['numero_conta']}
        Titular: {conta['usuario']['nome']}
        """
        print("-" * 50)
        print(listar)