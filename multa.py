def calcular_multa_com_carencia(atraso, carencia, valor_dia):

    if atraso <= 0:
        return 0.0

    dias_cobrados = max(0, atraso - carencia)

    return round(dias_cobrados * valor_dia, 2)
