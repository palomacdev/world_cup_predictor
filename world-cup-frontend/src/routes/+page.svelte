<script>
    // --- 1. Variáveis de Estado ---
    let timeCasa = 'Brazil';
    let timeVisitante = 'Argentina';
    let eCopaDoMundo = true;
    
    let isLoading = false;
    let previsao = null;
    let erro = null;
    let showUrlConfig = false;

    // URL da API
    let API_URL = 'https://lonely-werewolf-gv5jw6vqjxvc7wv-8000.app.github.dev/predict';

    // --- 2. Função de Previsão ---
    async function fazerPrevisao() {
        // Validação básica
        if (!timeCasa.trim() || !timeVisitante.trim()) {
            erro = 'Por favor, preencha ambos os times';
            return;
        }

        isLoading = true;
        previsao = null;
        erro = null;

        const dadosInput = {
            time_casa: timeCasa.trim(),
            time_visitante: timeVisitante.trim(),
            e_copa_do_mundo: eCopaDoMundo
        };

        try {
            console.log('🔍 Tentando conectar em:', API_URL);
            console.log('📦 Enviando dados:', dadosInput);
            
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(dadosInput)
            });

            console.log('✅ Resposta recebida. Status:', response.status);

            if (!response.ok) {
                const errorData = await response.text();
                throw new Error(`Erro ${response.status}: ${errorData || response.statusText}`);
            }

            previsao = await response.json();
            console.log('📊 Previsão:', previsao);

        } catch (error) {
            console.error("❌ Erro completo:", error);
            erro = error.message;
            
            if (error.message.includes('Failed to fetch')) {
                erro = `Não foi possível conectar à API em ${API_URL}. 
                
Possíveis causas:
1. Backend não está rodando
2. Porta 8000 não está pública no Codespace
3. URL incorreta

👉 Clique em "Configurar URL" abaixo para atualizar.`;
            }
        } finally {
            isLoading = false;
        }
    }

    function handleKeydown(event) {
        if (event.key === 'Enter' && !isLoading) {
            fazerPrevisao();
        }
    }

    async function testarConexao() {
        try {
            const baseUrl = API_URL.replace('/predict', '');
            console.log('🧪 Testando conexão com:', baseUrl);
            const response = await fetch(baseUrl);
            const data = await response.json();
            alert('✅ Conexão OK! ' + JSON.stringify(data));
        } catch (error) {
            alert('❌ Erro na conexão: ' + error.message);
        }
    }

    function trocarTimes() {
        [timeCasa, timeVisitante] = [timeVisitante, timeCasa];
    }

    function getResultadoEmoji(resultado) {
        if (resultado === 'vitoria_casa') return '🏠';
        if (resultado === 'empate') return '🤝';
        return '✈️';
    }

    function getResultadoTexto(resultado) {
        if (resultado === 'vitoria_casa') return `Vitória ${timeCasa}`;
        if (resultado === 'empate') return 'Empate';
        return `Vitória ${timeVisitante}`;
    }

    function getBarWidth(prob) {
        return (prob * 100).toFixed(1);
    }
</script>

<style>
    :global(body) {
        margin: 0;
        padding: 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
    }
    
    .container {
        max-width: 600px;
        margin: 0 auto;
        padding: 2rem 1rem;
        min-height: 100vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    main {
        background: white;
        border-radius: 20px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        padding: 2.5rem;
        animation: slideUp 0.5s ease-out;
    }

    @keyframes slideUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .header {
        text-align: center;
        margin-bottom: 2rem;
    }

    h1 {
        color: #2d3748;
        font-size: 2rem;
        margin: 0 0 0.5rem 0;
        font-weight: 800;
    }

    .subtitle {
        color: #718096;
        font-size: 0.95rem;
        margin: 0;
    }
    
    .teams-container {
        background: linear-gradient(135deg, #f6f8fb 0%, #f1f3f9 100%);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        position: relative;
    }

    .form-group {
        margin-bottom: 1.25rem;
    }
    
    label {
        display: block;
        margin-bottom: 0.5rem;
        font-weight: 600;
        color: #4a5568;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    input[type="text"] {
        width: 100%;
        padding: 0.875rem 1rem;
        box-sizing: border-box;
        border: 2px solid #e2e8f0;
        border-radius: 12px;
        font-size: 1rem;
        transition: all 0.3s ease;
        background: white;
        font-weight: 500;
    }
    
    input[type="text"]:focus {
        outline: none;
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }

    .swap-button {
        position: absolute;
        right: 1.5rem;
        top: 50%;
        transform: translateY(-50%);
        background: white;
        border: 2px solid #e2e8f0;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        cursor: pointer;
        font-size: 1.2rem;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }

    .swap-button:hover {
        transform: translateY(-50%) rotate(180deg);
        border-color: #667eea;
        background: #667eea;
    }
    
    .checkbox-container {
        background: white;
        border: 2px solid #e2e8f0;
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.75rem;
        cursor: pointer;
        transition: all 0.3s ease;
    }

    .checkbox-container:hover {
        border-color: #667eea;
        background: #f7fafc;
    }

    .checkbox-container.active {
        border-color: #667eea;
        background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
    }
    
    input[type="checkbox"] {
        width: 24px;
        height: 24px;
        cursor: pointer;
        accent-color: #667eea;
    }
    
    .checkbox-container label {
        margin: 0;
        cursor: pointer;
        text-transform: none;
        font-size: 1rem;
        letter-spacing: normal;
        flex: 1;
    }
    
    button {
        width: 100%;
        padding: 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        font-size: 1.1rem;
        font-weight: 700;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    button:hover:not(:disabled) {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5);
    }

    button:active:not(:disabled) {
        transform: translateY(0);
    }
    
    button:disabled {
        background: #cbd5e0;
        cursor: not-allowed;
        box-shadow: none;
    }
    
    .erro {
        margin-top: 1.5rem;
        padding: 1.25rem;
        background: #fff5f5;
        border-left: 4px solid #fc8181;
        border-radius: 12px;
        color: #742a2a;
        white-space: pre-line;
        animation: shake 0.5s ease;
    }

    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-10px); }
        75% { transform: translateX(10px); }
    }
    
    .button-group {
        display: flex;
        gap: 0.5rem;
        margin-top: 0.75rem;
    }
    
    .button-group button {
        flex: 1;
        padding: 0.625rem;
        font-size: 0.85rem;
        background: #718096;
    }

    .button-group button:hover:not(:disabled) {
        background: #4a5568;
    }
    
    .url-config {
        margin-top: 1rem;
        padding: 1.25rem;
        background: #fffaf0;
        border-left: 4px solid #ed8936;
        border-radius: 12px;
    }
    
    .url-config input {
        margin-top: 0.5rem;
        font-family: 'Courier New', monospace;
        font-size: 0.85rem;
    }
    
    .resultado {
        margin-top: 2rem;
        animation: slideUp 0.5s ease-out;
    }

    .resultado-header {
        text-align: center;
        margin-bottom: 1.5rem;
    }

    .resultado-header h3 {
        color: #2d3748;
        margin: 0 0 1rem 0;
        font-size: 1.3rem;
    }

    .resultado-destaque {
        background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 16px;
        text-align: center;
        box-shadow: 0 10px 25px rgba(72, 187, 120, 0.3);
        margin-bottom: 1.5rem;
    }

    .resultado-destaque-emoji {
        font-size: 3rem;
        margin-bottom: 0.5rem;
    }

    .resultado-destaque-texto {
        font-size: 1.5rem;
        font-weight: 800;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    
    .probabilidades {
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }

    .prob-item {
        background: white;
        border: 2px solid #e2e8f0;
        border-radius: 12px;
        padding: 1rem;
        transition: all 0.3s ease;
    }

    .prob-item:hover {
        border-color: #667eea;
        transform: translateX(5px);
    }

    .prob-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.75rem;
    }

    .prob-label {
        font-weight: 600;
        color: #4a5568;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .prob-value {
        font-size: 1.25rem;
        font-weight: 800;
        color: #667eea;
    }

    .prob-bar-container {
        background: #e2e8f0;
        height: 8px;
        border-radius: 4px;
        overflow: hidden;
    }

    .prob-bar {
        height: 100%;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 4px;
        transition: width 0.8s ease;
    }

    .loading-spinner {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(255,255,255,0.3);
        border-radius: 50%;
        border-top-color: white;
        animation: spin 0.8s linear infinite;
        margin-right: 0.5rem;
    }

    @keyframes spin {
        to { transform: rotate(360deg); }
    }
</style>

<div class="container">
    <main>
        <div class="header">
            <h1>⚽ Preditor de Jogos</h1>
            <p class="subtitle">Previsão baseada em Machine Learning</p>
        </div>

        <div class="teams-container">
            <div class="form-group">
                <label for="timeCasa">🏠 Time da Casa</label>
                <input 
                    type="text" 
                    id="timeCasa" 
                    bind:value={timeCasa}
                    on:keydown={handleKeydown}
                    placeholder="Ex: Brazil"
                >
            </div>

            <div class="form-group" style="margin-bottom: 0;">
                <label for="timeVisitante">✈️ Time Visitante</label>
                <input 
                    type="text" 
                    id="timeVisitante" 
                    bind:value={timeVisitante}
                    on:keydown={handleKeydown}
                    placeholder="Ex: Argentina"
                >
            </div>

            <button class="swap-button" on:click={trocarTimes} title="Trocar times">
                🔄
            </button>
        </div>

        <div class="checkbox-container {eCopaDoMundo ? 'active' : ''}" on:click={() => eCopaDoMundo = !eCopaDoMundo}>
            <input type="checkbox" id="eCopa" bind:checked={eCopaDoMundo}>
            <label for="eCopa">🏆 É jogo da Copa do Mundo?</label>
        </div>

        <button on:click={fazerPrevisao} disabled={isLoading}>
            {#if isLoading}
                <span class="loading-spinner"></span>
                Analisando...
            {:else}
                🔮 Fazer Previsão
            {/if}
        </button>

        {#if erro}
            <div class="erro">
                <strong>⚠️ Erro:</strong> {erro}
            </div>
            
            <div class="button-group">
                <button on:click={() => showUrlConfig = !showUrlConfig}>
                    {showUrlConfig ? '❌ Fechar' : '⚙️ Configurar URL'}
                </button>
                <button on:click={testarConexao}>
                    🧪 Testar Conexão
                </button>
            </div>
            
            {#if showUrlConfig}
                <div class="url-config">
                    <label for="apiUrl">🔗 URL da API:</label>
                    <input 
                        type="text" 
                        id="apiUrl" 
                        bind:value={API_URL}
                        placeholder="https://lonely-werewolf-gv5jw6vqjxvc7wv-8000.app.github.dev/predict"
                    >
                    <p style="margin-top: 0.5rem; font-size: 0.85rem; color: #744210;">
                        
                    </p>
                </div>
            {/if}
        {/if}

        {#if previsao}
            <div class="resultado">
                <div class="resultado-header">
                    <h3>{previsao.jogo}</h3>
                </div>
                
                <div class="resultado-destaque">
                    <div class="resultado-destaque-emoji">
                        {getResultadoEmoji(previsao.resultado_mais_provavel)}
                    </div>
                    <p class="resultado-destaque-texto">
                        {getResultadoTexto(previsao.resultado_mais_provavel)}
                    </p>
                </div>
                
                <div class="probabilidades">
                    <div class="prob-item">
                        <div class="prob-header">
                            <span class="prob-label">
                                <span>🏠</span>
                                <span>Vitória {timeCasa}</span>
                            </span>
                            <span class="prob-value">{getBarWidth(previsao.probabilidades.vitoria_casa)}%</span>
                        </div>
                        <div class="prob-bar-container">
                            <div class="prob-bar" style="width: {getBarWidth(previsao.probabilidades.vitoria_casa)}%"></div>
                        </div>
                    </div>

                    <div class="prob-item">
                        <div class="prob-header">
                            <span class="prob-label">
                                <span>🤝</span>
                                <span>Empate</span>
                            </span>
                            <span class="prob-value">{getBarWidth(previsao.probabilidades.empate)}%</span>
                        </div>
                        <div class="prob-bar-container">
                            <div class="prob-bar" style="width: {getBarWidth(previsao.probabilidades.empate)}%"></div>
                        </div>
                    </div>

                    <div class="prob-item">
                        <div class="prob-header">
                            <span class="prob-label">
                                <span>✈️</span>
                                <span>Vitória {timeVisitante}</span>
                            </span>
                            <span class="prob-value">{getBarWidth(previsao.probabilidades.vitoria_visitante)}%</span>
                        </div>
                        <div class="prob-bar-container">
                            <div class="prob-bar" style="width: {getBarWidth(previsao.probabilidades.vitoria_visitante)}%"></div>
                        </div>
                    </div>
                </div>
            </div>
        {/if}
    </main>
</div>