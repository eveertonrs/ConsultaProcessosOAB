document.addEventListener("DOMContentLoaded", function() {
    const loginForm = document.getElementById("login-form");

    loginForm.addEventListener("submit", function(event) {
        event.preventDefault();

        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;

        // Realizar uma solicitação AJAX para o Flask para autenticar o usuário
        fetch('/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username, password })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Autenticação bem-sucedida, redirecionar para a página inicial
                    window.location.href = '/home';
                } else {
                    // Exibir mensagem de erro de autenticação
                    const errorDiv = document.getElementById("error-message");
                    errorDiv.textContent = "Usuário ou senha incorretos. Tente novamente.";
                }
            })
            .catch(error => {
                console.error('Erro na solicitação AJAX:', error);
            });
    });
});