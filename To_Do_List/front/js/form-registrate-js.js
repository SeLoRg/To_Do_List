document.getElementById('registration-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Предотвращаем стандартное поведение формы

    const formData = new FormData(this);
    const data = {
        password: formData.get('password'),
        username: formData.get('username'),
        email: formData.get('email')
    };

    // Выполняем fetch-запрос
    fetch('/api/api-bd/users/create-user', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => {
        // Проверяем статус ответа
        if (response.status === 201){
            console.log(response);
            window.open("/email-send", "_blank");
        } else if (!response.ok) { // Если статус не в диапазоне 200-299
            return response.json().then(errorResult => {
                const errorEmailElement = document.getElementById('email-input-error');
                const errorPasswordElement = document.getElementById('password-input-error');

                errorEmailElement.textContent = "";
                errorPasswordElement.textContent = "";

                if (response.status === 422) {
                    console.error('Validation Error:', errorResult);
                    errorPasswordElement.textContent = "Invalid password";
                } else if (response.status === 409){
                    console.error(errorResult);
                    errorEmailElement.textContent = "Email already registered";
                } else if (response.status === 500) {
                    console.error('Server Error:', errorResult);
                    alert('An unexpected server error occurred: ' + errorResult.detail);
                } else {
                    throw new Error(`Unexpected error: ${response.status}`);
                }
            });
        }
        
        return response.json(); // Возвращаем успешный ответ
    })
    .catch(error => {
        // Обработка ошибок сети или других неожиданных ошибок
        console.error('Caught an error:', error);
        alert('An unexpected error occurred: ' + error.message); // Уведомление об ошибке
    });
});


document.getElementById("btn-login").addEventListener("click", function(event) {
    event.preventDefault();
    window.location.href = "/login";
});