const urlParams = new URLSearchParams(window.location.search);
const token = urlParams.get('token');

async function confirmEmail(token) {
    try {
        const response = await fetch(`/api/auth/user-verification?token=${token}`, { method: 'GET' });

        if (response.ok) {
            document.getElementById('content').textContent = "The email has been successfully confirmed. You can close this page"; // Обновляем сообщение
        } else {
            document.getElementById('content').textContent = "Error confirming email.";
        }
    } catch (error) {
        console.error('Network error:', error);
        document.getElementById('content').textContent = "Network error.";
    }
}

// Вызываем функцию подтверждения
confirmEmail(token);