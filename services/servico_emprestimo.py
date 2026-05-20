from models.emprestimo import Emprestimo
import datetime

class ServicoEmprestimo:

    def __init__(self, repo, notificador):
        self.repo = repo
        self.notificador = notificador

    def registrar(self, equip_id, nome, email, dias):

        equipamento = self.repo.buscar_equipamento(equip_id)

        if equipamento is None or not equipamento.disponivel:
            return False

        hoje = datetime.date.today()
        data_devolucao = hoje + datetime.timedelta(days=dias)

        emprestimo = Emprestimo(
            id=len(self.repo.emprestimos) + 1,
            equipamento_id=equip_id,
            equipamento_nome=equipamento.nome,
            tipo=equipamento.tipo,
            usuario_nome=nome,
            usuario_email=email,
            data_emprestimo=hoje,
            data_devolucao=data_devolucao,
            devolvido=False
        )

        self.repo.salvar_emprestimo(emprestimo)
        self.repo.marcar_indisponivel(equip_id)

        self.notificador.notificar_emprestimo(email, data_devolucao)

        return True

    def devolver(self, emprestimo_id):

        emprestimo = self.repo.buscar_emprestimo(emprestimo_id)

        if emprestimo is None or emprestimo.devolvido:
            return None  

        hoje = datetime.date.today()
        atraso = (hoje - emprestimo.data_devolucao).days

        equipamento = self.repo.buscar_equipamento(emprestimo.equipamento_id)
        multa = equipamento.calcular_multa(atraso)

        self.repo.marcar_devolvido(emprestimo_id)
        self.repo.marcar_disponivel(emprestimo.equipamento_id)

        self.notificador.notificar_devolucao(
            emprestimo.usuario_email,
            multa
        )

        return multa

    def listar_atrasados(self):

        lista = self.repo.listar_emprestimos()
        hoje = datetime.date.today()

        atrasos = []

        for emp in lista:
            if not emp.devolvido and emp.data_devolucao < hoje:

                atraso = (hoje - emp.data_devolucao).days
                equipamento = self.repo.buscar_equipamento(emp.equipamento_id)

                multa = equipamento.calcular_multa(atraso)

                atrasos.append((emp, atraso, multa))

                self.notificador.notificar_atraso(emp.usuario_email)

        if len(atrasos) == 0:
            return []

        return atrasos

    def calcular_multa(self, emprestimo):
        hoje = datetime.date.today()
        atraso = (hoje - emprestimo.data_devolucao).days
        equipamento = self.repo.buscar_equipamento(emprestimo.equipamento_id)
        return equipamento.calcular_multa(atraso)
