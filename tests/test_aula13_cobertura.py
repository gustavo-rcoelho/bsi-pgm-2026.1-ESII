import datetime

from app.sistema import SistemaDeEmprestimos
from services.notificador import Notificador
from services.notificador_email import NotificadorEmail


def test_sistema_registra_emprestimo_pela_facade():
    sistema = SistemaDeEmprestimos()

    resultado = sistema.registrar(
        1,
        "Ana",
        "ana@email.com",
        7,
    )

    assert resultado is True


def test_sistema_devolve_emprestimo_pela_facade():
    sistema = SistemaDeEmprestimos()

    sistema.registrar(
        1,
        "Ana",
        "ana@email.com",
        7,
    )

    resultado = sistema.devolver(1)

    assert resultado == 0.0


def test_sistema_lista_atrasados_pela_facade():
    sistema = SistemaDeEmprestimos()

    sistema.registrar(
        1,
        "Ana",
        "ana@email.com",
        7,
    )

    emprestimo = sistema._repositorio.buscar_emprestimo(1)
    emprestimo.data_devolucao = (
        datetime.date.today() - datetime.timedelta(days=2)
    )

    atrasados = sistema.listar_atrasados()

    assert len(atrasados) == 1
    assert atrasados[0][1] == 2


def test_notificador_imprime_emprestimo(capsys):
    notificador = Notificador()

    notificador.notificar_emprestimo(
        "ana@email.com",
        datetime.date(2026, 8, 20),
    )

    saida = capsys.readouterr().out

    assert "ana@email.com" in saida
    assert "empréstimo registrado" in saida


def test_notificador_imprime_devolucao(capsys):
    notificador = Notificador()

    notificador.notificar_devolucao(
        "ana@email.com",
        20.0,
    )

    saida = capsys.readouterr().out

    assert "ana@email.com" in saida
    assert "R$20.00" in saida


def test_notificador_imprime_atraso(capsys):
    notificador = Notificador()

    notificador.notificar_atraso("ana@email.com")

    saida = capsys.readouterr().out

    assert "ana@email.com" in saida
    assert "empréstimo em atraso" in saida


def test_notificador_email_trata_evento_emprestimo(capsys):
    notificador = NotificadorEmail()

    from services.evento import Evento

    notificador.update(
        Evento(
            tipo="emprestimo",
            email="ana@email.com",
            data=datetime.date(2026, 8, 20),
        )
    )

    saida = capsys.readouterr().out

    assert "ana@email.com" in saida
    assert "empréstimo até" in saida


def test_notificador_email_trata_evento_devolucao(capsys):
    notificador = NotificadorEmail()

    from services.evento import Evento

    notificador.update(
        Evento(
            tipo="devolucao",
            email="ana@email.com",
            multa=20.0,
        )
    )

    saida = capsys.readouterr().out

    assert "ana@email.com" in saida
    assert "R$20.00" in saida


def test_notificador_email_trata_evento_atraso(capsys):
    notificador = NotificadorEmail()

    from services.evento import Evento

    notificador.update(
        Evento(
            tipo="atraso",
            email="ana@email.com",
        )
    )

    saida = capsys.readouterr().out

    assert "ana@email.com" in saida
    assert "você está em atraso" in saida
