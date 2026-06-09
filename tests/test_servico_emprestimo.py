#test_servico_emprestimo
import datetime
import pytest
from models.equipamento import Notebook


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

def test_usuario_com_tres_emprestimos_nao_pode_registrar_quarto(
    servico,
    repositorio_fake
):
    servico.registrar(1, "Ana", "ana@x.com", 7)

    repositorio_fake._equipamentos.append(
    Notebook(4, "Notebook Extra", "notebook", True)
    )

    servico.registrar(4, "Ana", "ana@x.com", 7)

    repositorio_fake._equipamentos.append(
    Notebook(5, "Notebook Extra 2", "notebook", True)
    )

    servico.registrar(5, "Ana", "ana@x.com", 7)

    repositorio_fake._equipamentos.append(
    Notebook(6, "Notebook Extra 3", "notebook", True)
    )

    resultado = servico.registrar(6, "Ana", "ana@x.com", 7)

    assert resultado is False

def test_usuario_pode_registrar_novo_emprestimo_apos_devolucao(
    servico,
    repositorio_fake
):
    servico.registrar(1, "Ana", "ana@x.com", 7)

    repositorio_fake._equipamentos.append(
        Notebook(4, "Notebook Extra", "notebook", True)
    )
    servico.registrar(4, "Ana", "ana@x.com", 7)

    repositorio_fake._equipamentos.append(
        Notebook(5, "Notebook Extra 2", "notebook", True)
    )
    servico.registrar(5, "Ana", "ana@x.com", 7)

    servico.devolver(1)

    repositorio_fake._equipamentos.append(
        Notebook(6, "Notebook Extra 3", "notebook", True)
    )

    resultado = servico.registrar(6, "Ana", "ana@x.com", 7)

    assert resultado is True
    
def test_limite_de_emprestimos_e_por_usuario(
    servico,
    repositorio_fake
):
    servico.registrar(1, "Ana", "ana@x.com", 7)

    repositorio_fake._equipamentos.append(
        Notebook(4, "Notebook Extra", "notebook", True)
    )
    servico.registrar(4, "Ana", "ana@x.com", 7)

    repositorio_fake._equipamentos.append(
        Notebook(5, "Notebook Extra 2", "notebook", True)
    )
    servico.registrar(5, "Ana", "ana@x.com", 7)

    repositorio_fake._equipamentos.append(
        Notebook(6, "Notebook João", "notebook", True)
    )

    resultado = servico.registrar(
        6,
        "João",
        "joao@x.com",
        7
    )

    assert resultado is True