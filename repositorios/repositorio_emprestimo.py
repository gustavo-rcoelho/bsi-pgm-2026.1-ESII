from models.equipamento import Notebook, Projetor, Cabo
import datetime

class RepositorioEmprestimo:

    def __init__(self):
        self.equipamentos = [
            Notebook(1, "Notebook Dell", "notebook", True),
            Projetor(2, "Projetor Epson", "projetor", True),
            Cabo(3, "Cabo HDMI", "cabo", True),
        ]

        self.emprestimos = []

    def buscar_equipamento(self, equip_id):
        for e in self.equipamentos:
            if e.id == equip_id:
                return e
        return None

    def marcar_indisponivel(self, equip_id):
        eq = self.buscar_equipamento(equip_id)
        if eq:
            eq.disponivel = False

    def marcar_disponivel(self, equip_id):
        eq = self.buscar_equipamento(equip_id)
        if eq:
            eq.disponivel = True

    def salvar_emprestimo(self, emprestimo: Emprestimo):
        self.emprestimos.append(emprestimo)

    def buscar_emprestimo(self, emprestimo_id):
        for e in self.emprestimos:
            if e.id == emprestimo_id:
                return e
        return None

    def marcar_devolvido(self, emprestimo_id):
        emp = self.buscar_emprestimo(emprestimo_id)
        if emp:
            emp.devolvido = True

    def listar_emprestimos(self):
        return self.emprestimos
