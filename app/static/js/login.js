document.addEventListener("DOMContentLoaded", (event) => {
    console.log(document.getElementById('loginForm'))
    document.getElementById('loginForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        
        try {
            await axios.post('/auth/login', {
                email: email,
                password: password
            });
            
            window.location.href = '/';
            
        } catch (error) {
            let errorMessage = 'Ошибка входа';
            
            if (error.response) {
                if (error.response.status === 401) {
                    errorMessage = 'Неверный email или пароль';
                } else if (error.response.status === 403) {
                    errorMessage = 'Пользователь заблокирован';
                }
            }
            
            const errorDiv = document.createElement('div');
            errorDiv.className = 'error-message';
            errorDiv.textContent = errorMessage;
            
            const form = document.getElementById('loginForm');
            const existingError = form.querySelector('.error-message');
            if (existingError) form.removeChild(existingError);
            
            form.appendChild(errorDiv);    
        }
    });
})