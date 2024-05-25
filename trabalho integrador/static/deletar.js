document.getElementById('deletar').addEventListener('click', function(event) {
    event.preventDefault(); // Impede o redirecionamento imediato

    let password = prompt('Por favor, insira a senha:');

    if (password) {
        fetch('/verify-password', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ password: password })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Se a senha estiver correta, redirecione para o href original
                window.location.href = event.target.href;
            } else {
                alert('Senha incorreta. Tente novamente.');
            }
        })
        .catch(error => console.error('Error:', error));
    }
});