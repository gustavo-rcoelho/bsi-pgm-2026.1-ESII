import pytest

from models.fabrica_equipamento import FabricaEquipamento


@pytest.mark.parametrize(
    "equipamento,dias,multa",
    [
        (FabricaEquipamento.criar("notebook", 1, "Dell"), 3, 30.0),
        (FabricaEquipamento.criar("notebook", 1, "Dell"), 5, 50.0),

        (FabricaEquipamento.criar("projetor", 2, "Epson"), 2, 30.0),
        (FabricaEquipamento.criar("projetor", 2, "Epson"), 4, 60.0),

        (FabricaEquipamento.criar("cabo", 3, "HDMI"), 3, 6.0),
        (FabricaEquipamento.criar("cabo", 3, "HDMI"), 5, 10.0),
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
        FabricaEquipamento.criar("notebook", 1, "Dell"),
        FabricaEquipamento.criar("projetor", 2, "Epson"),
        FabricaEquipamento.criar("cabo", 3, "HDMI"),
    ]
)
def test_calcular_multa_atraso_negativo_retorna_zero(
    equipamento
):
    assert equipamento.calcular_multa(-5) == 0