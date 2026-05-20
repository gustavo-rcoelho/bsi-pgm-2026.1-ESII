from repositories.repositorio_emprestimo import RepositorioEmprestimo
from services.notificador import Notificador
from services.servico_emprestimo import ServicoEmprestimo


def main():
    repositorio = RepositorioEmprestimo()
    notificador = Notificador()
    servico     = ServicoEmprestimo(repositorio, notificador)

    while True:
        print("\n1-Registrar  2-Devolver  3-Atrasados  0-Sair")
        opcao = input("Opção: ")

        if opcao == "1":
            ok = servico.registrar(
                int(input("ID equipamento: ")),
                input("Nome: "),
                input("Email: "),
                int(input("Dias: "))
            )

            if ok:
                print("Empréstimo registrado com sucesso.")
            else:
                print("Equipamento inválido ou indisponível.")

        elif opcao == "2":
            multa = servico.devolver(int(input("ID empréstimo: ")))

            if multa is None:
                print("Empréstimo inválido ou já devolvido.")
            else:
                print(f"Devolução registrada. Multa: R${multa:.2f}")

        elif opcao == "3":
            atrasados = servico.listar_atrasados()

            if not atrasados:
                print("Nenhum empréstimo em atraso.")
            else:
                for emp, dias, multa in atrasados:
                    print(f"{emp.usuario_nome} — {dias} dias de atraso — R${multa:.2f}")

        elif opcao == "0":
            break


if __name__ == "__main__":
    main()
