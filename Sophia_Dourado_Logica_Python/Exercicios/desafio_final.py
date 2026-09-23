print("CONTROLE DE QUALIDADE")

codigo = input(("Digite o código do produto: "))
peso = float(input("Digite o peso do produto: "))
inspecao = int(input("O produto passou pela inspeção visual? (digite 1 para inspeção aprovada e 0 para reprovada): "))

ins_aprov = inspecao == 1

peca_boa = (peso >= 95) and (peso <= 105) and ins_aprov
print("RESULTADO DA ANÁLISE")
print(f"Peça código: {codigo}")
print(f"Peso: {peso} g")
print(f"Status de aprovação: {ins_aprov}")
print(f"Peça está dentro do nível de qualidade? {peca_boa}")

