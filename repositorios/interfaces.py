from abc import ABC, abstractmethod


class IRepositorioEmprestimo(ABC):

    @abstractmethod
    def buscar_equipamento(self, equip_id):
        pass

    @abstractmethod
    def salvar_emprestimo(self, emprestimo):
        pass

    @abstractmethod
    def marcar_indisponivel(self, equip_id):
        pass

    @abstractmethod
    def buscar_emprestimo(self, emprestimo_id):
        pass

    @abstractmethod
    def marcar_devolvido(self, emprestimo_id):
        pass

    @abstractmethod
    def marcar_disponivel(self, equipamento_id):
        pass

    @abstractmethod
    def listar_emprestimos(self):
        pass