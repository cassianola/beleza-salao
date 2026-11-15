# Escopo acadêmico

## Problema
Pequenos salões frequentemente organizam os atendimentos por mensagens e agenda física. Isso dificulta visualizar horários livres, aumenta a possibilidade de conflitos e torna a remarcação menos organizada.

## Solução
Sistema web de agenda para o funcionário do salão, com cadastro de clientes e serviços, consulta dos horários, confirmação, cancelamento e remarcação.

## Requisitos funcionais
| ID | Requisito |
|---|---|
| RF01 | Autenticar o funcionário. |
| RF02 | Cadastrar, consultar e editar clientes. |
| RF03 | Cadastrar serviços e suas durações. |
| RF04 | Configurar horário de funcionamento. |
| RF05 | Registrar atendimento com cliente, serviço, data, horário e observações. |
| RF06 | Impedir agendamentos conflitantes e fora do expediente. |
| RF07 | Consultar, filtrar, confirmar, remarcar e cancelar agendamentos. |
| RF08 | Exibir resumo da agenda no painel inicial. |

## Requisitos não funcionais
Interface responsiva; autenticação com senha armazenada como hash; formulários protegidos contra CSRF; persistência relacional; código versionado e testes automatizados.

## Fluxo de apresentação
1. Entrar com a conta de demonstração.
2. Abrir Clientes e cadastrar um cliente fictício.
3. Abrir Agendamentos e selecionar Novo Agendamento.
4. Selecionar cliente, serviço, uma data futura e horário disponível.
5. Salvar e verificar mensagem de sucesso e tabela.
6. Tentar cadastrar um horário sobreposto e observar a mensagem de erro.
7. Editar o agendamento, confirmar e cancelar; conferir a aba Cancelados.

## Modelo de dados
- User: login e hash da senha.
- Client: nome, telefone e e-mail.
- Service: nome e duração.
- Settings: abertura e fechamento.
- Appointment: chaves de cliente e serviço, data, início, duração, observações e status.

## Exclusões
Pagamentos, notificações, controle financeiro e gestão de vários profissionais não integram este MVP.
