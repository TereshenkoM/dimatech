document.addEventListener("DOMContentLoaded", () => {
    window.editUser = function(userId, userEmail, userFirstName, userLastName, userFatherName) {
        document.getElementById('editUserId').value = userId;
        document.getElementById('editEmail').value = userEmail;
        document.getElementById('editFirstName').value = userFirstName;
        document.getElementById('editLastName').value = userLastName;
        document.getElementById('editFatherName').value = userFatherName;

        openModal('editUserModal');
    }
    window.deleteUser = function(userId) {
        axios.delete('/api/admin/user', {
            data: { user_id: userId }
        })
        .then(response => {
            displayUsers();
        })
        .catch(error => {
            console.error('Error delete user:', error);
        });
    }    

    window.openModal = function(modalId) {
        document.getElementById(modalId).style.display = 'block';
    }

    window.closeModal = function(modalId) {
        document.getElementById(modalId).style.display = 'none';
    }

    function displayUsers() {
        axios.get('/api/admin/users')
        .then(response => {
            if (response.data) {
                const users = JSON.parse(response.data).users
                const usersHtml = users.map(user => `
                    <div class="user-item">
                        <div class="user-info">
                            <h3>${user.last_name} ${user.first_name} ${user.father_name}</h3>
                            <p><strong>ID:</strong> ${user.id}</p>
                            <p><strong>Почта:</strong> ${user.email}</p>
                            <p><strong>Счета:</strong> ${user.accounts && user.accounts.length 
                                ? user.accounts.map(a => `ID: ${a.account_id}, Баланс: ${a.balance}`).join(' | ')
                                : 'Нет счетов'}</p>
                        </div>
                        <div class="user-actions">
                            <button onclick="editUser('${user.id}', '${user.email}', '${user.first_name}', '${user.last_name}', '${user.father_name}')" class="edit-btn">Изменить</button>
                            <button onclick="deleteUser('${user.id}')" class="delete-btn">Удалить</button>
                        </div>
                    </div>
                `).join('');
                
                document.getElementById('usersList').innerHTML = usersHtml;
            }
        })
        .catch(console.error);
    }
    

    document.getElementById('addUserBtn').addEventListener('click', () => {
        openModal('addUserModal');
    });

    document.getElementById('addUserForm').addEventListener('submit', (e) => {
        e.preventDefault();
        axios.post('/api/admin/user', {
            email: document.getElementById('newEmail').value,
            first_name: document.getElementById('newFirstName').value,
            last_name: document.getElementById('newLastName').value,
            father_name: document.getElementById('newFatherName').value,
            password: document.getElementById('newPassword').value,
         })
        .then(response => {
            displayUsers();
        })
        .catch(error => {
            console.error('Error create user info:', error);
        });
        closeModal('addUserModal');
        e.target.reset();
    });

    document.getElementById('editUserForm').addEventListener('submit', (e) => {
        axios.patch('/api/admin/user', {
            email: document.getElementById('editEmail').value,
            first_name: document.getElementById('editFirstName').value,
            last_name: document.getElementById('editLastName').value,
            father_name: document.getElementById('editFatherName').value,
            password: document.getElementById('editPassword').value,
         })
        .then(response => {
            displayUsers();
        })
        .catch(error => {
            console.error('Error update user info:', error);
        });
        closeModal('addUserModal');
        e.target.reset();
    });

    displayUsers();
});