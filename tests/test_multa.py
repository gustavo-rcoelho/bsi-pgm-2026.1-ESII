from multa import calcular_multa_com_carencia


def test_multa_zero_quando_sem_atraso():
    assert calcular_multa_com_carencia(0, 2, 10.0) == 0.0


def test_multa_cobra_dias_alem_da_carencia():
    assert calcular_multa_com_carencia(5, 2, 10.0) == 30.0

def test_multa_dentro_da_carencia_retorna_zero():
    assert calcular_multa_com_carencia(1, 2, 10.0) == 0.0