notas = [7.5, 5.5, 4.0, 9.0]
nova_nota = float(input("Digite uma nota de 0 a 10 (insira ponto . para números decimais):"))

if 0 <= nova_nota <= 10:
    notas.append(nova_nota)
else:
    print("Nota fora do intervalo")

print(f"Notas cadastradas {notas}")
print("Quantidade: ", len(notas))
