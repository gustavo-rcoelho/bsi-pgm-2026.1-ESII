# Diagrama DIP

```mermaid
classDiagram

class IRepositorioEmprestimo
class INotificador

class RepositorioEmprestimo
class Notificador
class ServicoEmprestimo

IRepositorioEmprestimo <|.. RepositorioEmprestimo
INotificador <|.. Notificador

ServicoEmprestimo --> IRepositorioEmprestimo
ServicoEmprestimo --> INotificador
```
