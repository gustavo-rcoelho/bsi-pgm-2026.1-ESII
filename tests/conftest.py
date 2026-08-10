import pytest

from models.fabrica_equipamento import FabricaEquipamento
from repositorios.interfaces import IRepositorioEmprestimo
from services.evento import Evento
from services.observer import Observer
from services.servico_emprestimo import ServicoEmprestimo


class RepositorioFake(IRepositorioEmprestimo):

    def __init__(self):
        self._equipamentos = [
            FabricaEquipamento.criar(
                "notebook",
                 1,
                "Notebook Dell"
            ),

            FabricaEquipamento.criar(
                "projetor",
                2,
                "Projetor Epson"
            ),

            FabricaEquipamento.criar(
                "cabo",
                3,
                "Cabo HDMI"
            )
        ]
        self._emprestimos = []

    def buscar_equipamento(self, equip_id):
        return next(
            (e for e in self._equipamentos if e.id == equip_id),
            None
        )

    def salvar_emprestimo(self, emprestimo):
        self._emprestimos.append(emprestimo)

    def marcar_indisponivel(self, equip_id):
        equip = self.buscar_equipamento(equip_id)
        if equip:
            equip.disponivel = False

    def marcar_disponivel(self, equip_id):
        equip = self.buscar_equipamento(equip_id)
        if equip:
            equip.disponivel = True

    def buscar_emprestimo(self, emprestimo_id):
        return next(
            (e for e in self._emprestimos if e.id == emprestimo_id),
            None
        )

    def marcar_devolvido(self, emprestimo_id):
        emp = self.buscar_emprestimo(emprestimo_id)
        if emp:
            emp.devolvido = True

    def listar_emprestimos(self):
        return self._emprestimos

    @property
    def emprestimos(self):
        return self._emprestimos


class NotificadorSpy(Observer):

    def __init__(self):
        self.eventos = []

    def update(self, evento: Evento):
        self.eventos.append(evento)

@pytest.fixture
def repositorio_fake():
    return RepositorioFake()


@pytest.fixture
def notificador_spy():
    return NotificadorSpy()


@pytest.fixture
def servico(repositorio_fake, notificador_spy):
    s = ServicoEmprestimo(
        repositorio_fake
    )

    s.registrar_observer(
        notificador_spy
    )

    return s
