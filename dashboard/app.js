const dropZone = document.getElementById('drop-zone');
const audioInput = document.getElementById('audio-input');
const selectBtn = document.getElementById('select-file-btn');
const resultsSection = document.getElementById('results-section');
const verdictText = document.getElementById('verdict-text');
const confidenceValue = document.getElementById('confidence-value');
const confidencePath = document.getElementById('confidence-path');
const specContainer = document.getElementById('spec-container');

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
    // URL da API (Troque para sua URL do Railway após o deploy se necessário)
    // Dica: você pode usar window.location se o backend estiver no mesmo domínio
    const API_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' 
        ? 'http://localhost:8000' 
        : ''; // No deploy, se estiverem no mesmo projeto, deixe vazio. Caso contrário, coloque a URL do Railway.

    // Reset e mostra seção de resultados
    resultsSection.style.display = 'grid';
    verdictText.textContent = 'PROCESSANDO...';
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
        } else if (fraudProb > 40) {
            confidencePath.style.stroke = '#F59E0B'; // Amarelo (Atenção)
        } else {
            confidencePath.style.stroke = '#10B981'; // Verde (Seguro)
        }

        // Animação do círculo
        confidencePath.setAttribute('stroke-dasharray', `${fraudProb}, 100`);
    }

    // Atualiza Espectrograma
    if (data.spectrogram_url) {
        const specName = data.spectrogram_url.split(/[\\/]/).pop();
        const timestamp = new Date().getTime();
        specContainer.innerHTML = `<img src="/tmp/${specName}?t=${timestamp}" alt="Espectrograma de Mel">`;
    }
}
