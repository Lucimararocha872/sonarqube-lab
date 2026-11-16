def somar(a, b):
    return a + b


def dividir(a, b):
    if b == 0:
        raise ValueError("divisao por zero")
    return a / b


def media(valores):
    if not valores:
        return 0
    return sum(valores) / len(valores)
