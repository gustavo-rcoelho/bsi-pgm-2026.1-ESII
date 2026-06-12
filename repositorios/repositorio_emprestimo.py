from repositorios.interfaces import IRepositorioEmprestimo
from models.fabrica_equipamento import FabricaEquipamento
from models.emprestimo import Emprestimo
import datetime

class RepositorioEmprestimo(IRepositorioEmprestimo):

    def __init__(self):
        
        criar = FabricaEquipamento.criar
        
        self.equipamentos = [
            criar("notebook", 1, "Notebook Dell"),
            criar("projetor", 2, "Projetor Epson"),
            criar("cabo", 3, "Cabo HDMI")
        ]
        self.emprestimos = []

    def buscar_equipamento(self, equip_id):
        for e in self.equipamentos:
            if e.id == equip_id:
                return e
        return None

    def marcar_indisponivel(self, equip_id):
        equipamento = self.buscar_equipamento(equip_id)
        if equipamento:
            equipamento.disponivel = False

    def marcar_disponivel(self, equip_id):
        equipamento = self.buscar_equipamento(equip_id)
        if equipamento:
            equipamento.disponivel = True

    def salvar_emprestimo(self, emprestimo: Emprestimo):
        self.emprestimos.append(emprestimo)

    def buscar_emprestimo(self, emprestimo_id):
        for e in self.emprestimos:
            if e.id == emprestimo_id:
                return e
        return None

    def marcar_devolvido(self, emprestimo_id):
        emprestimo = self.buscar_emprestimo(emprestimo_id)
        if emprestimo:
            emprestimo.devolvido = True

    def listar_emprestimos(self):
        return self.emprestimos
    
    