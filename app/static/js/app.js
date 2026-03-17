let token = localStorage.getItem("token");

function parseJwt(token) {
    try {
        const base64Url = token.split('.')[1];
        const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
        return JSON.parse(atob(base64));
    } catch (e) { return {}; }
}
function isTokenExpired(token) {
    const c = parseJwt(token);
    if (!c.exp) return true;
    return c.exp * 1000 < Date.now();
}

function login(event) {
    if (event) event.preventDefault();
    fetch("/api/auth/login", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            username: document.getElementById("username").value,
            password: document.getElementById("password").value
        })
    })
    .then(res => {
        if (!res.ok) throw new Error('Login failed');
        return res.json();
    })
    .then(data => {
        localStorage.setItem("token", data.access_token);
        window.location.href = "/dashboard";
    })
    .catch(err => {
        alert('Credenciales inválidas o error en servidor');
        console.error(err);
    });
}

function createProcess(event) {
    if (event) event.preventDefault();
    const titleEl = document.getElementById("title");
    const descEl = document.getElementById("description");
    const title = titleEl.value.trim();
    const description = descEl.value.trim();
    if (!title || !description) {
        alert('Título y descripción son obligatorios');
        return;
    }
    fetch("/api/process/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + localStorage.getItem("token")
        },
        body: JSON.stringify({
            title: title,
            description: description
        })
    })
    .then(res => {
        if (!res.ok) return res.json().then(err => { throw err; });
        return res.json();
    })
    .then(data => {
        loadProcesses();
    })
    .catch(err => {
        const msg = err.message || err.msg || 'Error creando proceso';
        alert(msg);
        console.error(err);
    });
}

function loadProcesses() {
    fetch("/api/process/", {
        headers: {
            "Authorization": "Bearer " + localStorage.getItem("token")
        }
    })
    .then(res => {
        if (!res.ok) return res.json().then(err => { throw err; });
        return res.json();
    })
    .then(data => {
        const list = document.getElementById("processList");
        list.innerHTML = "";
        let count = 0;
        if (Array.isArray(data)) {
            count = data.length;
            const statusColors = {
                pending: "warning",
                in_progress: "primary",
                completed: "success"
            };
            const statusLabels = {
                pending: "Pendiente",
                in_progress: "En progreso",
                completed: "Completado"
            };
            data.forEach(p => {
                const color = statusColors[p.status] || "secondary";
                const label = statusLabels[p.status] || p.status;
                list.innerHTML += `
                <li class="list-group-item">
                    <div class="d-flex justify-content-between align-items-start">
                        <div>
                            <strong class="text-dark">${p.title}</strong>
                            <br><small class="text-muted">${p.description || ''}</small>
                            ${p.created_at ? `<br><small class="text-muted">📅 ${p.created_at}</small>` : ''}
                        </div>
                        <span class="badge bg-${color} ms-2">${label}</span>
                    </div>
                </li>`;
            });
        } else {
            console.warn('unexpected loadProcesses response', data);
        }
        document.getElementById('processCount').textContent = count;
    })
    .catch(err => {
        alert(err.message || 'Error al cargar procesos');
        console.error(err);
    });
}

function logout() {
    localStorage.removeItem("token");
    window.location.href = "/";
}

function createUser(event) {
    if (event) event.preventDefault();
    const username = document.getElementById('newUsername').value;
    const password = document.getElementById('newPassword').value;
    const role = document.getElementById('newRole').value;
    fetch('/api/auth/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + localStorage.getItem('token')
        },
        body: JSON.stringify({ username, password, role })
    })
    .then(res => {
        if (!res.ok) return res.json().then(err => { throw err; });
        return res.json();
    })
    .then(data => {
        loadUsers();
    })
    .catch(err => {
        alert(err.message || err.msg || 'Error creando usuario');
        console.error(err);
    });
}

function loadUsers() {
    fetch('/api/auth/users', {
        headers: { 'Authorization': 'Bearer ' + localStorage.getItem('token') }
    })
    .then(res => {
        if (!res.ok) return res.json().then(err => { throw err; });
        return res.json();
    })
    .then(data => {
        const list = document.getElementById('userList');
        list.innerHTML = '';
        let count = 0;
        if (Array.isArray(data)) {
            count = data.length;
            data.forEach(u => {
                list.innerHTML += `<li class="list-group-item">${u.username} (${u.role})</li>`;
            });
        }
        document.getElementById('userCount').textContent = count;
    })
    .catch(err => {
        console.error('loadUsers error', err);
    });
}

function loadLogs() {
    fetch('/api/admin/logs', {
        headers: { 'Authorization': 'Bearer ' + localStorage.getItem('token') }
    })
    .then(res => {
        if (!res.ok) return res.json().then(err => { throw err; });
        return res.json();
    })
    .then(data => {
        const list = document.getElementById('logList');
        list.innerHTML = '';
        let count = 0;
        if (Array.isArray(data)) {
            count = data.length;
            data.forEach(l => {
                list.innerHTML += `<li class="list-group-item">${l.user_id}: ${l.action}</li>`;
            });
        }
        document.getElementById('logCount').textContent = count;
    })
    .catch(err => {
        console.error('loadLogs error', err);
    });
}

function loadDemo() {
    fetch('/api/process/demo', {
        method: 'POST',
        headers: { 'Authorization': 'Bearer ' + localStorage.getItem('token') }
    })
    .then(res => res.json())
    .then(data => {
        loadProcesses();
        alert(data.message || 'Demo cargado');
    })
    .catch(err => {
        alert('Error cargando demo');
        console.error(err);
    });
}

// initialize on DOM
window.addEventListener('DOMContentLoaded', () => {    const tok = localStorage.getItem('token');
    if (tok) {
        if (isTokenExpired(tok)) {
            logout();
            return;
        }
        const claims = parseJwt(tok);
        // show username at top
        const welcome = document.getElementById('welcomeBanner');
        if (welcome && claims.sub) {
            welcome.innerHTML = `<div class="alert alert-success">Bienvenido, <strong>${claims.sub}</strong> (${claims.role || 'usuario'})</div>`;
        }
        if (claims.role === 'admin') {
            document.getElementById('userCard').style.display = 'block';
            document.getElementById('logsCard').style.display = 'block';
            loadUsers();
            loadLogs();
        } else {
            const note = document.createElement('div');
            note.className = 'alert alert-info';
            note.textContent = 'Sesión de usuario normal: funcionalidades de administrador ocultas.';
            document.querySelector('.container').prepend(note);
        }
    }
    loadProcesses();
});

