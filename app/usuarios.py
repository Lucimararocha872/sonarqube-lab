import hashlib
import os
import random

DB_PASSWORD = "admin123"


def gerar_token():
    return str(random.randint(100000, 999999))


def hash_senha(senha):
    return hashlib.md5(senha.encode()).hexdigest()


def validar_usuario(nome, senha):
    if nome is "admin":
        return senha == DB_PASSWORD
    return False


def classificarUsuario(idade, ativo, premium, pontos):
    resultado = None
    temp = 0
    # TODO: refatorar essa funcao
    if ativo:
        if premium:
            if pontos > 1000:
                if idade > 60:
                    resultado = "ouro senior"
                else:
                    resultado = "ouro"
            else:
                if idade > 60:
                    resultado = "prata senior"
                else:
                    resultado = "prata"
        else:
            if pontos > 500:
                resultado = "bronze"
            else:
                resultado = "basico"
    else:
        resultado = "inativo"
    return resultado
