
# projeto1-telezap2000

Projeto da equipe Telezap2000 para cadeira projeto 1

  

O projeto FADA (Ferramenta de Alocação de Disciplinas Acadêmicas) visa em seu uso tanto facilitar o processo de alocação de disciplinas feita pela coordenação, como facilitar a comunicação entre professores e coordenadores por meio de de feedbacks dentro da ferramenta. outro uso que se tornou importante durante o desenvolvimento foi a apresentação dos dados referentes a alocação para o uso dos alunos de forma mais direta e fácil.



Integrantes:

Iuri Castro SIlva

José Caique Militão França

José Flávio Alves Gomes Filho

José Ivan Sena Torres Portugal

Milena Costa Barrozo

## Documento de requisitos do sistema
<ul>
<li>
RFT: Requisitos Funcionais para Todos perfis
</li>
<li>
RFC: Requisitos Funcionais para Coordenador
</li>
<li>
RFP: Requisitos Funcionais para Professores
</li>
<li>
RFA: Requisitos Funcionais para Alunos

</li>
</ul>

|Código | Funcionalidade                                                 |Situação|
|-------|----------------------------------------------------------------|--------|
|RFT0001|Buscar nome do professor                                        |&check; |
|RFT0002|Buscar nome da disciplina                                       |&check; |
|RFT0003|Buscar nome da sala                                             |&check; |
|RFT0004|Filtrar busca por horário                                       |&check; |
|RFT0005|Filtrar busca por semestre                                      |&check; |
|RFT0006|Limitar acesso baseado em perfil                                |&check; |
|RFC0001|Gerar os horários                                               |&check; |
|RFC0002|Adicionar disciplina                                            |&check; |
|RFC0003|Atualizar disciplina                                            |&check; |
|RFC0004|Adicionar professor                                             |&check; |
|RFC0005|Atualizar professor                                             |&check; |
|RFC0006|Adicionar sala                                                  |&check; |
|RFC0007|Atualizar sala                                                  |&check; |
|RFC0008|Adicionar turma                                                 |&check; |
|RFC0009|Atualizar turma                                                 |&check; |
|RFC0010|Adicionar turma a disciplina                                    |&check; |
|RFC0011|Adicionar professor a disciplina                                |&check; |
|RFC0012|Adicionar sala a disciplina                                     |&check; |
|RFC0013|Alterar horário de uma turma                                    |&check; |
|RFC0014|Visualizar os horários como coordenador                         |&check; |
|RFC0015|Efetuar login como coordenador                                  |&check; |
|RFC0016|Visualizar número de disciplinas ofertadas                      |&check; |
|RFC0017|Visualizar número de disciplinas ofertadas por professor        |&check; |
|RFP0001|Fornecer feedback sobre a planilha                              |&check; |
|RFP0002|Visualizar os horários como professor                           |&check; |
|RFP0003|Efetuar login como professor                                    |&check; |
|RFA0001|Visualizar os horários como aluno                               |&check; |



## instalação
para rodar o código é necessário ter Node instalado, para instalar node siga as orientações em: https://docs.npmjs.com/downloading-and-installing-node-js-and-npm

para rodar o código é também necessário que a máquinha tenha instalada python e as seguintes bibliotecas que podem ser instaladas com pip:
```bash
pip install flask
pip install flask_cors
pip install flask_jwt_extended
pip install flask_sqlalchemy
```

## Desenvolvimento
para desenvolver o código referente ao backend do programa é necessário instalar as dependências necessárias e rodar um ambiente de desenvolvimento, ademais é necessário também que que o backend da ferramenta esteja rodando, seguem os comandos necessários para rodar ambos
### Frontend
```bash
cd ./frontend/
npm install
npm  run  dev
```
### Backend
```bash
cd ./backend/
npm install
npm  run  dev
```
  

## Building

  

para criar a versão de produção do programa basta rodar:

  

```bash
cd ./frontend/

npm  run  build

```

  

dá para ter uma preview da versão de prodrução fazendo o mesmo processo com `npm run preview`.

  

> para fazer deploy do programa é necessário usar um [adapter](https://kit.svelte.dev/docs/adapters) para o ambiente alvo.
