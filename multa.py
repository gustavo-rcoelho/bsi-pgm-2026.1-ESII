def calcular_multa_com_carencia(atraso, carencia, valor_dia):
    if atraso <= 0:
        return 0.0

    dias_cobrados = atraso - carencia
    return dias_cobrados * valor_dia