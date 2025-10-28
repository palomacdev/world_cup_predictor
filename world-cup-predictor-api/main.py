from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np
import warnings
from pathlib import Path

# Suprime avisos
warnings.filterwarnings('ignore', category=UserWarning)

# --- 1. Configuração e Carregamento dos Artefatos ---

BASE_DIR = Path(__file__).resolve().parent
ARTIFACTS_DIR = BASE_DIR / "artifacts"

app = FastAPI(title="Preditor da Copa do Mundo API")

# Carrega os artefatos 
# Isso garante que eles fiquem na memória e sejam rápidos
try:
    model = joblib.load(ARTIFACTS_DIR / "modelo_avancado.joblib")
    
    ranking_df = pd.read_csv(ARTIFACTS_DIR / "ranking_data.csv")
    ranking_df['data_ranking'] = pd.to_datetime(ranking_df['data_ranking'])
    
    stats_df = pd.read_csv(ARTIFACTS_DIR / "stats_data.csv")
    stats_df['date'] = pd.to_datetime(stats_df['date'])
    
    print("Modelo e dados de suporte carregados com sucesso.")
except FileNotFoundError:
    print("ERRO: Arquivos de artefatos não encontrados. Verifique a pasta /artifacts")
    model, ranking_df, stats_df = None, None, None

# --- 2. Funções Auxiliares (do notebook) ---

def get_latest_rank(team_name, df):
    try:
        rank = df[df['time'] == team_name].iloc[-1]['rank']
        return rank
    except IndexError:
        return 150 # Retorna um rank ruim por padrão

def get_latest_stats(team_name, df):
    try:
        stats = df[df['team'] == team_name].iloc[-1]
        return stats['avg_scored'], stats['avg_conceded']
    except IndexError:
        return 0, 0 # Retorna 0 por padrão

# --- 3. Definição do "Schema" de Entrada (Pydantic) ---

class JogoInput(BaseModel):
    time_casa: str
    time_visitante: str
    e_copa_do_mundo: bool

# --- 4. O Endpoint de Previsão ---

@app.post("/predict")
def predict_match(jogo: JogoInput):
    """
    Recebe os dados de um jogo e retorna as probabilidades do resultado.
    """
    if model is None:
        return {"erro": "Modelo não foi carregado. Verifique os logs."}

    # 1. Coletar dados (exatamente como na função do notebook)
    rank_home = get_latest_rank(jogo.time_casa, ranking_df)
    avg_scored_home, avg_conceded_home = get_latest_stats(jogo.time_casa, stats_df)
    
    rank_away = get_latest_rank(jogo.time_visitante, ranking_df)
    avg_scored_away, avg_conceded_away = get_latest_stats(jogo.time_visitante, stats_df)

    # 2. Montar o vetor de features
    dados_jogo = {
        'diferenca_ranking': rank_away - rank_home,
        'e_copa_do_mundo': 1 if jogo.e_copa_do_mundo else 0,
        'avg_scored_home': avg_scored_home,
        'avg_conceded_home': avg_conceded_home,
        'avg_scored_away': avg_scored_away,
        'avg_conceded_away': avg_conceded_away
    }
    df_predict = pd.DataFrame([dados_jogo])

    # 3. Fazer a previsão de probabilidades
    probabilidades = model.predict_proba(df_predict)[0]
    
    # 4. Formatar a resposta em JSON
    mapa_resultados = {0: 'vitoria_casa', 1: 'empate', 2: 'vitoria_visitante'}
    resultado_provavel = mapa_resultados[probabilidades.argmax()]

    response = {
        "jogo": f"{jogo.time_casa} vs. {jogo.time_visitante}",
        "probabilidades": {
            "vitoria_casa": round(probabilidades[0], 4),
            "empate": round(probabilidades[1], 4),
            "vitoria_visitante": round(probabilidades[2], 4)
        },
        "resultado_mais_provavel": resultado_provavel
    }
    
    return response

@app.get("/")
def read_root():
    return {"status": "API do Preditor da Copa do Mundo está no ar!"}