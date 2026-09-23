print("--- CONVERSOR DE TEMPERATURA ---")

temperatura = float(input("Digite o valor da temperatura: "))
escala = input("Essa temperatura está em Celsius (C) OU Fahrenheit (F)? ")

if escala == "C":
    fahrenheit = (temperatura * 9/5) + 32
    print(f"{temperatura}C equivale a {fahrenheit:.1f}F.")
elif escala == "F":
    celsius = (temperatura-32 * 5/9)
    print (f"{temperatura}F equivale a {celsius:.1f}C")
else: 
    print("Erro! Digite apenas C ou F.")     


