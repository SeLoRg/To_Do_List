document.getElementById('login-form').addEventListener('submit', async function(event) {
    event.preventDefault(); // Предотвращаем стандартное поведение формы

    // Создаем объект FormData из формы
    const formData = new FormData(this);

    // Преобразуем FormData в JSON
    const data = {
        email: formData.get('email'),
        password: formData.get('password'),
    };


        fetch('/api/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json', // Указываем тип контента
            },
            body: JSON.stringify(data), // Преобразуем данные в JSON
        })
        .then(response => {
            if (response.status === 200){
                console.log(response);
                window.location.href = "/";
            } else if (!response.ok) {
                return response.json().then(errorResult => {
                    const errorEmailElement = document.getElementById('email-input-error');
                    const errorPasswordElement = document.getElementById('password-input-error');

                    errorEmailElement.textContent = "";
                    errorPasswordElement.textContent = "";

                    if (response.status === 403) {
                        console.error(errorResult);
                        errorEmailElement.textContent = "Email is not confirmed";
                        window.open("/confirm-email", "_blank");
                    } else if (response.status === 404){
                        console.error(errorResult);
                        errorEmailElement.textContent = "Invalid email";
                    } else if (response.status === 422) {
                        console.error(errorResult);
                        errorPasswordElement.textContent = "Invalid password";
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

// const rememberMeCheckbox = document.getElementById('remember-me');

// rememberMeCheckbox.addEventListener('click', function() {
//     const formElement = document.getElementById("login-form")
//     if (this.checked) {
//         // console.log('Checkbox is checked'); 
//         formElement.setAttribute("autocomplete", "on");
//     } else {
//         // console.log('Checkbox is unchecked');
//         formElement.setAttribute("autocomplete", "off");
//     }
// });