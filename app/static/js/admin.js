document.addEventListener("DOMContentLoaded", () => {
    window.editUser = function(userId, userEmail, userFirstName, userLastName, userFatherName) {
        document.getElementById('editUserId').value = userId;
        document.getElementById('editEmail').value = userEmail;
        document.getElementById('editFirstName').value = userFirstName;
        document.getElementById('editLastName').value = userLastName;
        document.getElementById('editFatherName').value = userFatherName;

        openModal('editUserModal');
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
            const users = response.data.users;
            const usersHtml = users.map(user => `
                <div class="user-item">
                    <div class="user-info">
                        <h3>${user.last_name} ${user.first_name} ${user.father_name}</h3>
                        <p><strong>ID:</strong> ${user.id}</p>
                        <p><strong>Почта:</strong> ${user.email}</p>
                    </div>
                    <div class="user-actions">
                        <button onclick="editUser('${user.id}', '${user.email}', '${user.first_name}', '${user.last_name}', '${user.father_name}')" class="edit-btn">Изменить</button>
                        <button onclick="deleteUser('${user.id}')" class="delete-btn">Удалить</button>
                    </div>
                </div>
            `).join('');
            
            document.getElementById('usersList').innerHTML = usersHtml;
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
            firstName: document.getElementById('newFirstName').value,
            lastName: document.getElementById('newLastName').value,
            fatherName: document.getElementById('newFatherName').value,
            password: document.getElementById('newPassword').value,
         })
        .then(response => {
            const trans = response.data;
            console.log(trans)
        })
        .catch(error => {
            console.error('Error fetching user info:', error);
        });
        displayUsers();
        closeModal('addUserModal');
        e.target.reset();
    });

    displayUsers();
});