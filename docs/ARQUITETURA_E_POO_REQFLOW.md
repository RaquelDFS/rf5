# Arquitetura e Organização Orientada a Objetos — ReqFlow

## Visão Geral

O ReqFlow foi estruturado para manter a simplicidade do desenvolvimento em Python e Streamlit, mas com uma organização mais clara para permitir manutenção, expansão e melhor separação de responsabilidades.

A solução utiliza uma arquitetura em camadas, aproximando a aplicação de um modelo mais profissional, sem tornar o código excessivamente complexo.

O fluxo principal da aplicação é:

Interface Streamlit
↓
Controller
↓
Service
↓
Database
↓
SQLite


Essa estrutura ajuda a separar o que cada parte do sistema deve fazer, tornando o projeto mais fácil de entender, testar e evoluir.

---

## Estrutura em Camadas

### Interface

A camada de interface é composta pelas telas do Streamlit, localizadas principalmente nas pastas `screens/`, `views/` e `components/`.

Essa camada é responsável por:

- exibir informações ao usuário;
- receber dados digitados;
- apresentar botões, formulários e tabelas;
- chamar os controllers para executar ações.

A interface não deve concentrar toda a regra de negócio. Sua função principal é facilitar a interação com o sistema.

---

### Controllers

A camada `controllers/` atua como intermediária entre as telas e os serviços.

Ela é responsável por:

- validar campos obrigatórios;
- organizar chamadas das telas;
- tratar mensagens de sucesso ou erro;
- acionar os services corretos;
- reduzir a complexidade dentro das telas.

Exemplos de controllers:

- `usuario_controller.py`;
- `projeto_controller.py`;
- `requisito_controller.py`;
- `comentario_controller.py`;
- `historico_controller.py`.

---

### Services

A camada `services/` concentra a lógica de comunicação com os dados.

Ela é responsável por:

- chamar funções do `database/db.py`;
- organizar consultas e cadastros;
- concentrar operações relacionadas a cada entidade;
- evitar que as telas acessem diretamente o banco.

Exemplos de services:

- `usuario_service.py`;
- `projeto_service.py`;
- `requisito_service.py`;
- `comentario_service.py`;
- `historico_service.py`.

---

### Models

A camada `models/` representa as principais entidades do sistema.

Cada classe modela um elemento importante da solução, como usuário, projeto, requisito, comentário e histórico.

Exemplos de models:

- `Usuario`;
- `Projeto`;
- `Requisito`;
- `Comentario`;
- `Historico`.

Essas classes ajudam a representar os dados de forma mais organizada e demonstram a aplicação da Programação Orientada a Objetos no projeto.

---

### Database

A camada `database/` concentra a conexão com o SQLite por meio do arquivo `db.py`.

Essa camada é responsável por:

- abrir conexão com o banco;
- criar tabelas;
- inserir registros;
- consultar dados;
- atualizar informações;
- registrar alterações;
- manter os dados persistidos no arquivo `sistema.db`.

---

## Aplicação da Programação Orientada a Objetos

A Programação Orientada a Objetos foi aplicada no ReqFlow principalmente por meio da criação de classes que representam as entidades centrais da plataforma.

Essa abordagem permite organizar melhor os dados e comportamentos associados a cada elemento do sistema.

---

## Encapsulamento

O encapsulamento aparece na forma como as responsabilidades foram separadas.

As telas não precisam saber diretamente como o banco de dados funciona. Elas acionam controllers, que por sua vez chamam services, e somente então as funções do banco são executadas.

Essa separação evita que toda a lógica fique concentrada em um único arquivo e facilita futuras alterações.

Exemplo prático:

A tela de usuários solicita um cadastro
↓
O controller valida os dados
↓
O service encaminha a operação
↓
O database grava no SQLite


---

## Abstração

A abstração está presente na criação das entidades principais do sistema.

Classes como `Usuario`, `Projeto` e `Requisito` representam conceitos reais da solução, escondendo detalhes internos e permitindo trabalhar com objetos mais próximos da regra de negócio.

Isso facilita o entendimento do projeto, pois o código passa a refletir melhor os elementos utilizados no processo de gestão de requisitos.

---

## Herança

A herança pode ser aplicada de forma simples em evoluções futuras, especialmente na diferenciação entre perfis de usuário.

O sistema trabalha com diferentes perfis, como gerente, analista, desenvolvedor, testador e cliente. Todos compartilham características comuns de usuário, mas possuem permissões diferentes.

Conceitualmente, todos podem partir de uma estrutura base de usuário e especializar comportamentos conforme o perfil.

---

## Polimorfismo

O polimorfismo pode ser observado na forma como diferentes perfis interagem com funcionalidades semelhantes, mas com permissões diferentes.

Por exemplo:

- um gerente pode administrar usuários e projetos;
- um analista pode cadastrar requisitos;
- um cliente pode visualizar e validar requisitos;
- um desenvolvedor pode acompanhar requisitos vinculados;
- um testador pode atuar na etapa de revisão.

A ação de acessar o sistema é comum, mas o comportamento disponível muda conforme o perfil.

---

## Benefícios da Arquitetura

A organização adotada traz os seguintes benefícios:

- código mais limpo;
- melhor separação de responsabilidades;
- manutenção mais simples;
- facilidade para corrigir erros;
- maior clareza para novos integrantes;
- preparação para crescimento futuro;
- melhor alinhamento com boas práticas de desenvolvimento;
- facilidade para demonstrar a estrutura da solução.

---

## Relação com as Funcionalidades do Produto

A arquitetura em camadas apoia diretamente as funcionalidades do ReqFlow:

| Funcionalidade | Camadas Envolvidas |
|---|---|
| Login | View, Controller, Service, Database |
| Gestão de usuários | Screen, Controller, Service, Model, Database |
| Gestão de projetos | Screen, Controller, Service, Model, Database |
| Gestão de requisitos | Screen, Controller, Service, Model, Database |
| Comentários | Screen, Controller, Service, Model, Database |
| Histórico | Service, Model, Database |
| Exportação PDF | Screen, Service, Database |

---

## Conclusão

A estrutura do ReqFlow foi organizada para equilibrar simplicidade e profissionalismo.

A solução mantém uma base acessível para desenvolvimento em Python e Streamlit, mas adiciona uma divisão em camadas que melhora a manutenção, facilita a explicação técnica e prepara o sistema para novas evoluções.

A aplicação dos conceitos de Programação Orientada a Objetos contribui para tornar o código mais organizado, reutilizável e alinhado às necessidades de crescimento da plataforma.
