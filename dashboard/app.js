const dropZone = document.getElementById('drop-zone');
const audioInput = document.getElementById('audio-input');
const selectBtn = document.getElementById('select-file-btn');
const resultsSection = document.getElementById('results-section');
const verdictText = document.getElementById('verdict-text');
const confidenceValue = document.getElementById('confidence-value');
const confidencePath = document.getElementById('confidence-path');
const specContainer = document.getElementById('spec-container');
const verdictExplanation = document.getElementById('verdict-explanation');

// Event Listeners
selectBtn.addEventListener('click', () => audioInput.click());

audioInput.addEventListener('change', (e) => {
    if (e.target.files.length) handleUpload(e.target.files[0]);
});

dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('dragover');
});

dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('dragover');
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('dragover');
    if (e.dataTransfer.files.length) handleUpload(e.dataTransfer.files[0]);
});

async function handleUpload(file) {
    // Detecta se estamos rodando localmente ou no Hugging Face
    const isLocal = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
    
    // Se você estiver no Vercel, mude '' para a URL do seu Space no Hugging Face
    const API_URL = ''; // Usa o host atual (mesma porta)
    // Reset e mostra seção de resultados
    resultsSection.style.display = 'grid';
    verdictText.textContent = 'PROCESSANDO...';
    if (verdictExplanation) verdictExplanation.textContent = '';
    confidenceValue.textContent = '0%';
    confidencePath.setAttribute('stroke-dasharray', '0, 100');
    specContainer.innerHTML = '<p>Analisando frequências...</p>';

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch(`${API_URL}/analyze`, {
            method: 'POST',
            body: formData
        });

        const data = await response.json();
        displayResults(data);
    } catch (error) {
        console.error('Erro na análise:', error);
        verdictText.innerText = 'ERRO NA CONEXÃO';
    }
}

function displayResults(data) {
    console.log('Resultados recebidos:', data);
    
    // Atualiza veredito
    const isSpoof = data.verdict === 'SPOOF';
    verdictText.textContent = isSpoof ? ' FRAUDE DETECTADA' : ' ÁUDIO AUTÊNTICO';
    verdictText.style.color = isSpoof ? '#EF4444' : '#10B981';

    // Atualiza explicação do veredito (Consenso dos Motores)
    /* 
    if (verdictExplanation) {
        verdictExplanation.textContent = data.engines_consensus || '';
        verdictExplanation.style.color = isSpoof ? '#FCA5A5' : '#6EE7B7';
    }
    */
    verdictText.style.color = isSpoof ? '#EF4444' : '#10B981';
    
    // Atualiza ponto de pulso
    const pulseDot = document.querySelector('.pulse');
    if (pulseDot) {
        pulseDot.style.background = isSpoof ? '#EF4444' : '#10B981';
        pulseDot.style.boxShadow = `0 0 10px ${isSpoof ? '#EF4444' : '#10B981'}`;
    }
    
    // Agora mostramos a PROBABILIDADE DE FRAUDE no círculo, pois é o que importa para o usuário
    const fraudProb = Math.round((data.fraud_score || 0) * 100);
    console.log('Calculated Fraud Prob:', fraudProb);
    
    if (confidenceValue) {
        confidenceValue.textContent = `${fraudProb}%`;
    }
    
    if (confidencePath) {
        // Cor do círculo baseada no risco
        if (fraudProb > 80) {
            confidencePath.style.stroke = '#EF4444'; // Vermelho (Perigo)
            if (pulseDot) pulseDot.style.background = '#EF4444';
        } else if (fraudProb > 40) {
            confidencePath.style.stroke = '#F59E0B'; // Amarelo (Atenção)
            if (pulseDot) pulseDot.style.background = '#F59E0B';
        } else {
            confidencePath.style.stroke = '#10B981'; // Verde (Seguro)
            if (pulseDot) pulseDot.style.background = '#10B981';
        }

        // Animação do círculo
        confidencePath.setAttribute('stroke-dasharray', `${fraudProb}, 100`);
    }
    // Atualiza Espectrograma
    // Atualiza Espectrograma e Heatmap (XAI)
    if (data.spectrogram_url) {
        const specName = data.spectrogram_url.split(/[\\/]/).pop();
        const timestamp = new Date().getTime();
        
        let heatmapHtml = '<div class="heatmap-overlay">';
        if (data.temporal_scores && data.temporal_scores.length > 0) {
            data.temporal_scores.forEach(score => {
                // Interpola cor entre verde (seguro) e vermelho (fraude)
                // Usando HSL: 120 (verde) a 0 (vermelho)
                const hue = 120 - (score * 120);
                const opacity = score > 0.4 ? (score * 0.7) : (score * 0.2); 
                heatmapHtml += `<div class="heatmap-segment" style="background: hsla(${hue}, 100%, 50%, ${opacity})"></div>`;
            });
        }
        heatmapHtml += '</div>';

        specContainer.innerHTML = `
            <div class="spec-wrapper">
                <img src="/tmp/${specName}?t=${timestamp}" alt="Espectrograma de Mel">
                ${heatmapHtml}
            </div>
        `;
    }

    // Scroll automático suave para os resultados
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });

    // Atualiza Diagnóstico
    updateDiagnostics(data);
}

function updateDiagnostics(data) {
    const diagSection = document.getElementById('diagnostic-section');
    const toggleBtn = document.getElementById('toggle-diagnostic');
    const details = document.getElementById('diagnostic-details');
    
    if (!diagSection) return;

    diagSection.style.display = 'block';

    const w2vScore = Math.round((data.wav2vec_score || 0) * 100);
    const astScore = Math.round((data.ast_score || 0) * 100);

    // Atualiza valores e barras com delay para animação
    setTimeout(() => {
        document.getElementById('w2v-val').textContent = `${w2vScore}%`;
        document.getElementById('ast-val').textContent = `${astScore}%`;
        document.getElementById('w2v-bar').style.width = `${w2vScore}%`;
        document.getElementById('ast-bar').style.width = `${astScore}%`;
        document.getElementById('rigor-logic').textContent = data.engines_consensus || 'Padrão';
    }, 100);

    // Toggle behavior
    if (toggleBtn && !toggleBtn.dataset.hasListener) {
        toggleBtn.addEventListener('click', () => {
            const isHidden = details.style.display === 'none';
            details.style.display = isHidden ? 'block' : 'none';
            toggleBtn.textContent = isHidden ? 'Esconder' : 'Ver Detalhes';
            
            if (isHidden) {
                details.style.animation = 'fadeInUp 0.5s forwards';
            }
        });
        toggleBtn.dataset.hasListener = "true";
    }
}

// Lógica do Modal "Como Funciona" (Overlay)
const modal = document.getElementById('how-it-works-modal');
const openBtn = document.getElementById('open-how-it-works');
const closeBtn = document.getElementById('close-modal');

if (openBtn && modal) {
    openBtn.addEventListener('click', (e) => {
        e.preventDefault();
        modal.classList.add('active');
        document.body.style.overflow = 'hidden'; // Trava o scroll
    });
}

if (closeBtn && modal) {
    closeBtn.addEventListener('click', () => {
        modal.classList.remove('active');
        document.body.style.overflow = 'auto'; // Destrava o scroll
    });

    // Fechar ao clicar fora do conteúdo
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            closeBtn.click();
        }
    });
}

// Fechar com a tecla ESC
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modal && modal.classList.contains('active')) {
        closeBtn.click();
    }
});