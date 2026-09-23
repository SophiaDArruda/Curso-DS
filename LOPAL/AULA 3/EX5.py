print("---- SEMAFORO ----")
cor = input("Qual a cor do semaforo? (verde/amarelo/vermelho): ")

if cor == "verde":
    print("Tudo certo! O carro pode avançar!")
elif cor == "amarelo":
    print("Reduza sua velocidade e tome cuidado ao passar!")
elif cor == "vermelho":
    print("Sinal vermelho! Mantenha o carro parado!")
else:
    print("ERRO! Digite apenas verde, vermelho ou amarelo.")
