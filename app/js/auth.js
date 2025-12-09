/**
 * FaceBoi - Sistema de Autenticação (MVP Fake)
 */

const AUTH_KEY = 'faceboi_auth';

// Verifica se está logado
function isAuthenticated() {
    return localStorage.getItem(AUTH_KEY) !== null;
}

// Obtém dados do usuário logado
function getCurrentUser() {
    const auth = localStorage.getItem(AUTH_KEY);
    return auth ? JSON.parse(auth) : null;
}

// Faz login
function login(email, password) {
    // Simula verificação (MVP fake)
    if (email === DEMO_USER.email && password === DEMO_USER.password) {
        const userData = {
            email: DEMO_USER.email,
            name: DEMO_USER.name,
            farm: DEMO_USER.farm,
            loginTime: new Date().toISOString()
        };
        localStorage.setItem(AUTH_KEY, JSON.stringify(userData));
        return { success: true, user: userData };
    }
    return { success: false, error: 'Credenciais inválidas' };
}

// Faz logout
function logout() {
    localStorage.removeItem(AUTH_KEY);
    window.location.href = 'login.html';
}

// Handler do formulário de login
function setupLoginForm() {
    const form = document.getElementById('loginForm');
    if (!form) return;
    
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const submitBtn = form.querySelector('.btn-login');
        
        // Adiciona estado de loading
        submitBtn.classList.add('loading');
        
        // Simula delay de rede
        await new Promise(resolve => setTimeout(resolve, 800));
        
        const result = login(email, password);
        
        submitBtn.classList.remove('loading');
        
        if (result.success) {
            window.location.href = 'dashboard.html';
        } else {
            // Mostra erro
            const emailGroup = document.getElementById('email').parentElement;
            emailGroup.classList.add('error');
            
            let errorMsg = emailGroup.querySelector('.error-message');
            if (!errorMsg) {
                errorMsg = document.createElement('span');
                errorMsg.className = 'error-message';
                emailGroup.appendChild(errorMsg);
            }
            errorMsg.textContent = result.error;
            errorMsg.style.display = 'block';
            
            // Remove erro após 3 segundos
            setTimeout(() => {
                emailGroup.classList.remove('error');
                errorMsg.style.display = 'none';
            }, 3000);
        }
    });
}

// Protege rotas que precisam de autenticação
function protectRoute() {
    const currentPage = window.location.pathname.split('/').pop();
    
    if (currentPage === 'dashboard.html' && !isAuthenticated()) {
        window.location.href = 'login.html';
        return false;
    }
    
    if (currentPage === 'login.html' && isAuthenticated()) {
        window.location.href = 'dashboard.html';
        return false;
    }
    
    return true;
}

// Inicialização
document.addEventListener('DOMContentLoaded', () => {
    protectRoute();
    setupLoginForm();
    
    // Setup logout button
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', logout);
    }
});
