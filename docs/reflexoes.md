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

## Aula 08 — DIP com Interfaces

A introdução de interfaces explícitas fortaleceu a aplicação do Princípio da Inversão de Dependências. Antes, o serviço de empréstimos dependia diretamente das implementações concretas de repositório e notificador. Após a criação das interfaces `IRepositorioEmprestimo` e `INotificador`, o serviço passou a depender apenas de abstrações. Isso reduz acoplamento e facilita substituições futuras.

O teste com objetos falsos demonstrou uma das principais vantagens do DIP: a possibilidade de validar regras de negócio sem utilizar componentes reais do sistema. Dessa forma, o serviço pode ser testado de maneira isolada e previsível.

Entretanto, ainda existem dependências concretas remanescentes, como o uso direto de `datetime.date.today()`, a instanciação direta de `Emprestimo` e o acesso ao atributo `repo.emprestimos`. Esses pontos mostram que a aplicação do DIP é gradual e pode ser ampliada conforme a evolução do projeto.

Conforme discutido por Valente, a inversão de dependências busca reduzir o impacto de mudanças em módulos de baixo nível, permitindo que módulos de alto nível permaneçam estáveis. O uso de interfaces torna a arquitetura mais flexível, facilita testes e melhora a manutenção do software ao longo do tempo.

## Aula 08 — Testes

Os testes de integração verificam a colaboração entre componentes reais do sistema. No caso do sistema de empréstimos, o teste de integração garante que o ServiçoEmprestimo consegue interagir corretamente com o RepositorioEmprestimo e com o Notificador, validando que os objetos se comunicam de forma adequada quando executados em conjunto. Esse tipo de teste captura problemas de configuração, dependências incorretas, falhas de integração e incompatibilidades entre módulos, situações que normalmente não aparecem em testes de unidade.

Por outro lado, os testes de integração possuem menor capacidade de isolar defeitos. Quando um teste falha, pode ser mais difícil identificar exatamente qual componente causou o problema. Já os testes de unidade utilizam dublês como fakes e spies para isolar o comportamento da classe sob teste, permitindo validar regras específicas de negócio com maior precisão. Assim, testes de unidade são mais adequados para verificar cálculos de multa, regras de devolução e notificações individualmente, enquanto testes de integração garantem que o fluxo completo do sistema funciona corretamente quando os componentes reais são utilizados em conjunto.

## Aula 09 — TDD

Os testes TDD e os cenários BDD possuem objetivos diferentes. O teste TDD é mais adequado para desenvolvedores, pois descreve exatamente o comportamento esperado do código por meio de asserts e permite validar rapidamente se uma funcionalidade continua funcionando após alterações. Já o cenário BDD utiliza uma linguagem mais próxima do negócio, facilitando a comunicação com clientes, usuários e demais stakeholders que não possuem conhecimento técnico.

Para um cliente não técnico, o formato Dado-Quando-Então é mais fácil de compreender porque descreve situações reais de uso sem expor detalhes de implementação. Por outro lado, durante o desenvolvimento, prefiro utilizar TDD, pois fornece feedback imediato e ajuda a construir o código de forma incremental e segura. Já o BDD é mais útil para documentar requisitos e alinhar expectativas entre equipe técnica e negócio.

## Aula 10 — Factory e Facade

A Factory ajuda a concentrar a decisão de qual classe concreta deve ser criada a partir de um tipo. Embora exista um if/elif ou um mapa relacionando tipos às classes, esse acoplamento fica isolado em um único ponto do sistema. Isso é compatível com o princípio Open/Closed (OCP), pois o restante da aplicação não precisa conhecer as subclasses concretas. No meu projeto, o repositório passou a utilizar a FabricaEquipamento para criar Notebook, Projetor e Cabo, ficando desacoplado dessas classes. Assim, caso seja necessário adicionar um novo tipo de equipamento, a alteração fica concentrada na fábrica, evitando mudanças espalhadas pelo código.

A aplicação do padrão Facade não desfaz o DIP implementado anteriormente. A classe SistemaDeEmprestimos funciona como uma raiz de composição, responsável por instanciar e conectar os objetos concretos do sistema. A lógica de negócio continua localizada em ServicoEmprestimo, que ainda depende de abstrações e pode receber dublês durante os testes. Por isso, os testes permaneceram inalterados e continuam injetando repositórios e notificadores falsos diretamente no serviço. A fachada apenas simplifica o uso do subsistema pelo main.py, sem introduzir novas dependências ou regras de negócio. Conforme discutido por Valente no Capítulo 6, Factory e Facade ajudam a reduzir acoplamento e melhorar a organização estrutural do sistema.
