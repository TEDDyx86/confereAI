document.addEventListener('DOMContentLoaded', () => {
    // Elements
    const loginSection = document.getElementById('login-section');
    const dashboardSection = document.getElementById('dashboard-section');
    const loginForm = document.getElementById('login-form');
    const passwordInput = document.getElementById('admin-password');
    const loginError = document.getElementById('login-error');
    
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const selectedFileInfo = document.getElementById('selected-file-info');
    const filenameDisplay = document.getElementById('filename-display');
    const btnUploadTrain = document.getElementById('btn-upload-train');
    
    const progressContainer = document.getElementById('training-progress-container');
    const progressBar = document.getElementById('training-progress-bar');
    const statusText = document.getElementById('training-status-text');

    let currentFile = null;
    let token = null; // JWT ou Token simples para as rotas autenticadas
    let statusInterval = null;

    // Login Handling
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        loginError.classList.add('hidden');
        const password = passwordInput.value;

        try {
            // Simulando chamada de login para a API
            const response = await fetch('/admin/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ password: password })
            });

            if (response.ok) {
                const data = await response.json();
                token = data.token; // Armazena token temporário
                loginSection.classList.add('hidden');
                dashboardSection.classList.remove('hidden');
            } else {
                loginError.classList.remove('hidden');
            }
        } catch (error) {
            console.error('Login error:', error);
            loginError.textContent = 'Erro ao conectar no servidor.';
            loginError.classList.remove('hidden');
        }
    });

    // Drag and Drop Handling
    dropZone.addEventListener('click', () => fileInput.click());

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
        
        if (e.dataTransfer.files.length) {
            handleFileSelect(e.dataTransfer.files[0]);
        }
    });

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length) {
            handleFileSelect(e.target.files[0]);
        }
    });

    function handleFileSelect(file) {
        // Validações básicas (zip/rar)
        if (!file.name.endsWith('.zip') && !file.name.endsWith('.rar')) {
            alert('Apenas arquivos .zip ou .rar são permitidos.');
            return;
        }
        
        currentFile = file;
        filenameDisplay.textContent = file.name;
        selectedFileInfo.classList.remove('hidden');
        btnUploadTrain.removeAttribute('disabled');
    }

    // Upload & Train Handling
    btnUploadTrain.addEventListener('click', async () => {
        if (!currentFile || !token) return;

        btnUploadTrain.setAttribute('disabled', 'true');
        progressContainer.classList.remove('hidden');
        statusText.textContent = 'Fazendo upload e extraindo dataset...';
        progressBar.style.width = '10%';

        const formData = new FormData();
        formData.append('file', currentFile);

        try {
            // 1. Upload
            const uploadResponse = await fetch('/admin/upload_dataset', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`
                },
                body: formData
            });

            if (!uploadResponse.ok) {
                const errData = await uploadResponse.json();
                throw new Error(errData.detail || 'Erro no upload');
            }

            statusText.textContent = 'Upload concluído. Iniciando fine-tuning...';
            progressBar.style.width = '30%';

            // 2. Start Training
            const trainResponse = await fetch('/admin/train', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (!trainResponse.ok) {
                const errData = await trainResponse.json();
                throw new Error(errData.detail || 'Erro ao iniciar treino');
            }

            // 3. Start Polling
            startStatusPolling();

        } catch (error) {
            statusText.textContent = `Erro: ${error.message}`;
            statusText.style.color = 'var(--danger)';
            btnUploadTrain.removeAttribute('disabled');
        }
    });

    function startStatusPolling() {
        if (statusInterval) clearInterval(statusInterval);

        statusInterval = setInterval(async () => {
            try {
                const response = await fetch('/admin/status', {
                    headers: { 'Authorization': `Bearer ${token}` }
                });

                if (response.ok) {
                    const data = await response.json();
                    
                    progressBar.style.width = `${data.progress}%`;
                    statusText.textContent = data.message || `Treinamento: ${data.progress}%`;

                    if (data.status === 'completed') {
                        clearInterval(statusInterval);
                        statusText.textContent = 'Treinamento concluído com sucesso! Modelo atualizado.';
                        statusText.style.color = 'var(--success)';
                        btnUploadTrain.removeAttribute('disabled');
                        progressBar.style.width = '100%';
                    } else if (data.status === 'failed') {
                        clearInterval(statusInterval);
                        statusText.textContent = `Falha no treinamento: ${data.error}`;
                        statusText.style.color = 'var(--danger)';
                        btnUploadTrain.removeAttribute('disabled');
                    }
                }
            } catch (err) {
                console.error("Erro ao verificar status:", err);
            }
        }, 2000); // Polling a cada 2 segundos
    }
});
