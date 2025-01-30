document.getElementById('recovery-password-form').addEventListener('submit', async function(event) {
    event.preventDefault(); // Предотвращаем стандартное поведение формы

    // Создаем объект FormData из формы
    const formData = new FormData(this);

    // Преобразуем FormData в JSON
    const data = {
        email: formData.get('email'),
    };


        fetch('/api/auth/send-email-update-password', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json', // Указываем тип контента
            },
            body: JSON.stringify(data), // Преобразуем данные в JSON
        })
        .then(response => {
            if (response.status === 200){
                console.log(response);
                window.location.href = "/email-send";
            } else if (!response.ok) {
                return response.json().then(errorResult => {
                        throw new Error(`Unexpected error: ${response.status}`);

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
