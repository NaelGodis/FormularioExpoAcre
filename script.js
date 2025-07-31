document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('questionario-form');
    const successMessage = document.getElementById('success-message');
    const submitBtn = form.querySelector('.submit-btn');
    const btnText = submitBtn.querySelector('.btn-text');

    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Desabilita o botão e mostra loading
        submitBtn.disabled = true;
        btnText.textContent = 'Enviando...';
        
        try {
            // Coleta os dados do formulário
            const formData = new FormData(form);
            const data = {};
            
            // Processa campos normais
            for (let [key, value] of formData.entries()) {
                if (key === 'como_encontrar') {
                    // Para checkboxes múltiplos, cria um array
                    if (!data[key]) {
                        data[key] = [];
                    }
                    data[key].push(value);
                } else {
                    data[key] = value;
                }
            }
            
            // Se não há checkboxes selecionados, define como array vazio
            if (!data.como_encontrar) {
                data.como_encontrar = [];
            }
            
            // Adiciona timestamp
            data.timestamp = new Date().toISOString();
            
            console.log('Dados coletados:', data);
            
            // Envia para o servidor
            const response = await fetch('/submit', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
            
            if (response.ok) {
                // Mostra mensagem de sucesso
                showSuccessMessage();
                
                // Reset do formulário
                form.reset();
            } else {
                throw new Error('Erro ao enviar dados');
            }
            
        } catch (error) {
            console.error('Erro:', error);
            alert('Ocorreu um erro ao enviar suas respostas. Tente novamente.');
        } finally {
            // Reabilita o botão
            submitBtn.disabled = false;
            btnText.textContent = 'Enviar Respostas';
        }
    });
    
    function showSuccessMessage() {
        successMessage.classList.remove('hidden');
        
        // Fecha a mensagem após 3 segundos
        setTimeout(() => {
            successMessage.classList.add('hidden');
        }, 3000);
        
        // Permite fechar clicando no fundo
        successMessage.addEventListener('click', function(e) {
            if (e.target === successMessage) {
                successMessage.classList.add('hidden');
            }
        });
    }
    
    // Adiciona animações suaves aos elementos do formulário
    const questionGroups = document.querySelectorAll('.question-group');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, {
        threshold: 0.1
    });
    
    questionGroups.forEach(group => {
        group.style.opacity = '0';
        group.style.transform = 'translateY(20px)';
        group.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(group);
    });
    
    // Validação em tempo real
    const requiredInputs = form.querySelectorAll('[required]');
    
    requiredInputs.forEach(input => {
        input.addEventListener('change', function() {
            validateInput(this);
        });
        
        input.addEventListener('blur', function() {
            validateInput(this);
        });
    });
    
    function validateInput(input) {
        const questionGroup = input.closest('.question-group');
        const existingError = questionGroup.querySelector('.error-message');
        
        if (existingError) {
            existingError.remove();
        }
        
        if (input.hasAttribute('required') && !input.value.trim()) {
            if (input.type === 'radio') {
                const radioGroup = questionGroup.querySelectorAll('input[type="radio"]');
                const isChecked = Array.from(radioGroup).some(radio => radio.checked);
                if (!isChecked) {
                    showError(questionGroup, 'Este campo é obrigatório');
                }
            } else {
                showError(questionGroup, 'Este campo é obrigatório');
            }
        }
    }
    
    function showError(questionGroup, message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.textContent = message;
        errorDiv.style.color = '#ef4444';
        errorDiv.style.fontSize = '0.875rem';
        errorDiv.style.marginTop = '0.5rem';
        
        questionGroup.appendChild(errorDiv);
    }
    
    // Adiciona efeitos visuais aos elementos interativos
    const interactiveElements = document.querySelectorAll('.radio-option, .checkbox-option');
    
    interactiveElements.forEach(element => {
        element.addEventListener('mouseenter', function() {
            this.style.transform = 'translateX(4px)';
        });
        
        element.addEventListener('mouseleave', function() {
            this.style.transform = 'translateX(0)';
        });
    });
});

