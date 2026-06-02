import datetime
import pytest


def test_registrar_devolve_true_quando_equipamento_disponivel(
    servico
):
    resultado = servico.registrar(
        1,
        "Ana",
        "ana@email.com",
        7
    )

    assert resultado is True


def test_registrar_devolve_false_quando_equipamento_indisponivel(
    servico,
    repositorio_fake
):
    equipamento = repositorio_fake.buscar_equipamento(1)
    equipamento.disponivel = False

    resultado = servico.registrar(
        1,
        "Ana",
        "ana@email.com",
        7
    )

    assert resultado is False


def test_registrar_notifica_usuario_apos_sucesso(
    servico,
    notificador_spy
):
    servico.registrar(
        1,
        "Ana",
        "ana@email.com",
        7
    )

    assert len(notificador_spy.eventos) == 1
    assert notificador_spy.eventos[0][0] == "emprestimo"


@pytest.mark.parametrize(
    "equip_id,dias_atraso,multa",
    [
        (1, 2, 20.0),
        (1, 3, 30.0),

        (2, 2, 30.0),
        (2, 3, 45.0),

        (3, 2, 4.0),
        (3, 3, 6.0),
    ]
)
def test_devolver_calcula_multa_correta_para_atraso(
    servico,
    repositorio_fake,
    equip_id,
    dias_atraso,
    multa
):
    servico.registrar(
        equip_id,
        "Ana",
        "ana@email.com",
        7
    )

    emp = repositorio_fake.buscar_emprestimo(1)

    emp.data_devolucao = (
        datetime.date.today()
        - datetime.timedelta(days=dias_atraso)
    )

    resultado = servico.devolver(1)

    assert resultado == multa


def test_devolver_marca_equipamento_como_disponivel(
    servico,
    repositorio_fake
):
    servico.registrar(
        1,
        "Ana",
        "ana@email.com",
        7
    )

    emp = repositorio_fake.buscar_emprestimo(1)

    emp.data_devolucao = (
        datetime.date.today()
        - datetime.timedelta(days=1)
    )

    servico.devolver(1)

    equipamento = repositorio_fake.buscar_equipamento(1)

    assert equipamento.disponivel is True


def test_devolver_falha_silenciosamente_para_emprestimo_inexistente(
    servico
):
    resultado = servico.devolver(999)

    assert resultado is None