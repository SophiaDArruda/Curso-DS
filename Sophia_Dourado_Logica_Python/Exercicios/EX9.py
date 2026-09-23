print("Bem vindo ao sistema de divisão de equipes!")
print("-------------------------------------------")


alunos = int(input("Digite a quantidade de alunos: "))
grupos = int(input("Digite a quantidade de alunos por grupo: "))
total = alunos // grupos
totalf = alunos / grupos
rstdalunos = alunos % grupos


print(f"Cálculos feitos! Uma sala com {alunos} alunos pode formar um total de {total} grupos, tendo um resto de {rstdalunos} alunos. ")
print(f"Quantidade de grupos: {total}")
print(f"Divisão real dos grupos: {totalf}")
print(f"Qntd de alunos sem grupo: {rstdalunos}")
