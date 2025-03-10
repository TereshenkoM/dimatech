document.addEventListener("DOMContentLoaded", () => {
    console.log( document.getElementById("getSignature"))
    document.getElementById("getSignature").addEventListener("click", async (e) => {
        event.preventDefault();
        
        const transactionId = document.getElementById("transactionId").value;
        const userId = document.getElementById("userId").value;
        const accountId = document.getElementById("accountId").value;
        const amount = document.getElementById("amount").value;
        const resultDiv = document.getElementById("result");        

        axios.post("/api/signature", {
            transaction_id: transactionId,
            user_id: userId,
            account_id: accountId,
            amount: amount,
        })
            .then(response => {
                const signature = response.data.signature;
                try {
                    resultDiv.textContent = `Сгенерированная подпись: ${signature}`;
                    resultDiv.className = "result success";
                
                } catch (error) {
                    resultDiv.textContent = "Ошибка при генерации подписи: " + error.message;
                    resultDiv.className = "result error";
                }
            })
            .catch(error => {
                console.error("Error fetching user info:", error);
            });
    })
});
