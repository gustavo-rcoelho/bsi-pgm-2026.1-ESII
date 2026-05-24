## Aula 05 — OCP

Na implementação da hierarquia de equipamentos, o uso de classes abstratas e polimorfismo aplica diretamente o Princípio Aberto/Fechado (OCP), conforme descrito por Valente no Capítulo 5. O serviço de empréstimos deixa de depender de `if/elif`, e passa a depender apenas da interface estável `calcular_multa()`. Assim, o módulo fica fechado para modificação, mas aberto para extensão, pois adicionar um novo tipo exige apenas criar uma nova subclasse de `Equipamento`, sem alterar o serviço.

Entretanto, Valente enfatiza que o OCP não é um “escudo universal”: ele funciona bem quando as variações são previsíveis e organizáveis em uma hierarquia. Caso surja um requisito radicalmente distinto — por exemplo, multa por hora em vez de por dia, ou um cálculo que depende do dia da semana — nossa hierarquia atual talvez não seja suficiente. Isso exigiria reavaliar as abstrações centrais e possivelmente redefinir a classe base ou separar novas políticas de cálculo. Como Valente argumenta, “toda abstração tem um limite de aplicabilidade”; não devemos forçar o OCP além desses limites. Por isso, a solução funciona bem para os tipos atuais, mas mudanças mais amplas exigiriam reestruturação orientada à nova dimensão de variação.

## Aula 06 — Verificação de LSP

O contrato definido na classe abstrata `Equipamento` estabelece que o método
`calcular_multa(dias_atraso)` deve sempre retornar um `float >= 0` e nunca lançar
exceções inesperadas. Verificando cada subclasse:

- Notebook:
  - calcular_multa(0) → max(0, 0) = 0.0
  - calcular_multa(-5) → max(0, -50) = 0.0
- Projetor:
  - calcular_multa(0) → 0.0
  - calcular_multa(-5) → 0.0
- Cabo:
  - calcular_multa(0) → 0.0
  - calcular_multa(-5) → 0.0

Todas as subclasses retornam um valor float não-negativo, mesmo quando a entrada é
negativa, graças ao uso consistente de `max(0, ...)`. Nenhuma lança exceções,
independentemente do valor de dias_atraso.

Portanto, todas as subclasses honram integralmente o contrato definido pela classe base.
Segundo Valente (Cap. 5), uma subclasse satisfaz LSP quando pode ser usada no lugar da
classe pai sem quebrar o funcionamento do sistema. Este é exatamente o caso: o
ServicoEmprestimo funciona corretamente com qualquer subclasse de Equipamento.

## Aula 06 — DIP     

 Antes da refatoração, o serviço de empréstimos dependia diretamente de implementações concretas do repositório e do notificador, o que tornava difícil testar o comportamento isoladamente. Para verificar um fluxo simples de empréstimo, era necessário usar o repositório real e um notificador real, criando efeitos colaterais indesejados. Isso viola o DIP porque o módulo de alto nível (Serviço) estava acoplado a detalhes de baixo nível.

Após a aplicação do DIP, o serviço passou a depender apenas de abstrações implícitas, ou seja, qualquer objeto que forneça os métodos necessários pode ser usado. Assim, criamos doubles (como RepositorioFalso e NotificadorFalso) para testes. Isso permitiu testar o serviço sem modificar seu código e sem precisar do restante do sistema. Esse desacoplamento melhora a reutilização, facilita manutenção e torna o sistema mais estável a mudanças.

Segundo Valente (Cap. 5), o DIP “reduz o impacto das alterações em módulos concretos ao forçar que módulos estáveis dependam de abstrações”. Ele também destaca que a inversão de dependências é crucial para permitir testes automatizados de forma simples e confiável. A atividade demonstrou exatamente isso: substituindo implementações reais por dublês, o módulo de alto nível pôde ser testado de maneira previsível e isolada.

Essa refatoração tornou o código mais flexível, menos acoplado e mais alinhado aos princípios de boas práticas de projeto.