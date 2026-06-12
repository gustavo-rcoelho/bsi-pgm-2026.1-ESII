from app.sistema import SistemaDeEmprestimos


def main():
    sistema = SistemaDeEmprestimos()

    while True:
        print("\n1-Registrar  2-Devolver  3-Atrasados  0-Sair")
        opcao = input("Opção: ")

        if opcao == "1":
            ok = sistema.registrar(
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
            multa = sistema.devolver(int(input("ID empréstimo: ")))

            if multa is None:
                print("Empréstimo inválido ou já devolvido.")
            else:
                print(f"Devolução registrada. Multa: R${multa:.2f}")

        elif opcao == "3":
            atrasados = sistema.listar_atrasados()

            if not atrasados:
                print("Nenhum empréstimo em atraso.")
            else:
                for emp, dias, multa in atrasados:
                    print(f"{emp.usuario_nome} — {dias} dias de atraso — R${multa:.2f}")

        elif opcao == "0":
            break


if __name__ == "__main__":
    main()
