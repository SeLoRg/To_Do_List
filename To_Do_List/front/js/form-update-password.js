document.getElementById("form-update-password").addEventListener("submit", async function (event) {
    event.preventDefault();
    
    const urlParams = new URLSearchParams(window.location.search);
    const email = urlParams.get('email');
    const errorPasswordConfirmElement = document.getElementById('password-confirm-input-error');
    const formData = new FormData(this);

    errorPasswordConfirmElement.textContent = "";
    
    // if  (formData.get('new-password') !== formData.get('confirm-password')){
    //     errorPasswordConfirmElement.textContent = "passwords don't match";
    //     return {"detail": "passwords don't match"}
    // }

    
    const data = {
        password: formData.get('new-password')
    };

    const apiUrl = `/api/api-bd/users/update-user?email=${encodeURIComponent(email)}`;

    fetch(apiUrl, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => {
        if (response.status === 200) {
            console.log(response);
            window.location.href = "/login";
        } else if (!response.ok){
            return response.json().then(errorresult =>{
                const errorPasswordElement = document.getElementById('password-input-error');

                errorPasswordElement.textContent = "";
                
                if (response.status === 422) {
                    console.error(errorResult);
                    errorPasswordElement.textContent = "The password len must be 8 symbols";
                } else {
                    throw new Error(`Unexpected error: ${response.status}`);
                }
            });
        }
        return response.json();
    })
    .catch(error => {
        // Обработка ошибок сети или других неожиданных ошибок
        console.error('Caught an error:', error);
        alert('An unexpected error occurred: ' + error.message); // Уведомление об ошибке
    });


});