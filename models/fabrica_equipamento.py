from models.equipamento import Notebook, Projetor, Cabo
from models.multa_strategy import MultaPorDia


class FabricaEquipamento:

    _config = {
        "notebook": (Notebook, MultaPorDia(10.0)),
        "projetor": (Projetor, MultaPorDia(15.0)),
        "cabo": (Cabo, MultaPorDia(2.0)),
    }

    @classmethod
    def criar(cls, tipo, id, nome):

        classe, estrategia = cls._config.get(tipo, (None, None))

        if classe is None:
            raise ValueError(f"Tipo desconhecido: {tipo}")

        return classe(id, nome, tipo, estrategia)