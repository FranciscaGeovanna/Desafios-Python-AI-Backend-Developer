from Funcoes import *

def main():
    saldo = 0
    limite = 500
    extrato = ""
    num_saques = 0
    usuarios = []
    contas = []
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    while True:
        opcao = menu()

        if opcao == "d":
            valor_deposito = float(input("Informe o valor que deseja depositar (xxx.xx): R$ "))

            saldo, extrato = depositar(saldo, valor_deposito, extrato)

        elif opcao == "s":
            valor_saque = float(input("Informe o valor que deseja sacar (xxx.xx): R$"))

            saldo, extrato, num_saques = sacar(
                saldo = saldo,
                valor_saque = valor_saque,
                extrato = extrato,
                limite = limite,
                num_saques = num_saques,
                limite_saques = LIMITE_SAQUES,
            )

        elif opcao == "e":
            mostrar_extrato(saldo, extrato = extrato)

        elif opcao == "u":
            criar_usuario(usuarios)

        elif opcao == "c":
            num_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, num_conta, usuarios)

            if conta:
                contas.append(conta)

        elif opcao == "l":
            listar_contas(contas)

        elif opcao == "x":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

main()