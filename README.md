# 💪 AI Personal Trainer - Python & MySQL

Sistema inteligente que gera treinos personalizados utilizando a API da Cohere, com filtragem dinâmica de exercícios via MySQL e salvamento de histórico em JSON.

## 🚀 Tecnologias
* **Python 3.x**
* **MySQL** (Banco de Dados Relacional)
* **Cohere API** (IA Generativa)
* **Python-dotenv** (Segurança de credenciais)

## 🧠 Como funciona?
O projeto resolve o problema de "alucinação" das IAs. 
1. O script consulta o banco de dados **MySQL** para ver quais exercícios existem para o grupo muscular escolhido.
2. Esses exercícios são enviados como contexto para a **IA (Cohere)**.
3. A IA gera o treino formatado.
4. O resultado final é estruturado em **JSON** e salvo no banco de dados para consulta posterior.

## 🛠️ Como rodar o projeto
1. Clone o repositório.
2. Instale as dependências: `pip install -r requirements.txt`.
3. Configure o arquivo `.env` com suas chaves de API e banco de dados.
4. Execute: `python main.py`.

---
Desenvolvido por **Gabriel Neto** durante os estudos de ADS.
