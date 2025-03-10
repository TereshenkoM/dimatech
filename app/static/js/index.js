document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("logoutBtn").addEventListener("click", async (e) => {
        e.preventDefault();
        try {
            await axios.post("/auth/logout");
            window.location.href = "/login";
        } catch (error) {
            console.error("Logout failed:", error);
        }
    });

    axios.get("/api/user_info")
        .then(response => {
            let userData = JSON.parse(response.data);
            let userId = userData.user_id;
            let userFullName = userData.user_fullname;
            let userEmail = userData.email;

            document.getElementById("userDetails").innerHTML = `
                <p><strong>ID:</strong> ${userId}</p>
                <p><strong>Электронная почта:</strong> ${userEmail}</p>
                <p><strong>Полное имя:</strong> ${userFullName}</p>
        `;
        })
        .catch(error => {
            console.error("Error fetching user info:", error);
        });
    
    axios.get("/api/transaction")
        .then(response => {
            if (response.data) {
                const transactions = JSON.parse(response.data).transactions;
                const transactionsHtml = transactions.map(transaction => `
                    <div class="payment-item">
                        <p><strong>Дата:</strong> ${transaction.created_at}</p>
                        <p><strong>Сумма:</strong> ${transaction.amount}</p>
                    </div>
                    <hr>
                `).join("");
                document.getElementById("paymentsList").innerHTML = transactionsHtml;
            }
        })
        .catch(error => {
            console.error("Error fetching transaction info:", error);
        });
    
    
    axios.get("/api/account_info")
        .then(response => {
            if (response.data) {
                const accounts = JSON.parse(response.data).accounts;
                const accountsHtml = accounts.map(account => `
                    <div class="account-item">
                        <p><strong>ID:</strong> ${account.id}</p>
                        <p><strong>Баланс:</strong> ${account.balance}</p>
                        <p><strong>Создан:</strong> ${account.created_at}</p>
                    </div>
                    <hr>
                `).join("");
                
                document.getElementById("accountsList").innerHTML = accountsHtml;
            }
        })
        .catch(error => {
            console.error("Error fetching account info:", error);
        });
    
    // axios.post("/api/transaction", {
    //     transaction_id: "1eae174f-7cd0-472c-bd36-35660f00132b",
    //     user_id: "5d0ff10f-7c2d-4555-8292-595c280bf621",
    //     account_id: "fas-ssas-ddd",
    //     amount: 90,
    //     signature: "2dee703eee43a0a3147acc1d5117bdac383859bcf94c670c9f6b5b4b1b203e73"
    // })
    //     .then(response => {
    //         const trans = response.data;
    //         console.log(trans)
    //     })
    //     .catch(error => {
    //         console.error("Error fetching user info:", error);
    //     });
});