
# Beleza Exemplo — Sistema de Agendamento

## Sobre o projeto

O Beleza Exemplo é um sistema web de agendamento desenvolvido como MVP (Produto Mínimo Viável) para auxiliar na gestão de pequenos salões de beleza.

O projeto busca substituir o controle manual de agendamentos por uma plataforma digital, proporcionando maior organização, redução de conflitos de horários e facilidade no gerenciamento de clientes e serviços.

## Objetivos

- Digitalizar os agendamentos do salão.
- Reduzir conflitos de horários.
- Facilitar o cadastro e a consulta de clientes.
- Melhorar a organização dos atendimentos.
- Otimizar a rotina dos funcionários.

## Funcionalidades

- Login de funcionários.
- Painel inicial de atendimentos.
- Cadastro e edição de clientes.
- Cadastro de serviços.
- Calendário de agendamentos.
- Consulta de horários disponíveis.
- Criação de novos agendamentos.
- Confirmação, remarcação e cancelamento.
- Busca por cliente ou serviço.
- Validação de conflitos de horários.
- Interface responsiva.

## Tecnologias utilizadas

- Python 3.12
- Flask
- Flask-SQLAlchemy
- Flask-Login
- MySQL
- SQLite
- HTML5
- CSS3
- JavaScript
- Pytest
- Git e GitHub

## Arquitetura do sistema

O projeto utiliza a arquitetura MVC (Model-View-Controller), separando os dados, as regras de negócio e a interface do usuário.

- Model: gerenciamento dos dados.
- View: interface e apresentação das informações.
- Controller: processamento das solicitações e controle das funcionalidades.

## Estrutura do projeto

```text
beleza-salao/
├── app/
│   ├── templates/
│   ├── static/
│   ├── models.py
│   ├── routes.py
│   └── domain.py
├── tests/
├── docs/
├── requirements.txt
├── docker-compose.yml
├── run.py
└── README.md
```

## Como executar o projeto

Instale o Python 3.12 e execute os comandos abaixo na pasta do projeto:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m flask --app run init-db
.\.venv\Scripts\python.exe run.py
```

Acesse o sistema pelo navegador:

http://127.0.0.1:5000

## Acesso demonstrativo

- Usuário: funcionario
- Senha: beleza123

As credenciais são destinadas exclusivamente à demonstração acadêmica.

## Testes

O projeto possui testes unitários e de integração para verificar as regras de negócio e as principais funcionalidades do sistema.

Para executar os testes:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

## Versionamento

O Git e o GitHub são utilizados para controlar as alterações do código-fonte e registrar a evolução do desenvolvimento.

## Resultados esperados

Espera-se que o sistema contribua para a melhoria da organização dos atendimentos, redução de erros operacionais e maior eficiência no gerenciamento da agenda do salão.

## Melhorias futuras

- Agendamento online pelos clientes.
- Notificações automáticas.
- Integração com WhatsApp.
- Controle financeiro.
- Gerenciamento de múltiplos profissionais.
- Relatórios de atendimento.

## Finalidade acadêmica

Este projeto foi desenvolvido para fins acadêmicos, aplicando conhecimentos de engenharia de software, desenvolvimento web, banco de dados, testes e versionamento de código.

O sistema utiliza dados fictícios e não está destinado ao uso em produção.
