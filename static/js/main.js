function toggleSession() {
    const isLoggedIn = document.body.classList.toggle('logged-in');
    alert(isLoggedIn ? 'Sesión iniciada' : 'Sesión cerrada');
    // Aquí puedes agregar más lógica para manejar el estado de la sesión.
}

// main.js

// Function to toggle the theme
function toggleTheme() {
    // Select the body element
    const body = document.body;

    // Toggle the light theme class
    body.classList.toggle('light-theme');

    // Store the current theme in local storage to persist on page reload
    if (body.classList.contains('light-theme')) {
        localStorage.setItem('theme', 'light');
    } else {
        localStorage.setItem('theme', 'dark');
    }
}

// Load the theme from local storage when the page loads
document.addEventListener('DOMContentLoaded', () => {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'light') {
        document.body.classList.add('light-theme');
    }
});