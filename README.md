# 🏆 World Cup Match Predictor (Previsor de Jogos da Copa do Mundo)

## Visão Geral do Projeto

Este projeto demonstra uma solução completa de Machine Learning (ML) implantada em uma arquitetura Full-Stack. O objetivo é prever o resultado (Vitória Casa, Empate, Vitória Visitante) de partidas de futebol internacional, utilizando dados históricos e estatísticas avançadas.

A solução é composta por:
1. **Back-end (API):** Desenvolvido em **Python** com **FastAPI** para hospedar o modelo de ML.
2. **Front-end (Web App):** Desenvolvido com **Svelte** para fornecer uma interface interativa que consome a API em tempo real.

## 🛠️ Stack Tecnológico

| Componente | Tecnologia | Uso Principal |
| :--- | :--- | :--- |
| **Data Science** | `Pandas`, `NumPy`, `Scikit-learn`, `Joblib` | ETL, Engenharia de Features, Treinamento do Modelo. |
| **Modelo** | `RandomForestClassifier` | Previsão de Classificação (3 classes). |
| **Back-end** | `FastAPI` (Python) | Criação da API RESTful para servir as previsões. |
| **Front-end** | `Svelte` / `SvelteKit` | Interface de Usuário moderna e reativa. |
| **Controle de Versão** | `Git` e **Git LFS** | Gerenciamento do código e dos grandes arquivos binários (modelo ML). |

## 🧠 Arquitetura de Machine Learning

O modelo foi treinado em mais de **23.000 partidas internacionais** desde 1993. A performance foi otimizada através da **Engenharia de Features Avançada** e um rigoroso processo de validação.

### Features Preditivas (X)

O modelo utiliza 6 features principais para tomar suas decisões:

1. **`diferenca_ranking`**: Diferença no ranking da FIFA entre os times.
2. **`e_copa_do_mundo`**: Fator binário para ponderar jogos de torneio (vs. amistosos).
3. **`avg_scored_home` / `avg_conceded_home`**: Média de gols marcados/sofridos pelo Time da Casa nos últimos 5 jogos.
4. **`avg_scored_away` / `avg_conceded_away`**: Média de gols marcados/sofridos pelo Time Visitante nos últimos 5 jogos.

### Performance Final do Modelo (Modelo 3 - Balanceado)

Para resolver o problema de desbalanceamento de classes (os empates são mais raros), foi aplicado o `class_weight='balanced'`.

| Métrica | Acurácia Geral | Recall (Empate) |
| :--- | :---: | :---: |
| **Resultado** | **54.29%** | **34%** |
| *Comparação:* | *Acurácia 21 pontos acima do chute aleatório (33.3%).* | *Melhora de 10x na capacidade de identificar empates (vs. 3% do modelo inicial).* |

## 🚀 Como Executar o Projeto Localmente

### Pré-requisitos

* Python 3.8+ e Node.js / npm
* Git LFS (necessário para baixar o arquivo do modelo grande)

```bash
# Instale o Git LFS, se ainda não o fez
git lfs install
```
### 1. Clonar o Repositório
```bash
# Isto baixará o repositório e os arquivos grandes via LFS
git clone [https://github.com/palomacdev/world_cup_predictor](https://github.com/palomacdev/world_cup_predictor)
cd world_cup_predictor
```
### 2. Rodar o Back-end (API FastAPI)
Navegue até a pasta da API, instale as dependências e inicie o servidor:
```bash
cd world-cup-predictor-api
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```
*A API estará acessível em `http://127.0.0.1:8000`.*
### 3. Rodar o Front-end (Svelte)
Abra um novo terminal, navegue até a pasta do front-end, instale e inicie:
```bash
cd ../world-cup-frontend 
npm install
npm run dev -- --open
```
*O App Web abrirá em `http://localhost:5173` e se conectará à API.*

## 🔗 Próximos Passos (Deployment)
O objetivo final é implantar a API FastAPI (usando Render ou Heroku) e o Front-end Svelte (usando Vercel ou Netlify) para que o aplicativo seja acessível online.


