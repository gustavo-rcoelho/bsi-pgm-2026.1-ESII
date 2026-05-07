# Diagramas e Decomposição em Camadas

## Decomposição em camadas

- `models/Equipamento`
Representa a entidade de domínio equipamento. Possui apenas dados e alta coesão por entidade.

- `models/Emprestimo`
Representa a entidade de domínio empréstimo. Centraliza os dados relacionados ao empréstimo sem regras de interface.

- `services/ServicoEmprestimo`
Responsável pelas regras de negócio dos casos de uso UC01, UC02 e UC03. Possui alta coesão por concentrar apenas operações de empréstimo.

- `services/Notificador`
Responsável exclusivamente pelo envio de notificações. Separado para manter SRP e permitir mudança futura do canal de notificação.

- `repositories/RepositorioEmprestimo`
Responsável pelo acesso e persistência de dados. Oculta detalhes de armazenamento das demais camadas.

- `main.py`
Responsável apenas pela interface CLI e interação com o usuário. Não contém regras de negócio.

---

# Diagramas de sequência

## UC01 — Registrar Empréstimo

```mermaid
sequenceDiagram
    actor Atendente
    participant main as main.py
    participant servico as ServicoEmprestimo
    participant repo as RepositorioEmprestimo
    participant notif as Notificador

    Atendente->>main: informa equip_id, nome, email, dias
    main->>servico: registrar(equip_id, nome, email, dias)
    servico->>repo: buscar_equipamento(equip_id)
    repo-->>servico: Equipamento

    alt equipamento disponível
        servico->>repo: salvar_emprestimo(emprestimo)
        servico->>repo: marcar_indisponivel(equip_id)
        servico->>notif: notificar_emprestimo(email, data_devolucao)
        servico-->>main: True
    else equipamento indisponível
        servico-->>main: False
    end
```

## UC02 — Registrar Devolução

```mermaid
sequenceDiagram
    actor Atendente
    participant main as main.py
    participant servico as ServicoEmprestimo
    participant repo as RepositorioEmprestimo
    participant notif as Notificador

    Atendente->>main: informa emprestimo_id
    main->>servico: devolver(emprestimo_id)

    servico->>repo: buscar_emprestimo(emprestimo_id)
    repo-->>servico: Emprestimo

    alt empréstimo válido
        servico->>servico: calcular_multa(emprestimo)
        servico->>repo: marcar_devolvido(emprestimo_id)
        servico->>repo: marcar_disponivel(equipamento_id)
        servico->>notif: notificar_devolucao(email, multa)
        servico-->>main: multa
    else empréstimo inválido
        servico-->>main: erro
    end
```

## UC03 — Listar Empréstimos em Atraso

```mermaid
sequenceDiagram
    actor Coordenador
    participant main as main.py
    participant servico as ServicoEmprestimo
    participant repo as RepositorioEmprestimo
    participant notif as Notificador

    Coordenador->>main: solicita atrasados
    main->>servico: listar_atrasados()

    servico->>repo: listar_emprestimos()
    repo-->>servico: lista_emprestimos

    loop para cada empréstimo atrasado
        servico->>servico: calcular_multa(emprestimo)
        servico->>notif: notificar_atraso(email)
        servico-->>main: exibir_atrasado(nome, atraso, multa)
    end

    alt nenhum atraso
        servico-->>main: "Nenhum empréstimo em atraso"
    end
```
