import datetime

from models.emprestimo import Emprestimo
from services.evento import Evento
from services.observer import Subject


class ServicoEmprestimo(Subject):

    def __init__(self, repositorio):
        super().__init__()
        self.repo = repositorio

    def _contar_emprestimos_abertos(self, email):
        contador = 0

        for emp in self.repo.listar_emprestimos():
            if emp.usuario_email == email and not emp.devolvido:
                contador += 1

        return contador

    def registrar(self, equipamento_id, nome, email, dias):

        if self._contar_emprestimos_abertos(email) >= 3:
            return False

        equipamento = self.repo.buscar_equipamento(equipamento_id)

        if equipamento is None or not equipamento.disponivel:
            return False

        hoje = datetime.date.today()
        data_devolucao = hoje + datetime.timedelta(days=dias)

        emprestimo = Emprestimo(
            id=len(self.repo.emprestimos) + 1,
            equipamento_id=equipamento_id,
            equipamento_nome=equipamento.nome,
            tipo=equipamento.tipo,
            usuario_nome=nome,
            usuario_email=email,
            data_emprestimo=hoje,
            data_devolucao=data_devolucao,
            devolvido=False
        )

        self.repo.salvar_emprestimo(emprestimo)
        self.repo.marcar_indisponivel(equipamento_id)

        self.notificar(
            Evento(
                tipo="emprestimo",
                email=email,
                data=data_devolucao
            )
        )

        return True

    def devolver(self, emprestimo_id):

        emprestimo = self.repo.buscar_emprestimo(emprestimo_id)

        if emprestimo is None or emprestimo.devolvido:
            return None

        hoje = datetime.date.today()
        atraso = (hoje - emprestimo.data_devolucao).days

        equipamento = self.repo.buscar_equipamento(
            emprestimo.equipamento_id
        )

        multa = equipamento.calcular_multa(atraso)

        self.repo.marcar_devolvido(emprestimo_id)
        self.repo.marcar_disponivel(emprestimo.equipamento_id)

        self.notificar(
            Evento(
                tipo="devolucao",
                email=emprestimo.usuario_email,
                multa=multa
            )
        )

        return multa

    def listar_atrasados(self):

        lista = self.repo.listar_emprestimos()
        hoje = datetime.date.today()

        atrasos = []

        for emp in lista:
            if not emp.devolvido and emp.data_devolucao < hoje:

                atraso = (hoje - emp.data_devolucao).days

                equipamento = self.repo.buscar_equipamento(
                    emp.equipamento_id
                )

                multa = equipamento.calcular_multa(atraso)

                atrasos.append((emp, atraso, multa))

                self._notificar_atraso(emp)

        if len(atrasos) == 0:
            return []

        return atrasos

    def calcular_multa(self, emprestimo):
        hoje = datetime.date.today()
        atraso = (hoje - emprestimo.data_devolucao).days

        equipamento = self.repo.buscar_equipamento(
            emprestimo.equipamento_id
        )

        return equipamento.calcular_multa(atraso)

    def _notificar_atraso(self, emprestimo):
        self.notificar(
            Evento(
                tipo="atraso",
                email=emprestimo.usuario_email
            )
        )
