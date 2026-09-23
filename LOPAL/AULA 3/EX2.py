print("---- LOJA VIRTUAL ----")

valor_compra = float((input("Insira o valor da compra: ")))

cliente_vip = int((input("Voce e um cliente vip? (Digite 1 para sim e 0 para nao): ")))


if valor_compra >= 150.00 or cliente_vip == 1:
    print(f"Parabens! Voce ganhou frete gratis.")
else:
    print(f"O frete custara R$ 20.00.")