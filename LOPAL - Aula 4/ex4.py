notas = []
print("Lista inicial", notas)

for tentativa in range(3):
    nota = float(input(f"Digite a nota {tentativa + 1}: "))
    notas.append(nota)
    print("Lista atual: ", notas)
print("Quantidade de notas: ", len(notas))
print("Primeira nota cadastrada: ", notas[0])
