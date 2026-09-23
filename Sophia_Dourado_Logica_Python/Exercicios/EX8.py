print("Bem vindo ao sistema de divisão de balas!")


balas = int(input("Digite a quantidade de balas: "))
amigos = int(input("Digite a quantidade de amigos: "))
total = balas // amigos
totalf = balas / amigos
sobras = balas % amigos


print(f"Cálculos feitos! {amigos} amigos podem comer {total} balas, tendo um resto de {sobras} balas! ")
print(f"Quantidade de pedaços de balas: {balas}")
print(f"Divisão real das balas : {totalf}")
print(f"Qntd de balas restantes {sobras}")
