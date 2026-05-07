# Diagramação em Camadas

main.py
services/
repositorios/
models/
notificador/

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


