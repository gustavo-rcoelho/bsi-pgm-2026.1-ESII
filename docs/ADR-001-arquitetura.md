# ADR-001: Arquitetura da v2.0 do Sistema de Empréstimos

**Status:** Proposed 
**Data:** 2026-04-28

| Critério                                                   | Arquivo único                     | Em camadas                                          | MVC                                                  |
| ---------------------------------------------------------- | --------------------------------- | --------------------------------------------------- | ---------------------------------------------------- |
| **Atende RNF03 (novo tipo sem modificar vários módulos)?** |  Não — tudo está misturado       |  Sim — regras ficam isoladas em services/models   |  Sim — modelos separados                           |
| **Atende RNF04 (testar regras sem estado externo)?**       |  Não — depende de input, globals |  Sim — serviços podem receber repositórios falsos |  Sim — controllers podem ser testados isoladamente |
| **Adequado para CLI sem interface gráfica?**               |  Sim                            |  Sim                                              |  Não — MVC é mais útil p/ GUI                       |
| **Familiar para equipe iniciante?**                        |  Muito simples                  |  Complexidade moderada e compreensível            |  Alto custo e conceitos extras                      |

## Contexto

A versão 1.0 foi construída em um único arquivo (`emprestimos.py`).  
Essa estrutura não atende dois requisitos críticos:

- **RNF03 – Manutenibilidade:** adicionar um novo tipo de equipamento exige alterar múltiplas partes do código, pois regras, dados e interface estão misturados.
- **RNF04 – Testabilidade:** não é possível testar regras de negócio isoladamente, pois dependem de variáveis globais e entrada do usuário.

Para garantir evolução segura da v2.0, era necessário escolher uma organização arquitetural que reduzisse acoplamento e permitisse testes independentes.

## Opções consideradas

### 1. Arquivo único
- **Vantagens:** simples de implementar, familiar para iniciantes.
- **Desvantagens:** não atende RNF03 nem RNF04; código altamente acoplado.
- **Motivo do descarte:** mantém exatamente os problemas que a v2.0 deve resolver.

### 2. MVC
- **Vantagens:** separa responsabilidades; favorece testabilidade.
- **Desvantagens:** pensado para aplicações com interface gráfica; adiciona complexidade desnecessária para um CLI.
- **Motivo do descarte:** custo de complexidade maior que o necessário para o escopo do projeto.

### 3. Arquitetura em camadas
- **Vantagens:** separa regras, dados e interface; atende plenamente RNF03 e RNF04; fácil para equipe iniciante compreender.
- **Motivo da escolha:** entrega manutenibilidade e testabilidade sem criar sobrecarga conceitual.

## Decisão

Adotar **arquitetura em camadas**. A estrutura da v2.0 será organizada assim:

- `main.py`  
  Interface CLI (menu). Não contém regras de negócio.

- `services/`  
  Regras de negócio (empréstimos, devoluções, cálculo de multa).  
  Independente de interface e persistência.

- `repositorios/`  
  Persistência dos dados (listas, arquivos, futuro banco, etc.).  
  Pode ser substituído por repositório falso nos testes.

- `models/`  
  Representações das entidades do domínio: `Equipamento`, `Emprestimo`, etc.


## Consequências

### Positivas
- Atende **RNF03**: adicionar novo tipo de equipamento exigirá apenas criar/alterar uma entidade em `models/`.
- Atende **RNF04**: regras de negócio podem ser testadas isoladamente com repositórios falsos.
- Interface e lógica deixam de ser acopladas — CLI pode mudar sem afetar regras.
- Preparação para futura migração a banco de dados sem alterar a lógica central.

### Negativas / custos
- Maior número de arquivos comparado ao script único.
- Exige organização mínima e instrução da equipe.

