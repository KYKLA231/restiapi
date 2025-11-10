document.addEventListener('DOMContentLoaded', () => {
    // Flash messages
    const flashMessages = document.querySelectorAll('.alert');
    flashMessages.forEach(message => {
        setTimeout(() => {
            message.style.opacity = '0';
            setTimeout(() => message.remove(), 300);
        }, 3000);
    });

    // Form validation: перехватываем только формы с data-ajax="true"
    // Это предотвращает бесконечную загрузку при обычных submit+redirect
    const forms = document.querySelectorAll('form[data-ajax="true"]');
    forms.forEach(form => {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(form);
            const data = Object.fromEntries(formData.entries());

            try {
                const response = await fetch(form.action, {
                    method: form.method || 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data),
                    redirect: 'follow'
                });

                // Попытка распарсить JSON, но если ответ не JSON — обработаем это
                let result = null;
                const contentType = response.headers.get('content-type') || '';
                if (contentType.includes('application/json')) {
                    result = await response.json();
                } else {
                    // Если сервер вернул redirect или HTML — считаем, что успех
                    result = {};
                }

                if (!response.ok) {
                    throw new Error(result.detail || 'Ошибка при отправке формы');
                }

                // Показать успех и очистить форму
                const alert = document.createElement('div');
                alert.className = 'alert alert-success';
                alert.textContent = 'Успешно!';
                form.insertBefore(alert, form.firstChild);
                form.reset();

                // Перенаправление, если указано
                if (form.dataset.redirect) {
                    setTimeout(() => {
                        window.location.href = form.dataset.redirect;
                    }, 800);
                }
            } catch (error) {
                const alert = document.createElement('div');
                alert.className = 'alert alert-danger';
                alert.textContent = error.message || 'Ошибка';
                form.insertBefore(alert, form.firstChild);
            }
        });
    });

    // User profile dropdown
    const profileDropdown = document.querySelector('.profile-dropdown');
    if (profileDropdown) {
        profileDropdown.addEventListener('click', () => {
            const menu = profileDropdown.querySelector('.dropdown-menu');
            menu.classList.toggle('show');
        });
    }

    // Mobile menu toggle
    const menuToggle = document.querySelector('.menu-toggle');
    const navbarNav = document.querySelector('.navbar-nav');
    if (menuToggle && navbarNav) {
        menuToggle.addEventListener('click', () => {
            navbarNav.classList.toggle('show');
        });
    }
});