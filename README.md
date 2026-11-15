# Beleza Exemplo — Sistema de Agendamento

MVP acadêmico de um sistema web para pequenos salões de beleza. O objetivo é substituir a agenda física e a organização manual por WhatsApp por uma agenda centralizada, reduzindo conflitos e facilitando cancelamentos e remarcações.

## Funcionalidades

- Login de funcionário e encerramento de sessão.
- Painel inicial com total de atendimentos do dia e próximo agendamento.
- Cadastro, consulta e edição de clientes.
- Cadastro de serviços com duração e configuração do expediente.
- Cadastro, consulta, confirmação, edição, remarcação e cancelamento de agendamentos.
- Filtros por data, cliente, serviço, próximos atendimentos e cancelados.
- Calendário, horários disponíveis e validação de sobreposição e expediente no servidor.
- Interface responsiva inspirada nos protótipos acadêmicos.

## Tecnologias e arquitetura

Python 3.12, Flask 3.1, Flask-SQLAlchemy 3.1, Flask-Login, PyMySQL, MySQL 8.0 (opcionalmente SQLite para demonstração), HTML, CSS próprio, JavaScript e pytest. O projeto segue uma arquitetura monolítica MVC: `models.py` representa o modelo, `routes.py` o controlador e `templates/` as telas. O módulo `domain.py` contém as regras de negócio. A implementação usa CSS próprio em vez de Bootstrap para reproduzir a identidade visual sem depender de CDN.

## Como executar (Windows)

Instale Python 3.12 e abra o PowerShell na pasta do projeto:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m flask --app run init-db
.\.venv\Scripts\python.exe run.py
```

Acesse http://127.0.0.1:5000 no navegador.

**Usuário demonstrativo:** `funcionario`  
**Senha demonstrativa:** `beleza123`

O comando `init-db` cria as tabelas e dados fictícios. A agenda demonstrativa é preenchida para o dia seguinte à inicialização. Acesse a aba Próximos agendamentos ou selecione esse dia. A base SQLite fica em `instance/`, ignorada pelo Git.

### Linux/macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m flask --app run init-db
python run.py
```

### MySQL 8.0 (alternativa conforme arquitetura proposta)

Com Docker Desktop e Docker Compose instalados, execute `docker compose up -d` e aguarde o banco ficar saudável (`docker compose ps`). No PowerShell:

```powershell
$env:DATABASE_URL = 'mysql+pymysql://beleza:beleza_local@127.0.0.1:3306/beleza?charset=utf8mb4'
.\.venv\Scripts\python.exe -m flask --app run init-db
.\.venv\Scripts\python.exe run.py
```

As credenciais do Compose são exclusivamente para uso local e acadêmico. Para outros ambientes, configure `DATABASE_URL`, `SECRET_KEY`, `DEMO_USERNAME` e `DEMO_PASSWORD` antes de inicializar o banco. As credenciais demonstrativas não devem ser usadas em produção. A chave de sessão aleatória padrão é adequada apenas para desenvolvimento local, pois muda a cada reinício.

## Testes

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

O workflow `.github/workflows/tests.yml` instala as dependências e roda os testes a cada push ou pull request no GitHub. Os testes incluem regras de conflito, horário de funcionamento, login, agendamento, remarcação, cancelamento, clientes e disponibilidade.

## Estrutura

```text
app/
  __init__.py       # aplicação, sessão, CSRF e inicialização
  models.py         # entidades e banco de dados
  routes.py         # controladores e rotas HTTP
  domain.py         # regras de negócio
  templates/        # páginas HTML/Jinja
  static/           # CSS e JavaScript
tests/              # testes unitários e de integração
docs/               # documentação acadêmica
.github/workflows/  # integração contínua
run.py              # ponto de entrada
requirements.txt    # dependências
docker-compose.yml  # opção de banco MySQL
```

## Limites do MVP

Agenda única do salão (um atendimento por vez); sem pagamentos, notificações automáticas, controle financeiro, recuperação de senha ou perfis de múltiplos profissionais. A prevenção de conflitos é feita na aplicação, adequada à demonstração de um operador; concorrência simultânea em produção exigiria proteção transacional adicional. Não é um serviço hospedado nem um sistema pronto para produção. Use somente dados fictícios no repositório público.

## Publicação

Consulte [docs/PUBLICAR.md](docs/PUBLICAR.md) para enviar este projeto ao GitHub preservando o histórico de commits.
