from dataclasses import dataclass
from abc import ABC, abstractmethod

@dataclass
class Equipamento(ABC):
    id: int
    nome: str
    tipo: str
    disponivel: bool

    @abstractmethod
    def calcular_multa(self, dias_atraso: int) -> float:
        pass

class Notebook(Equipamento):
    def calcular_multa(self, dias_atraso: int) -> float:
        return max(0, dias_atraso * 10.0)

class Projetor(Equipamento):
    def calcular_multa(self, dias_atraso: int) -> float:
        return max(0, dias_atraso * 15.0)

class Cabo(Equipamento):
    def calcular_multa(self, dias_atraso: int) -> float:
        return max(0, dias_atraso * 2.0)