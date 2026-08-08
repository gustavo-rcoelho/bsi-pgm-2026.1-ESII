# Diagnóstico — Aula 12: Refactoring e Code Smells

## Objetivo

Este diagnóstico identifica code smells presentes ou aparentes no código do sistema de empréstimos. A análise considera os princípios de refactoring apresentados na Aula 12, especialmente Mysterious Name, Inline Variable e Data Class como falso positivo.

O objetivo dos refactorings é melhorar a estrutura e a legibilidade do código sem alterar o comportamento observável do sistema.

---

## 1. `repositorios/interfaces.py` — parâmetros `equip_id`

**Smell:** Mysterious Name

**Refactoring proposto:** Rename

**Local:** métodos `buscar_equipamento` e `marcar_indisponivel`.

**Justificativa:**
O nome `equip_id` é uma abreviação que não deixa tão explícito que o valor representa o identificador de um equipamento. O restante do sistema utiliza o nome `equipamento_id`, que comunica melhor a intenção do parâmetro.

Uma renomeação para `equipamento_id` deixaria a interface consistente com os demais módulos do sistema e reduziria a necessidade de interpretar abreviações.

**Situação:** melhoria identificada. O serviço `ServicoEmprestimo` já foi refatorado para utilizar `equipamento_id`, mas a interface ainda possui ocorrências de `equip_id`.

---

## 2. `repositorios/repositorio_emprestimo.py` — variável `criar`

**Smell:** Mysterious Name

**Refactoring proposto:** Rename ou Inline Variable

**Local:** método `__init__`.

**Justificativa:**
A variável local `criar` recebe uma referência para `FabricaEquipamento.criar`. Apesar de funcionar corretamente, o nome é genérico e não revela que se trata do método responsável pela criação de equipamentos através da fábrica.

Além disso, a variável é utilizada apenas para chamar o método de criação. O código poderia utilizar diretamente `FabricaEquipamento.criar(...)`, eliminando a indireção desnecessária por meio de **Inline Variable**.

**Situação:** refactoring recomendado.

---

## 3. `repositorios/repositorio_emprestimo.py` — variável `e`

**Smell:** Mysterious Name

**Refactoring proposto:** Rename

**Local:** métodos `buscar_equipamento`, `buscar_emprestimo` e `marcar_devolvido`.

**Justificativa:**
A variável `e` representa objetos diferentes dependendo do método: em alguns casos representa um equipamento e em outro representa um empréstimo. O nome de uma única letra não comunica sua intenção.

Por exemplo, em `buscar_equipamento`, um nome como `equipamento` tornaria o código mais explícito:

```python
for equipamento in self.equipamentos:
    if equipamento.id == equip_id:
        return equipamento
```

Da mesma forma, em `buscar_emprestimo`, o nome `emprestimo` seria mais expressivo.

**Situação:** refactoring recomendado.

---

## 4. `models/equipamento.py` — subclasses `Notebook`, `Projetor` e `Cabo`

**Smell aparente:** Data Class

**Refactoring proposto:** Não refatorar — falso positivo

**Local:** classes `Notebook`, `Projetor` e `Cabo`.

**Justificativa:**
As três subclasses atualmente não possuem comportamento próprio e contêm apenas `pass`. À primeira vista, isso pode parecer um caso de Data Class ou de classes desnecessárias.

Entretanto, esse é um **falso positivo**. As subclasses representam explicitamente os diferentes tipos de equipamento existentes no domínio. Além disso, o cálculo da multa foi transferido para o padrão Strategy na Aula 11, por meio de `MultaStrategy` e `MultaPorDia`.

Eliminar essas subclasses com um `Inline Class` ou devolver o cálculo de multa para elas faria com que parte da solução obtida com Strategy e OCP fosse perdida.

Portanto, apesar da aparência de smell, as subclasses devem permanecer.

**Situação:** não refatorado por decisão de design.

---

## 5. `models/emprestimo.py` — classe `Emprestimo`

**Smell aparente:** Data Class

**Refactoring proposto:** Não refatorar — estrutura de dados intencional

**Local:** classe `Emprestimo`.

**Justificativa:**
`Emprestimo` é uma `@dataclass` composta principalmente por dados: identificador, equipamento, usuário, datas e estado de devolução.

Apesar de possuir pouca lógica própria, isso não significa automaticamente que exista um code smell. A classe representa uma entidade do domínio e é utilizada para transportar e armazenar os dados de um empréstimo entre as diferentes partes do sistema.

De acordo com a discussão da Aula 12, uma classe composta por dados somente é um smell quando se esperava que ela também concentrasse comportamento. Nesse caso, a estrutura é deliberada e não há evidência suficiente para justificar sua transformação.

**Situação:** não refatorado.

---

## 6. `repositorios/repositorio_emprestimo.py` — métodos de busca com lógica repetida

**Smell:** Duplicated Code

**Refactoring proposto:** Extract Function / Move Function, caso a duplicação aumente

**Local:** `buscar_equipamento` e `buscar_emprestimo`.

**Justificativa:**
Os dois métodos possuem uma estrutura semelhante: percorrem uma coleção, comparam o identificador e retornam o objeto correspondente ou `None`.

Atualmente a duplicação é pequena e os métodos possuem responsabilidades claramente distintas, portanto não é necessário realizar uma refatoração agressiva apenas para eliminar algumas linhas semelhantes.

Ainda assim, a repetição pode ser observada como um ponto de atenção para futuras evoluções do repositório. Caso surjam outras operações de busca com a mesma estrutura, poderá ser justificável extrair uma função auxiliar genérica.

**Situação:** identificado como ponto de atenção; refactoring não considerado necessário neste momento.

---

## Resumo dos smells

| # | Arquivo                                  | Smell               | Refactoring              | Situação              |
| - | ---------------------------------------- | ------------------- | ------------------------ | --------------------- |
| 1 | `repositorios/interfaces.py`             | Mysterious Name     | Rename                   | Recomendado           |
| 2 | `repositorios/repositorio_emprestimo.py` | Mysterious Name     | Rename / Inline Variable | Recomendado           |
| 3 | `repositorios/repositorio_emprestimo.py` | Mysterious Name     | Rename                   | Recomendado           |
| 4 | `models/equipamento.py`                  | Data Class aparente | Não refatorar            | Falso positivo        |
| 5 | `models/emprestimo.py`                   | Data Class aparente | Não refatorar            | Estrutura intencional |
| 6 | `repositorios/repositorio_emprestimo.py` | Duplicated Code     | Extract Function         | Ponto de atenção      |

## Conclusão

A análise mostra que os principais problemas restantes são relacionados à clareza dos nomes e a pequenas repetições no código. O `ServicoEmprestimo` já recebeu refactorings importantes durante a Aula 12, incluindo a substituição do evento baseado em `dict` por `Evento`, a melhoria de nomes e a extração da notificação de atraso.

Também foram identificados casos que aparentam ser code smells, mas que não devem ser modificados. As subclasses `Notebook`, `Projetor` e `Cabo` são um exemplo importante: embora estejam vazias após a aplicação de Strategy, elas possuem uma função de representação dos tipos de equipamento e sua remoção poderia desfazer decisões arquiteturais da Aula 11.

Assim, o diagnóstico não considera que todo código aparentemente simples ou sem comportamento próprio precise ser refatorado. A decisão de refatorar deve considerar a intenção do design e o impacto sobre os princípios já aplicados ao sistema.
