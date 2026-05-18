# Sistema de Gestão de Stock (Mercado Pro)

Este projeto é um sistema de gestão de stock para mercados, desenvolvido em Python. O sistema permite o registo de produtos e a visualização do stock em tempo real, utilizando uma base de dados na nuvem através do Supabase. O projeto inclui duas abordagens de interface: uma versão desktop e uma versão web.

## Funcionalidades

* Registo de novos produtos (nome, preço e quantidade).
* Visualização em lista de todos os itens em stock com formatação de preços.
* Atualização em tempo real dos dados conectados ao Supabase.
* Proteção de credenciais da base de dados utilizando variáveis de ambiente.

## Tecnologias Utilizadas

* Python 3
* CustomTkinter (Interface Gráfica Desktop)
* Streamlit (Interface Web)
* Supabase (Base de dados na nuvem)
* python-dotenv (Gestão de variáveis de ambiente)

## Como Executar o Projeto Localmente

### 1. Instalação de Dependências
Certifique-se de ter o Python instalado. No terminal, instale as bibliotecas necessárias:

```bash
pip install customtkinter supabase python-dotenv streamlit
