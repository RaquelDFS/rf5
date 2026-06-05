# Estratégia de Versionamento — ReqFlow

## Objetivo

A estratégia de versionamento do ReqFlow foi definida para garantir organização, segurança e rastreabilidade durante a evolução do projeto.

Como a solução envolve diferentes telas, regras de negócio, banco de dados e camadas de código, o uso de Git e GitHub permite controlar as alterações realizadas, preservar versões anteriores e facilitar a colaboração entre os integrantes da equipe.

---

## Ferramentas Utilizadas

O controle de versão do projeto será realizado com:

- **Git** — controle local das alterações;
- **GitHub** — armazenamento remoto do repositório;
- **VS Code** — ambiente de desenvolvimento integrado ao Git.

---

## Estratégia Adotada

A estratégia adotada consiste em realizar commits frequentes e objetivos, sempre que uma entrega relevante for concluída.

Cada commit deve representar uma alteração clara no projeto, como:

- criação ou ajuste de telas;
- melhoria nas regras de negócio;
- alteração no banco de dados;
- correção de erros;
- inclusão de documentação;
- ajustes na arquitetura;
- implementação de funcionalidades;
- melhoria na organização do código.

Essa abordagem facilita a leitura do histórico e permite entender como a solução evoluiu ao longo do desenvolvimento.

---

## Padrão de Mensagens de Commit

Para manter o histórico claro, recomenda-se utilizar mensagens simples e descritivas.

Exemplos:

```text
feat: adiciona tela de gestão de usuários
feat: implementa cadastro de requisitos
fix: corrige listagem de projetos por perfil
docs: atualiza documentação do projeto
refactor: organiza chamadas por controller e service
chore: atualiza dependências do projeto
```

---

## Organização do Repositório

O repositório deve conter todos os arquivos necessários para executar e compreender o projeto:

- código-fonte completo;
- arquivo `README.md`;
- arquivo `requirements.txt`;
- documentação técnica;
- banco de dados local para testes, se aplicável;
- instruções de execução;
- credenciais de demonstração.

A estrutura do repositório deve permitir que qualquer avaliador ou integrante da equipe consiga baixar o projeto, instalar as dependências e executar a aplicação localmente.

---

## Controle de Integridade

Para garantir a integridade do código, a equipe deve seguir boas práticas simples:

1. testar localmente antes de realizar commit;
2. evitar subir arquivos temporários ou desnecessários;
3. manter o `requirements.txt` atualizado;
4. documentar alterações relevantes;
5. realizar backup antes de mudanças estruturais no banco;
6. revisar conflitos antes de atualizar o repositório principal.

---

## Benefícios para o Projeto

A estratégia de versionamento traz benefícios práticos para o ReqFlow:

- permite acompanhar a evolução da solução;
- reduz o risco de perda de código;
- facilita a colaboração entre os integrantes;
- melhora a organização das entregas;
- permite recuperar versões anteriores em caso de erro;
- apoia a rastreabilidade técnica do desenvolvimento;
- fortalece a confiabilidade do projeto.

---

## Conclusão

O versionamento com Git e GitHub será utilizado como mecanismo de controle, colaboração e segurança do desenvolvimento do ReqFlow.

A realização de commits organizados, com mensagens claras e testes locais antes do envio ao repositório, garante maior integridade ao código e facilita a continuidade do projeto.

Essa prática também demonstra maturidade no processo de desenvolvimento, pois mantém um histórico claro das decisões técnicas, melhorias implementadas e correções realizadas ao longo da construção da solução.
