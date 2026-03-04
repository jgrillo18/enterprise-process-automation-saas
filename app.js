// simple static login/dashboard logic for demo
function login(event) {
    if (event) event.preventDefault();
    const u = document.getElementById('username').value;
    const p = document.getElementById('password').value;
    if (u === 'admin' && p === 'admin') {
        document.getElementById('loginScreen').style.display = 'none';
        document.getElementById('dashboardScreen').style.display = 'block';
        document.getElementById('userLabel').textContent = u;
    } else {
        alert('Usuario o contraseña incorrectos');
    }
}
function logout() {
    document.getElementById('dashboardScreen').style.display = 'none';
    document.getElementById('loginScreen').style.display = 'block';
}
console.log('demo script loaded');

