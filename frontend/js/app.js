const API_URL = "http://localhost:8000/api";

// State
let token = localStorage.getItem('token');

// DOM Elements
const authView = document.getElementById('auth-view');
const appView = document.getElementById('app-view');
const loginForm = document.getElementById('login-form');
const messagesDiv = document.getElementById('messages');
const userInput = document.getElementById('user-input');

// Init
if (token) {
    showApp();
}

// Login Logic
loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    const formData = new FormData();
    formData.append('username', email);
    formData.append('password', password);

    try {
        const res = await fetch(`${API_URL}/auth/login`, {
            method: 'POST',
            body: formData
        });
        const data = await res.json();
        if (res.ok) {
            token = data.access_token;
            localStorage.setItem('token', token);
            showApp();
        } else {
            alert(data.detail);
        }
    } catch (err) {
        console.error(err);
    }
});

function showApp() {
    authView.classList.add('hidden');
    appView.classList.remove('hidden');
}

function logout() {
    localStorage.removeItem('token');
    location.reload();
}

// Routing
function router(viewName) {
    document.querySelectorAll('.view').forEach(el => el.classList.remove('active'));
    document.getElementById(`${viewName}-view`).classList.add('active');
}

// Chat Functionality
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && userInput.value.trim() !== '') {
        sendMessage(userInput.value);
        userInput.value = '';
    }
});

async function sendMessage(text) {
    // Add User Message
    appendMessage('user', text);

    try {
        const res = await fetch(`${API_URL}/chat/query`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ question: text })
        });
        const data = await res.json();
        appendMessage('ai', data.answer, data.sources);
    } catch (err) {
        appendMessage('ai', "Error connecting to server.");
    }
}

function appendMessage(role, text, sources = []) {
    const div = document.createElement('div');
    div.className = `message ${role}`;
    
    let sourceHtml = sources.length ? `<br><small style="color: #aaa;">Sources: ${sources.join(', ')}</small>` : '';
    
    div.innerHTML = `<div class="bubble">${text}${sourceHtml}</div>`;
    messagesDiv.appendChild(div);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

// Document Upload
async function uploadFile() {
    const fileInput = document.getElementById('file-upload');
    if (fileInput.files.length === 0) return;

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    try {
        const res = await fetch(`${API_URL}/docs/upload`, {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${token}` },
            body: formData
        });
        const data = await res.json();
        alert(data.info);
        
        const li = document.createElement('li');
        li.innerText = fileInput.files[0].name;
        document.getElementById('doc-list').appendChild(li);
    } catch (err) {
        console.error(err);
    }
}