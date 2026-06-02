import pytest
from models.equipamento import Notebook, Projetor, Cabo


@pytest.mark.parametrize(
    "equipamento,dias,multa",
    [
        (Notebook(1, "Dell", "notebook", True), 3, 30.0),
        (Notebook(1, "Dell", "notebook", True), 5, 50.0),

        (Projetor(2, "Epson", "projetor", True), 2, 30.0),
        (Projetor(2, "Epson", "projetor", True), 4, 60.0),

        (Cabo(3, "HDMI", "cabo", True), 3, 6.0),
        (Cabo(3, "HDMI", "cabo", True), 5, 10.0),
    ]
)
def test_calcular_multa_atraso_positivo(
    equipamento,
    dias,
    multa
):
    assert equipamento.calcular_multa(dias) == multa


@pytest.mark.parametrize(
    "equipamento",
    [
        Notebook(1, "Dell", "notebook", True),
        Projetor(2, "Epson", "projetor", True),
        Cabo(3, "HDMI", "cabo", True),
    ]
)
def test_calcular_multa_atraso_negativo_retorna_zero(
    equipamento
):
    assert equipamento.calcular_multa(-5) == 0