from services.interfaces import INotificador


class Notificador(INotificador):

    def notificar_emprestimo(self, email, data_devolucao):
        print(f"[EMAIL] {email} — empréstimo registrado. Devolução até {data_devolucao}.")

    def notificar_devolucao(self, email, multa):
        print(f"[EMAIL] {email} — devolução confirmada. Multa: R${multa:.2f}")

    def notificar_atraso(self, email):
        print(f"[EMAIL] {email} — você possui um empréstimo em atraso!")
