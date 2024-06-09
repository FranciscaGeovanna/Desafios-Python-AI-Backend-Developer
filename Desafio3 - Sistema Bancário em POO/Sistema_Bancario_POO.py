from abc import ABC, abstractmethod
from datetime import datetime

class Cliente:
    def __init__(self, endereco) -> None:
        self.endereco = endereco
        self.contas = []
    
    def cadastrar_conta(self, conta):
        self.contas.append(conta)
    
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
    
    
class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
        super().__init__(endereco)
    
    def __str__(self):
        return self.nome

    def __repr__(self):
        return self.__str__()
    

class Historico:
    def __init__(self):
        self._transacoes = []
    
    @property
    def transacoes(self):
        return self._transacoes
    
    def add_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )


class Conta:
    def __init__(self, num, cliente) -> None:
        self._saldo = 0
        self._num = num
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()
    
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def agencia(self):
        return self._agencia

    @property
    def num(self):
        return self._num
    
    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico
    
    def sacar(self, valor_saque):
        saldo = self.saldo
        saldo_execedido = valor_saque > saldo
        
        if saldo_execedido:
            print("\nERRO: Você não possui saldo suficiente.")
        elif valor_saque > 0:
            self._saldo -= valor_saque
            print(f"\nSaque de R$ {valor_saque:.2f} realizado com sucesso!")
            return True
        else:
            print("\nERRO: Operação falhou!")
        
        return False
    
    def depositar(self, valor_deposito):
        if valor_deposito > 0:
            self._saldo += valor_deposito
            print(f"\nDepósito de R$ {valor_deposito:.2f} realizado com sucesso!")
        else:
            print("\nERRO: Por favor tente novamente, a operação falhou.")
            return False
    
        return True
    

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass
    
    @abstractmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor_saque):
        self._valor_saque = valor_saque
        
    @property
    def valor(self):
        return self._valor_saque
    
    def registrar(self, conta):
        transacao_realizada = conta.sacar(self.valor)

        if transacao_realizada:
            conta.historico.add_transacao(self)

 
class ContaCorrente(Conta):
    def __init__(self, num, cliente, limite = 500, limite_saque = 3):
        self.limite = limite
        self.limite_saque = limite_saque
        super().__init__(num, cliente)
    
    def sacar(self, valor_saque):
        num_saque = len(
            [ transacao for transacao in self.historico.transacoes 
            if transacao["tipo"] == Saque.__name__ ]
        )
        
        excedeu_limite = valor_saque > self.limite
        excedeu_saques = num_saque >= self.limite_saque
        
        if excedeu_limite:
            print("\nERRO: O saque não pode ser realizado, pois exede o valor limite de R$ 500,00 por saque.")
        elif excedeu_saques:
            print("\nERRO: O saque não pode ser realizado, pois você já excedeu o limite de saques diários.")
        else:
            return super().sacar(valor_saque)
    
        return False
    
    def __str__(self):
        return (
            f"Agência:        {self.agencia}\n"
            f"C/C:            {self.num}\n"
            f"Titular:        {self.cliente.nome}\n"
        )

    def __repr__(self):
        return self.__str__()

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        transacao_realizada = conta.depositar(self.valor)

        if transacao_realizada:
            conta.historico.add_transacao(self)


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


def verificar_cliente(clientes, cpf):
    cliente_verificado = [ cliente for cliente in clientes if isinstance(cliente, PessoaFisica) and cliente.cpf == cpf ]
    return cliente_verificado[0] if cliente_verificado else None

def recuperar_conta(cliente):
    if cliente.contas:
        return cliente.contas[0]
    else:
        print("\nERRO: O cliente não possui uma conta.")
        return None
    

def depositar(clientes):
    cpf = input("\nInforme o CPF: ")
    cliente = verificar_cliente(clientes, cpf)
    
    if not cliente:
        print("\nERRO: O cliente não foi encontrado.")
        return
    
    valor = float(input("Informe o valor que deseja depositar (xxx.xx): R$ "))
    transacao = Deposito(valor)
    
    conta = recuperar_conta(cliente)
    
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

def sacar(clientes):
    cpf = input("\nInforme o CPF: ")
    cliente = verificar_cliente(clientes, cpf)

    if not cliente:
        print("\nERRO: O cliente não foi encontrado.")
        return

    valor = float(input("Informe o valor que deseja sacra: R$ "))
    transacao = Saque(valor)

    conta = recuperar_conta(cliente)
    
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)

def mostrar_extrato(clientes):
    cpf = input("\nInforme o CPF: ")
    cliente = verificar_cliente(clientes, cpf)

    if not cliente:
        print("\nERRO: O cliente não foi encontrado.")
        return

    conta = recuperar_conta(cliente)
    
    if not conta:
        return

    print("\n================ EXTRATO ================")
    
    transacoes = conta.historico.transacoes
    extrato = ""
    
    if not transacoes:
        print("Não foi realizada nenhuma movimentação.")
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"
        print(extrato)
        print(f"\n\nSaldo: R$ {conta.saldo:.2f}")
        
    print("==========================================")

def cadastrar_cliente(clientes):
    cpf = input("\nInforme o CPF (apenas números): ")
    cliente = verificar_cliente(clientes, cpf)

    if cliente:
        print(f"\nERRO: Já existe um cliente com o CPF {cpf}")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, número, bairro, cidade e estado): ")

    cliente = PessoaFisica(nome = nome, data_nascimento = data_nascimento, cpf = cpf, endereco = endereco)
    clientes.append(cliente)

    print("\nCliente cadastrado com sucesso!")

def cadastrar_conta(num_conta, clientes, contas):
    cpf = input("\nInforme o CPF: ")
    cliente = verificar_cliente(clientes, cpf)

    if not cliente:
        print("\nERRO: Não foi possível encontrar o cliente.")
        return

    conta = ContaCorrente.nova_conta(cliente = cliente, numero = num_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("\nA conta foi criada com sucesso!")

def mostrar_contas(contas):
    for conta in contas:
        print("=" * 90)
        print(conta)


def Main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            depositar(clientes)

        elif opcao == "s":
            sacar(clientes)

        elif opcao == "e":
            mostrar_extrato(clientes)

        elif opcao == "u":
            cadastrar_cliente(clientes)

        elif opcao == "c":
            num_conta = len(contas) + 1
            cadastrar_conta(num_conta, clientes, contas)

        elif opcao == "l":
            mostrar_contas(contas)

        elif opcao == "x":
            break

        else:
            print("\nERRO: Opção inválida, por favor selecione novamente.")

Main()