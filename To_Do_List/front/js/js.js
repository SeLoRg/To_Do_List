async function updateTaskBlock(date) {
 
    const [year, month, day] = date.split('-');
    const tasks_block = document.getElementById("tasks-block");
    
    const data = {
        day: day,
        month: month,
        year: year
    };


    try {
        const response = await fetch('/api/api-bd/tasks/get-tasks-day', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json', // Указываем тип контента
            },
            body: JSON.stringify(data), // Преобразуем данные в JSON
        });

        if (!response.ok) {
            throw new Error(`Ошибка: ${response.statusText}`);
        }

        const tasks = await response.json();
        tasks_block.innerHTML = ''; // Очищаем предыдущие задачи

        tasks.forEach(task => {
            const newTask = document.createElement("li");
            newTask.className = "main__tasks-cart";
            newTask.innerHTML = `
                <p class="main__task-description">${task.name}</p>
                <div class="main__task-rout">
                    <button type="button" class="main__task-done --task-btn"><i class='bx bx-check'></i></button>
                    <button type="button" class="main__task-delete --task-btn"><i class='bx bx-x'></i></button>
                </div>
            `;
            if (task.status === 'completed'){
                newTask.classList.add('--task-complete')
            }
            tasks_block.appendChild(newTask);

            // Добавляем обработчик события для кнопки удаления
            newTask.querySelector('.main__task-delete').addEventListener('click', function(event) {
                const taskName = task.name; // Используем имя задачи из объекта task
            
                const deleteData = {
                    name: taskName
                };
            
                fetch('/api/api-bd/tasks/delete-task', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json', // Указываем тип контента
                    },
                    body: JSON.stringify(deleteData), // Преобразуем данные в JSON
                })
                .then(response => {
                    if (response.status === 204) {
                        // Удаляем элемент из DOM вместо перезагрузки страницы
                        tasks_block.removeChild(newTask);
                    } else if (!response.ok) {
                        throw new Error('Ошибка при удалении задачи');
                    }
                })
                .catch(error => {
                    console.error('Caught an error:', error);
                    alert('An unexpected error occurred: ' + error.message); // Уведомление об ошибке
                });
            });

            newTask.querySelector('.main__task-done').addEventListener('click', function(event){
                const taskName = task.name; // Используем имя задачи из объекта task
            
                const deleteData = {
                    name: taskName,
                    status: 'completed',
                    date: date

                };
            
                fetch('/api/api-bd/tasks/task-status-update', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json', // Указываем тип контента
                    },
                    body: JSON.stringify(deleteData), // Преобразуем данные в JSON
                })
                .then(response => {
                    if (response.ok) {

                        newTask.classList.toggle('--task-complete');
                    } else if (!response.ok) {
                        throw new Error('Ошибка при обновлении статуса задачи');
                    }
                })
                .catch(error => {
                    console.error('Caught an error:', error);
                    alert('An unexpected error occurred: ' + error.message); // Уведомление об ошибке
                });
            });
        });
    } catch (error) {
        console.error('Ошибка при получении задач:', error);
        alert('An unexpected error occurred while fetching tasks: ' + error.message);
    }
}

fetch('/')
    .then(response => {
        if (response.status === 401) {
            // Перенаправляем пользователя на страницу входа
            window.location.href = '/login';
        } else if (!response.ok) {
            // Обработка других ошибок
            console.error('Ошибка:', response.statusText);
        }
    })
    .catch(error => {
        console.error('Ошибка при выполнении запроса:', error);
    });

document.addEventListener("DOMContentLoaded", () => {
    const dateLoad =document.getElementById('date-load')
    const currentDate = new Date();
    const year = currentDate.getFullYear();
    const month = String(currentDate.getMonth() + 1).padStart(2, '0'); // Добавляем 0 перед месяцем, если он меньше 10
    const day = String(currentDate.getDate()).padStart(2, '0'); // Добавляем 0 перед днем, если он меньше 10
    dateLoad.value = `${year}-${month}-${day}`

    updateTaskBlock(dateLoad.value);
})

document.getElementById('add-task-btn').addEventListener('click', async function (event) {
    event.preventDefault();
    const currentData = document.getElementById('date-load').value

    const formHTML = `
    <div id="add-task-container" class="wrapper" autofocus>
        <form id="add-task-form" action="/api/api-bd/tasks/create-task">
            <h1 class="task">Задача</h1>
            <div class="wrapper__data-input">
                <label for="start">День:</label>
                <input type="date" id="date" name="date" value=${currentData}>
            </div>
            <div class="input-box input-box_task">
                <input name="name" type="string" placeholder="task" required autofocus>
                <i id="task-input-error" class="error-message"></i>
            </div>
    
            <div class="btn-box">
                <button id="create-task-btn" type="submit" class="btn-create" autofocus>Создать задачу</button>
            </div>
        </form>
        </div>
`;

    document.getElementById('form-task-container').insertAdjacentHTML('beforeend', formHTML);
    const button  = document.getElementById("add-task-btn");
    button.disabled=true;
    document.getElementById('add-task-form').addEventListener('submit', async function (event) {
        event.preventDefault();
        const formData = new FormData(this);
        const data = {
            name: formData.get('name'),
            data: document.getElementById('date').value
        };
    
        fetch('/api/api-bd/tasks/create-task', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json', // Указываем тип контента
            },
            body: JSON.stringify(data), // Преобразуем данные в JSON
        })
        .then(response => {
            if (response.ok){
                console.log(response);
                // Выбираем элемент по ID
                const element = document.getElementById("add-task-container");
                const button  = document.getElementById("add-task-btn");
                button.disabled=false;
                // Удаляем элемент
                element.remove();

                updateTaskBlock(document.getElementById('date-load').value)
            } else if (!response.ok) {
                return response.json().then(errorResult => {
                    const errorTasksElement = document.getElementById('task-input-error');
                    errorTasksElement.textContent = "";
                    if (response.status === 422) {
                        console.error(errorResult);
                        errorTasksElement.textContent = errorResult.detail;
                    }
                        throw new Error(`Unexpected error: ${response.status}`);            });
            }
            return response.json();
        });
    });
});

const user_logo_bx = document.getElementById('user-logo-bx');


user_logo_bx.addEventListener('click', async function(event){
    const formHTML = `
                <div id="user-settings" class="user-settings-wrapper">
                    <div id="user-settings-logo-bx" class="user-settings-wrapper__user-logo-bx">
                        <img src="/front/images/auth.jpg" alt="user-logo" class="user-settings-wrapper__user-logo">
                        <p class="user-setting-wrapper__uer-name">Selorg</p>
                    </div>
                    <button class="user-settings-wrapper__exit">Выйти</button>
                    <button class="user-settings-wrapper__accounts-box"></button>
                </div>
    `;
    document.getElementById('header-inner').insertAdjacentHTML('beforeend', formHTML);
    user_logo_bx.classList.toggle('--user-logo-bx-active');
    user_logo_bx.disabled = true;
});

const humburger_container = document.getElementById('humburger-container');
humburger_container.addEventListener('click', async function(event){
    const formHTML = `
            <div id="main-nav" class="main__nav">
                <ul class="main__nav-block nav-block">
                    <li id="nav-block-element-groups" class="nav-block__element --groups">Группы</li>
                    <li id="nav-block-element-friends" class="nav-block__element --friends">Друзья</li>
                    <li id="nav-block-element-messages" class="nav-block__element --messages">Сообщения</li>
                    <li id="nav-block-element-tasks" class="nav-block__element --tasks">Задачи</li>
                </ul>
            </div>
    `;
    document.getElementById('header-inner').insertAdjacentHTML('beforeend', formHTML);
    humburger_container.classList.toggle('--humburger-active');
    humburger_container.disabled = true;

    
});

const user_settings_logo_bx = document.getElementById('user-settings-logo-bx');

// user_settings_logo_bx.addEventListener('click', function(event){

// });




document.getElementById('date-load').addEventListener('change', function() {
    const currentData = document.getElementById('date-load').value;
    updateTaskBlock(currentData);
});

document.addEventListener("DOMContentLoaded", () => {
    const dateLoad =document.getElementById('date-load')
    const currentDate = new Date();
    const year = currentDate.getFullYear();
    const month = String(currentDate.getMonth() + 1).padStart(2, '0'); // Добавляем 0 перед месяцем, если он меньше 10
    const day = String(currentDate.getDate()).padStart(2, '0'); // Добавляем 0 перед днем, если он меньше 10
    dateLoad.value = `${year}-${month}-${day}`

    updateTaskBlock(dateLoad.value);
})

document.body.addEventListener('click', function(event){
    // event.preventDefault();
    if (!event.target.closest('.wrapper') && event.target.tagName !== 'BUTTON'){
        const element = document.getElementById("add-task-container");
        if (element !== null) {
            element.remove();
            const button  = document.getElementById("add-task-btn");
            button.disabled=false;
        }
    }

    if (!event.target.closest('.user-settings-wrapper') && event.target.tagName !== 'BUTTON'){
        const element = document.getElementById("user-settings");
        if (element !== null) {
            element.remove();
            user_logo_bx.classList.toggle('--user-logo-bx-active');
            user_logo_bx.disabled=false;
        }
    }
    if (!event.target.closest('.header__humburger-container') && event.target.tagName !== 'BUTTON'){
        const element = document.getElementById("main-nav");
        if (element !== null) {
            element.remove();
            humburger_container.classList.toggle('--humburger-active');
            humburger_container.disabled=false;
        }
    }
});