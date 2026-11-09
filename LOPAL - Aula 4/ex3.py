notas = [7.5, 5.5, 9.0, 6.0]
qntd_na_media = 0

for nota in notas:
    if nota >= 6.00:
        print(nota, "- Atingiu a média")
        qntd_na_media +=1
    else:
        print(nota, "- Abaixo da média")

print(f"Quantidade que atingiu a média: {qntd_na_media}")