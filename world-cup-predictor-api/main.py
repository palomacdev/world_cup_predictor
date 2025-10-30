from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np
import warnings
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware

# Suprime avisos
warnings.filterwarnings('ignore', category=UserWarning)

# --- 1. Configuração e Carregamento dos Artefatos ---

BASE_DIR = Path(__file__).resolve().parent
ARTIFACTS_DIR = BASE_DIR / "artifacts"

app = FastAPI(title="Preditor da Copa do Mundo API")

# Origens do frontend
origins = [
    "https://lonely-werewolf-gv5jw6vqjxvc7wv-5173.app.github.dev", # codespace do github
    "http://localhost",
    "http://127.0.0.1:5173", # Outra forma de acessar o Svelte
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # Permite as origens da lista
    allow_credentials=True,
    allow_methods=["*"], # Permite todos os métodos (GET, POST, etc.)
    allow_headers=["*"], # Permite todos os cabeçalhos
)

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

# Mapeamento de Times (Atualizando: adicionando conforme necessário)
MAPA_TIMES = {
    "brasil": "Brazil",
    "brazil": "Brazil",
    "alemanha": "Germany",
    "germany": "Germany",
    "argentina": "Argentina",
    "inglaterra": "England",
    "england": "England",
    "frança": "France",
    "france": "France",
    "eua": "United States",
    "usa": "United States",
    "united states": "United States",
    "espanha": "Spain",
    "spain": "Spain",
    "portugal": "Portugal",
    "holanda": "Netherlands",
    "netherlands": "Netherlands",
    "italia": "Italy",
    "italy": "Italy",
    "japao": "Japan",
    "japan": "Japan"
}

print("Mapeamento de nomes de times carregado")

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

def normalize_team_name(name: str) -> str:
    """
    Converte o input do usuário (ex: 'brasil', 'EUA') para o nome
    oficial usado nos dataframes (ex: 'Brazil', 'United States').
    """
    normalize_input = name.lower().strip()

    return MAPA_TIMES.get(normalize_input, name.title())

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

    
    # Normaliza os nomes ANTES de usá-los
    time_casa_oficial = normalize_team_name(jogo.time_casa)
    time_visitante_oficial = normalize_team_name(jogo.time_visitante)
    

    # 1. Coletar dados (usando os nomes oficiais normalizados)
    rank_home = get_latest_rank(time_casa_oficial, ranking_df)
    avg_scored_home, avg_conceded_home = get_latest_stats(time_casa_oficial, stats_df)
    
    rank_away = get_latest_rank(time_visitante_oficial, ranking_df)
    avg_scored_away, avg_conceded_away = get_latest_stats(time_visitante_oficial, stats_df)

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
        # Mantém os nomes originais para o usuário ver
        "jogo": f"{jogo.time_casa} vs. {jogo.time_visitante}",
        
        
        "nomes_oficiais_usados": f"{time_casa_oficial} vs. {time_visitante_oficial}",
       

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
