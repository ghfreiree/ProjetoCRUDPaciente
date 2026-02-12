# Projeto CRUD Paciente

Este projeto consiste em uma aplicação de linha de comando (CLI) desenvolvida em **Python** para o gerenciamento de registros de pacientes. O sistema realiza operações completas de CRUD (Create, Read, Update, Delete) persistindo os dados em um banco de dados **Oracle**.

## 🚀 Funcionalidades

O sistema oferece um menu interativo com as seguintes opções:

* **Inserir Paciente**: Cadastra um único paciente (Nome, Idade, Descrição e Status).
* **Inserir Múltiplos Pacientes**: Permite a inserção em lote (batch insert) de vários pacientes de uma só vez, otimizando a performance do banco.
* **Listar Pacientes**: Exibe todos os registros armazenados na tabela, ordenados pelo ID.
* **Atualizar Status**: Altera o campo "Status" de um paciente específico buscando pelo seu ID.
* **Deletar Paciente**: Remove um registro do banco de dados através do ID.
* **Criação Automática**: Ao iniciar, o script verifica e cria a tabela `pacientes` caso ela não exista.

## 🛠️ Tecnologias Utilizadas

* **Python 3.13**
* **Oracle Database**: Banco de dados relacional.
* **python-oracledb**: Driver atualizado para conexão com banco de dados Oracle.

## 📋 Estrutura do Banco de Dados

O código cria automaticamente uma tabela chamada `pacientes` com a seguinte estrutura:

| Coluna | Tipo | Detalhes |
| :--- | :--- | :--- |
| `id` | NUMBER | Chave Primária (Auto-incremento via IDENTITY) |
| `nome` | VARCHAR2(100) | Obrigatório |
| `idade` | NUMBER(3) | |
| `descricao` | VARCHAR2(200) | |
| `status` | VARCHAR2(30) | |

## 📦 Instalação e Configuração

### Pré-requisitos
Certifique-se de ter o Python instalado. Em seguida, instale a biblioteca de conexão com o Oracle:

```bash
pip install oracledb
