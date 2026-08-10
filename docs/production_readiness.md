# Production Readiness Checklist

## 1. Pipeline e qualidade

| Item                                      | Status     | Esforço | Prioridade | Observação                                                                                           |
| ----------------------------------------- | ---------- | ------: | ---------- | ---------------------------------------------------------------------------------------------------- |
| Lint com Ruff executado no CI             | ✅ OK       |   feito | alta       | O pipeline executa `ruff check .` e a verificação está passando.                                     |
| Testes automatizados no CI                | ✅ OK       |   feito | alta       | A suíte possui 36 testes e todos estão passando.                                                     |
| Gate de cobertura mínima                  | ✅ OK       |   feito | alta       | O gate está configurado em 80% e a cobertura atual é de 91,63%.                                      |
| Cobertura mantida nas próximas alterações | ⚠️ PARCIAL |   1–2 h | alta       | O gate impede queda abaixo de 80%, mas novos testes ainda precisam acompanhar novas funcionalidades. |

**Avaliação:** O pipeline já possui lint, testes e gate de cobertura. É a categoria mais próxima de produção, embora a manutenção da cobertura continue sendo necessária.

---

## 2. Containerização

| Item                                            | Status     |    Esforço | Prioridade | Observação                                                           |
| ----------------------------------------------- | ---------- | ---------: | ---------- | -------------------------------------------------------------------- |
| Dockerfile para build da aplicação              | ❌ FALTA    |      2–4 h | média      | O repositório não possui Dockerfile.                                 |
| Build reprodutível da aplicação                 | ❌ FALTA    |      2–4 h | média      | Ainda não existe uma receita de build em container versionada.       |
| Imagem executando sem root                      | ❌ FALTA    |      1–2 h | baixa      | Não há configuração de usuário não-root em container.                |
| Exclusão de arquivos desnecessários do contexto | ⚠️ PARCIAL | 30 min–1 h | baixa      | O projeto possui `.gitignore`, mas ainda não possui `.dockerignore`. |

**Avaliação:** A aplicação ainda não possui estratégia de containerização. Essa etapa seria necessária para obter um ambiente de execução mais reprodutível.

---

## 3. Persistência

| Item                                               | Status  |  Esforço | Prioridade | Observação                                                                                   |
| -------------------------------------------------- | ------- | -------: | ---------- | -------------------------------------------------------------------------------------------- |
| Empréstimos sobrevivem ao encerramento do programa | ❌ FALTA | 1–2 dias | alta       | Os empréstimos são mantidos pelo repositório em memória e não há banco de dados persistente. |
| Equipamentos e seus estados são persistidos        | ❌ FALTA | 1–2 dias | alta       | O estado de disponibilidade dos equipamentos não é armazenado de forma permanente.           |
| Backup dos dados                                   | ❌ FALTA | 1–2 dias | média      | Não existe mecanismo de backup porque ainda não existe persistência externa.                 |
| Recuperação dos dados após reinício                | ❌ FALTA |    1 dia | alta       | Ao encerrar o processo, os dados mantidos em memória deixam de estar disponíveis.            |

**Avaliação:** Persistência é uma das principais lacunas para produção. O sistema funciona durante a execução, mas não possui armazenamento permanente dos dados dos empréstimos.

---

## 4. Segurança

| Item                                        | Status     | Esforço | Prioridade | Observação                                                                                                                |
| ------------------------------------------- | ---------- | ------: | ---------- | ------------------------------------------------------------------------------------------------------------------------- |
| Credenciais fora do código-fonte            | ⚠️ PARCIAL |   2–4 h | alta       | Não há infraestrutura de produção configurada para gerenciamento de segredos.                                             |
| Validação das entradas                      | ⚠️ PARCIAL |   4–8 h | alta       | Existem validações no domínio, mas seria necessário revisar todas as entradas recebidas pela aplicação antes de produção. |
| Dependências de desenvolvimento versionadas | ✅ OK       |   feito | média      | `requirements-dev.txt` está versionado e inclui as ferramentas utilizadas no CI.                                          |
| Auditoria automatizada das dependências     | ❌ FALTA    |   2–4 h | média      | Não há etapa de auditoria de vulnerabilidades das dependências no pipeline.                                               |

**Avaliação:** Existem algumas proteções no código, mas ainda seria necessária uma revisão de segurança antes de disponibilizar o sistema em produção.

---

## 5. Observabilidade

| Item                                | Status     |  Esforço | Prioridade | Observação                                                                                                            |
| ----------------------------------- | ---------- | -------: | ---------- | --------------------------------------------------------------------------------------------------------------------- |
| Logs estruturados da aplicação      | ❌ FALTA    |    4–8 h | alta       | O sistema possui mensagens de saída, mas não há uma estratégia estruturada de logging com níveis e destino definidos. |
| Métricas da aplicação               | ❌ FALTA    | 1–2 dias | média      | Não existem métricas para acompanhar uso, erros ou desempenho.                                                        |
| Investigação de falhas anteriores   | ⚠️ PARCIAL |    1 dia | alta       | Sem armazenamento centralizado de logs, investigar uma falha ocorrida anteriormente seria limitado.                   |
| Monitoramento de saúde da aplicação | ❌ FALTA    |    4–8 h | média      | Não existe mecanismo de health check ou monitoramento de disponibilidade.                                             |

**Avaliação:** A observabilidade ainda é insuficiente para produção. O principal problema é a ausência de uma estratégia de logs persistentes e métricas que permita diagnosticar problemas após sua ocorrência.

---

## 6. Deployment

| Item                                | Status     |  Esforço | Prioridade | Observação                                                                                                            |
| ----------------------------------- | ---------- | -------: | ---------- | --------------------------------------------------------------------------------------------------------------------- |
| Processo automatizado de deployment | ❌ FALTA    | 1–2 dias | alta       | O GitHub Actions atualmente verifica a qualidade do código, mas não realiza deployment da aplicação.                  |
| Estratégia de rollback              | ❌ FALTA    |    4–8 h | alta       | Não existe procedimento automatizado ou documentado para retornar à versão anterior após uma falha.                   |
| Ambiente de produção configurado    | ❌ FALTA    | 1–2 dias | alta       | O projeto ainda não possui um ambiente de produção configurado.                                                       |
| Aprovação antes da publicação       | ⚠️ PARCIAL |    2–4 h | média      | O uso de branch e Pull Request permite revisão, mas não existe um fluxo formal de aprovação e publicação em produção. |

**Avaliação:** O CI já verifica o código, mas ainda não existe a etapa de entrega contínua para um ambiente de produção. Deployment e rollback precisam ser definidos antes da publicação real.

---

## Síntese executiva

Para tornar o sistema pronto para produção, eu atacaria primeiro a **persistência**, depois a **segurança** e, em terceiro lugar, o **deployment**. A persistência é a primeira prioridade porque atualmente os empréstimos e estados dos equipamentos são mantidos em memória, fazendo com que os dados sejam perdidos quando o processo termina. Além de representar um risco alto, essa etapa é uma dependência para outras melhorias, como backup e recuperação de dados.

Em seguida, eu priorizaria a segurança, principalmente a validação completa das entradas e o tratamento adequado de credenciais. Com os dados persistidos e as principais questões de segurança resolvidas, seria possível estruturar o deployment com maior confiança. Fazer o deployment antes dessas etapas aumentaria o risco de disponibilizar uma aplicação que pode perder dados e ainda não possui controles suficientes para um ambiente real.

O terceiro item seria o deployment, incluindo uma estratégia clara de publicação e rollback. O pipeline de CI já fornece uma base importante, pois atualmente executa lint, testes e gate de cobertura, mantendo a cobertura acima do limite exigido. A cobertura atual de 91,63% também reduz o risco de alterações quebrarem comportamentos já testados.

A **containerização** pode esperar em relação às três primeiras prioridades. Embora um Dockerfile torne o ambiente mais reprodutível e facilite a implantação, ele não resolve o problema mais crítico do sistema: a ausência de persistência. Portanto, considerando risco, esforço e dependências, faz mais sentido primeiro garantir que os dados sejam preservados e que o sistema tenha requisitos mínimos de segurança antes de investir na infraestrutura de execução.
