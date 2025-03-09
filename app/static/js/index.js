document.addEventListener("DOMContentLoaded", () => {
    document.getElementById('logoutBtn').addEventListener('click', async (e) => {
        e.preventDefault();
        
        try {
            await axios.post('/auth/logout');
            window.location.href = '/login';
        } catch (error) {
            console.error('Ошибка при выходе:', error);
        }
    });
});