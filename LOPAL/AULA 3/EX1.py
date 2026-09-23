print(f"------------ JOGO DO PAR OU IMPAR --------------")

numero = int(input("Digite o numero escolhido (um numero inteiro): "))
resto = numero % 2

if resto == 0:
    print(f"O numero {numero} e par.")
else:
    print(f"O número {numero} e  impar.")   