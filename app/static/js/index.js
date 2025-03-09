document.addEventListener("DOMContentLoaded", () => {
    document.getElementById('logoutBtn').addEventListener('click', async (e) => {
        e.preventDefault();
        try {
            await axios.post('/auth/logout');
            window.location.href = '/login';
        } catch (error) {
            console.error('Logout failed:', error);
        }
    });

    axios.get('/api/user_info')
        .then(response => {
            let userData = response.data;
            let userId = userData.user_id;
            let userFullName = userData.user_fullname;
            let userEmail = userData.email;

            document.getElementById('userDetails').innerHTML = `
                <p><strong>ID:</strong> ${userId}</p>
                <p><strong>Электронная почта:</strong> ${userEmail}</p>
                <p><strong>Полное имя:</strong> ${userFullName}</p>
        `;
        })
        .catch(error => {
            console.error('Error fetching user info:', error);
        });
    
    axios.get('/api/account_info')
        .then(response => {
            const accounts = response.data.accounts;
            
            const accountsHtml = accounts.map(account => `
                <div class="account-item">
                    <p><strong>ID:</strong> ${account.id}</p>
                    <p><strong>Баланс:</strong> ${account.balance}</p>
                    <p><strong>Создан:</strong> ${account.created_at}</p>
                </div>
            `).join('');
            
            document.getElementById('accountsList').innerHTML = accountsHtml;
        })
        .catch(error => {
            console.error('Error fetching user info:', error);
        });
    
});