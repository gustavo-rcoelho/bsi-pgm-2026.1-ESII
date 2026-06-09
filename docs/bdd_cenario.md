# Cenário: Limite de empréstimos simultâneos

Funcionalidade: Controle de empréstimos

Cenário: Usuário não pode registrar um quarto empréstimo

Dado que o usuário possui três empréstimos em aberto

E que existe um equipamento disponível para empréstimo

Quando o usuário tentar registrar um novo empréstimo

Então o sistema deve negar o empréstimo

E deve retornar falso
