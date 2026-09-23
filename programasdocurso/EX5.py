print("Bem vindo ao Sistema Escolar!")

nome = input("Digite o nome do aluno: ")
prova1 =  float(input("Nota da prova 1: "))
prova2 =  float(input("Nota da prova 2: "))
prova3 =  float(input("Nota da prova 3: "))
trabalho =  float(input("Nota do trabalho: "))
matriculado = True

media_provas = (prova1 + prova2 + prova3) / 3
media_final = (media_provas + trabalho) / 2
status_aprov = (media_provas >= 7.0) and (matriculado == True)
print(f"\n------RELATÓRIO DA PROVA------")
if status_aprov == False :
    print(f"Caro aluno(a) {nome}, você se encontra em recuperação.")
    print(f"Status de aprovação: {status_aprov}")
    print(f"A média final do aluno foi de {media_final:.1f}")
else: 
  print(f"Caro aluno(a) {nome}, você passou de ano!")
  print(f"Status de aprovação: {status_aprov}")
  print(f"A média final do aluno foi de {media_final:.1f}")


