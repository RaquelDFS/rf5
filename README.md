# ReqFlow — Plataforma Inteligente para Gestão de Requisitos

## Visão Geral

O **ReqFlow** é uma plataforma desenvolvida para centralizar, organizar e formalizar o levantamento de requisitos em projetos de software. A solução foi criada para reduzir falhas de comunicação, evitar perda de informações, melhorar a rastreabilidade das decisões e acelerar a geração de documentação técnica.

Em vez de depender de e-mails, reuniões sem registro, planilhas soltas ou documentos manuais, o ReqFlow oferece um ambiente único para cadastro de projetos, registro de requisitos, comentários, validações e exportação de documentação.

A proposta é entregar mais clareza para o cliente, mais controle para a equipe técnica e mais segurança para a gestão do projeto.

---

## Proposta de Valor

O ReqFlow apoia empresas e equipes de desenvolvimento que precisam transformar solicitações de clientes em requisitos claros, organizados e validados.

A plataforma contribui para:

- reduzir retrabalho causado por requisitos mal definidos;
- centralizar informações do projeto em um único ambiente;
- melhorar a comunicação entre cliente, analista e equipe técnica;
- registrar decisões, comentários e alterações;
- controlar aprovações e reprovações de requisitos;
- gerar documentação padronizada com mais agilidade;
- facilitar a rastreabilidade do escopo do projeto.

---

## Principais Funcionalidades

### Gestão de Usuários e Perfis

Permite cadastrar, editar, listar e desativar usuários, considerando diferentes perfis de acesso:

- gerente;
- analista;
- desenvolvedor;
- testador;
- cliente.

Cada perfil possui permissões específicas, garantindo que cada usuário acesse apenas as funcionalidades adequadas ao seu papel no processo.

### Gestão de Projetos

Permite cadastrar e acompanhar projetos, registrando informações como:

- nome do projeto;
- descrição ou escopo resumido;
- status;
- data de início;
- data fim prevista;
- responsável;
- cliente vinculado.

### Gestão de Requisitos

Permite registrar requisitos funcionais e não funcionais de forma estruturada, mantendo vínculo com o projeto correspondente.

Cada requisito pode conter:

- nome;
- descrição;
- tipo;
- status;
- visibilidade para o cliente;
- projeto relacionado.

### Colaboração e Comentários

Permite registrar comentários vinculados aos requisitos, mantendo as conversas dentro do próprio sistema. Isso reduz a perda de informações e melhora o alinhamento entre cliente e equipe técnica.

### Homologação de Requisitos

Permite controlar a aprovação ou reprovação de requisitos, formalizando a validação do cliente antes do avanço do projeto.

### Histórico e Rastreabilidade

Registra alterações relevantes, comentários e decisões tomadas ao longo do ciclo de vida dos requisitos, apoiando a auditoria e o controle do escopo.

### Exportação de Documentos

Permite gerar documentação em PDF com base nas informações cadastradas no sistema, reduzindo esforço manual e aumentando a padronização dos entregáveis.

---

## Tecnologias Utilizadas

O ReqFlow foi desenvolvido com tecnologias simples, acessíveis e adequadas para um MVP funcional:

- **Python** — linguagem principal do projeto;
- **Streamlit** — construção da interface web;
- **SQLite** — banco de dados local;
- **Git e GitHub** — versionamento e colaboração;
- **VS Code** — ambiente de desenvolvimento;
- **Programação Orientada a Objetos** — organização da estrutura interna da aplicação.

---

## Arquitetura da Solução

A aplicação segue uma estrutura organizada em camadas, mantendo simplicidade no desenvolvimento e clareza para manutenção futura.

Fluxo principal:

Tela Streamlit
↓
Controller
↓
Service
↓
database/db.py
↓
sistema.db

Essa divisão permite separar responsabilidades:

- as **telas** cuidam da interação com o usuário;
- os **controllers** validam dados e controlam o fluxo da operação;
- os **services** organizam a comunicação com a camada de dados;
- o arquivo **database/db.py** centraliza as operações com SQLite;
- o banco **sistema.db** armazena os dados persistentes.

---

## Estrutura de Pastas


rf5/
├── app.py
├── requirements.txt
├── README.md
├── sistema.db
│
├── components/
│   ├── tabela_projetos.py
│   └── tabela_requisitos.py
│
├── config/
│   └── navigation.py
│
├── controllers/
│   ├── usuario_controller.py
│   ├── projeto_controller.py
│   ├── requisito_controller.py
│   ├── comentario_controller.py
│   └── historico_controller.py
│
├── database/
│   └── db.py
│
├── docs/
│   └── ARQUITETURA_E_POO_REQFLOW.md
│
├── models/
│   ├── usuario.py
│   ├── projeto.py
│   ├── requisito.py
│   ├── comentario.py
│   └── historico.py
│
├── screens/
│   ├── inicio.py
│   ├── projetos.py
│   ├── requisitos.py
│   ├── clientes.py
│   ├── usuarios.py
│   ├── gestao_usuarios.py
│   └── perfis/
│       ├── perfil_usuario.py
│       ├── perfil_cliente.py
│       ├── perfil_projeto.py
│       └── perfil_requisito.py
│
├── services/
│   ├── usuario_service.py
│   ├── projeto_service.py
│   ├── requisito_service.py
│   ├── comentario_service.py
│   └── historico_service.py
│
└── views/
    ├── login.py
    └── dashboard.py

---

## Como Executar o Projeto

### 1. Clonar o repositório

```bash
git clone LINK_DO_REPOSITORIO_AQUI
```

### 2. Acessar a pasta do projeto

```bash
cd rf5
```

### 3. Criar o ambiente virtual

```bash
python -m venv venv
```

Caso o comando `python` não funcione no Windows, utilize:

```bash
py -m venv venv
```

### 4. Ativar o ambiente virtual

No Windows PowerShell:

```bash
venv\Scripts\activate
```

### 5. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 6. Executar a aplicação

```bash
streamlit run app.py
```

Após executar o comando, o Streamlit abrirá o sistema no navegador.

---

## Credenciais de Demonstração

| Perfil | Login | Senha |
|---|---|---|
| Gerente | gerente | 123456 |
| Analista | raquel | 123 |
| Cliente | Wallace | 123456 |
| Cliente | Caio | 123456 |
| Desenvolvedor | dev | 123456 |
| Testador | testador | 123456 |

As credenciais podem variar conforme os dados cadastrados no banco `sistema.db`.

---

## Banco de Dados

O projeto utiliza SQLite por meio do arquivo:

```text
sistema.db
```

As principais tabelas utilizadas são:

- `usuarios`;
- `projeto`;
- `requisitos`;
- `comentarios`;
- `historico`.

O arquivo `database/db.py` concentra as funções de criação, consulta, atualização e persistência dos dados.

---

## Status da Solução

O ReqFlow encontra-se em versão MVP funcional, com foco em demonstrar o fluxo principal da solução:

1. acesso ao sistema;
2. gestão de usuários;
3. cadastro e acompanhamento de projetos;
4. cadastro de requisitos;
5. comentários e colaboração;
6. homologação;
7. rastreabilidade;
8. exportação documental.

---

## Próximas Evoluções

As próximas melhorias previstas são:

- refinamento das permissões por perfil;
- melhoria visual das telas;
- ampliação da rastreabilidade;
- melhoria da exportação em PDF;
- inclusão de notificações;
- evolução para banco em nuvem;
- implantação em ambiente web.

---

## Equipe

- Nathalissa de Amorim Ocampos Almeida;
- Nicole Galloway Araujo;
- Raquel da Fonseca Silva;
- Thiago Manoel Pereira Mina.

---

## Considerações Finais

O ReqFlow foi desenvolvido para resolver uma dor recorrente em projetos de software: a dificuldade de transformar necessidades do cliente em requisitos claros, rastreáveis e formalizados.

A solução entrega um ambiente simples, funcional e preparado para evolução, contribuindo para reduzir retrabalho, aumentar a transparência do processo e melhorar a qualidade da documentação de requisitos.
