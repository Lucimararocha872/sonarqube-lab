import pytest
from app.calculos import somar, dividir, media


def test_somar():
    assert somar(2, 3) == 5


def test_dividir():
    assert dividir(10, 2) == 5


def test_dividir_por_zero():
    with pytest.raises(ValueError):
        dividir(1, 0)


def test_media():
    assert media([2, 4, 6]) == 4
    assert media([]) == 0
