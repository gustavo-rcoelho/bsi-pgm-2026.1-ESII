from repositorios.repositorio_emprestimo import RepositorioEmprestimo
from services.notificador import Notificador
from services.servico_emprestimo import ServicoEmprestimo


def test_fluxo_registrar_devolver_com_componentes_reais():

    repositorio = RepositorioEmprestimo()
    notificador = Notificador()
    servico = ServicoEmprestimo(
        repositorio,
        notificador
    )

    sucesso = servico.registrar(
        1,
        "Ana",
        "ana@ufra.edu.br",
        dias=7
    )

    assert sucesso is True

    emprestimo = repositorio.buscar_emprestimo(1)

    assert emprestimo is not None
    assert emprestimo.equipamento_id == 1

    equipamento = repositorio.buscar_equipamento(1)

    assert equipamento.disponivel is False