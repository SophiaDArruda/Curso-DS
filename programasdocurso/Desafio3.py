print("Bem vindo ao sistema de divisão de pizza!")

pedacos = int(input("Digite a quantidade de pedaços: "))
amigos = int(input("Digite a quantidade de amigos: "))
total = pedacos // amigos
totalf = pedacos / amigos 
sobras = pedacos % amigos

print(f"Cálculos feitos! {amigos} amigos podem comer {total} pedaços, tendo um resto de {sobras} pedaços! ")
print(f"Quantidade de pedaços de pizza : {pedacos}")
print(f"Divisão real dos pedaços : {totalf}")
sabor = str(input("Digite o sabor da pizza (digite utilizando apenas letras minúsculas): "))
if sabor == "chocolate":
 print(f"Não é possível dar nenhuma sobra ao cachorro, guarde os pedaços para depois!")
else:
 print(f"é possível se dar as {sobras} sobras para o cachorro comer!") 
