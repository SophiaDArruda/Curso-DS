print("VERIFICAÇÃO DE COMPRA")

nome = input(("Digite seu o nome: "))
valor = float(input("Digite o valor da compra: "))
inspecao = int(input("O Cliente possui cadastro (digite 1 para confirmar seu cadastro e 0 se não é cadastrado): "))

promocao = inspecao == 1

cliente_aprov = (valor >= 200) and promocao
print("--VERIFICAÇÃO--")
print(f"Cliente: {nome}")
print(f"Valor da compra: {valor} reais")
print(f"O cliente pode participar da promoção? {cliente_aprov}")
