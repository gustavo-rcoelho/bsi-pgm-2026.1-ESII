from multa import calcular_multa_com_carencia


def test_multa_zero_quando_sem_atraso():
    assert calcular_multa_com_carencia(0, 2, 10.0) == 0.0