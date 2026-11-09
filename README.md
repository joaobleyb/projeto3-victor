# Sistema de Gerenciamento de Clínica

Sistema web desenvolvido em **Python** e **Django** para organizar os médicos, pacientes e consultas de uma clínica médica, substituindo o agendamento manual.

## Funcionalidades

- **Pacientes:** cadastrar, listar, editar e excluir.
- **Médicos:** cadastrar, listar, editar e excluir (cada médico pertence a uma especialidade).
- **Especialidades:** cadastrar e consultar, com a quantidade de médicos de cada uma.
- **Consultas:**
  - agendar selecionando paciente, médico, data e horário;
  - listar as consultas com o paciente, o médico e a especialidade;
  - filtrar por status, médico, paciente e data;
  - alterar o status (Agendada, Realizada ou Cancelada).

## Regras de negócio

- Um paciente pode ter várias consultas.
- Um médico pode realizar várias consultas.
- Cada médico deve estar associado a uma especialidade.
- Cada consulta está vinculada a um paciente e a um médico.
- O sistema **não permite duas consultas no mesmo dia e horário para o mesmo médico**, a menos que uma delas esteja cancelada. A regra vale tanto ao agendar quanto ao reativar uma consulta cancelada.
- Não é possível excluir um paciente, médico ou especialidade que tenha registros vinculados.

## Modelos

| Modelo | Campos |
|---|---|
| `Especialidade` | nome, descrição |
| `Paciente` | nome, CPF, data de nascimento, telefone |
| `Medico` | nome, especialidade, CRM, telefone |
| `Consulta` | paciente, médico, data, horário, status |

## Tecnologias

- Python 3.12
- Django 5.2
- SQLite (banco de dados padrão do Django)

## Como executar

```bash
# 1. Clonar o repositório
git clone https://github.com/joaobleyb/projeto3-victor.git
cd projeto3-victor

# 2. (Opcional) Criar e ativar um ambiente virtual
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Linux/macOS

# 3. Instalar as dependências
pip install -r requirements.txt

# 4. Criar o banco de dados
python manage.py migrate

# 5. Iniciar o servidor
python manage.py runserver
```

Acesse **http://127.0.0.1:8000** no navegador.

Para usar o painel administrativo (`/admin`), crie um usuário:

```bash
python manage.py createsuperuser
```

### Ordem sugerida de uso

1. Cadastre as **especialidades**.
2. Cadastre os **médicos** e os **pacientes**.
3. **Agende** as consultas.

## Testes

```bash
python manage.py test atendimentos
```

## Estrutura do projeto

```
├── clinica/                 # Configurações do projeto Django
├── atendimentos/            # App principal
│   ├── models.py            # Modelos e regra de conflito de horário
│   ├── forms.py             # Formulários
│   ├── views.py             # Views (class-based views)
│   ├── urls.py              # Rotas
│   ├── admin.py             # Painel administrativo
│   ├── tests.py             # Testes automatizados
│   └── templates/           # Páginas HTML
├── manage.py
└── requirements.txt
```
