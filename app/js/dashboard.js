/**
 * FaceBoi - Dashboard Controller
 */

document.addEventListener('DOMContentLoaded', () => {
    initDashboard();
});

function initDashboard() {
    // Carrega dados do usuário
    loadUserInfo();
    
    // Configura data atual
    setCurrentDate();
    
    // Carrega dados iniciais
    loadRecentActivity();
    loadCattleGrid();
    loadAlerts();
    
    // Configura navegação
    setupNavigation();
    
    // Configura modal
    setupModal();
    
    // Configura filtros
    setupFilters();
    
    // Mobile menu
    setupMobileMenu();
}

// Carrega informações do usuário
function loadUserInfo() {
    const user = getCurrentUser();
    if (user) {
        document.getElementById('userName').textContent = user.name || 'Agricultor';
        document.getElementById('userFarm').textContent = user.farm || 'Fazenda';
    }
}

// Define data atual
function setCurrentDate() {
    const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    const date = new Date().toLocaleDateString('pt-BR', options);
    document.getElementById('currentDate').textContent = date.charAt(0).toUpperCase() + date.slice(1);
}

// Carrega atividades recentes
function loadRecentActivity() {
    const container = document.getElementById('recentActivity');
    if (!container) return;
    
    container.innerHTML = MOCK_RECENT_ACTIVITY.map(activity => `
        <div class="activity-item" data-cattle-id="${activity.cattleId}">
            <div class="activity-icon">🐄</div>
            <div class="activity-info">
                <div class="activity-title">${activity.name} <small>(${activity.cattleId})</small></div>
                <div class="activity-meta">${activity.weight}kg • Visita #${activity.cochoVisit} do dia</div>
            </div>
            <div class="activity-time">${activity.time}</div>
        </div>
    `).join('');
    
    // Adiciona click handler para abrir modal
    container.querySelectorAll('.activity-item').forEach(item => {
        item.addEventListener('click', () => {
            const cattleId = item.dataset.cattleId;
            openCattleModal(cattleId);
        });
    });
}

// Carrega grid de gado
function loadCattleGrid(filter = {}) {
    const container = document.getElementById('cattleGrid');
    if (!container) return;
    
    let cattle = [...MOCK_CATTLE];
    
    // Aplica filtros
    if (filter.search) {
        const search = filter.search.toLowerCase();
        cattle = cattle.filter(c => 
            c.id.toLowerCase().includes(search) || 
            c.name.toLowerCase().includes(search)
        );
    }
    
    if (filter.weight) {
        cattle = cattle.filter(c => {
            if (filter.weight === 'light') return c.weight < 350;
            if (filter.weight === 'medium') return c.weight >= 350 && c.weight <= 450;
            if (filter.weight === 'heavy') return c.weight > 450;
            return true;
        });
    }
    
    if (filter.health) {
        cattle = cattle.filter(c => c.status === filter.health);
    }
    
    container.innerHTML = cattle.map(c => {
        const changeClass = c.weightChange >= 0 ? 'positive' : 'negative';
        const changeSign = c.weightChange >= 0 ? '+' : '';
        
        return `
            <div class="cattle-card" data-cattle-id="${c.id}">
                <div class="cattle-card-header">
                    <span class="cattle-id">${c.id}</span>
                    <span class="cattle-status ${c.status}">${getStatusLabel(c.status)}</span>
                </div>
                <div class="cattle-card-body">
                    <div class="cattle-weight">
                        <span class="weight-value">${c.weight}</span>
                        <span class="weight-unit">kg</span>
                        <div class="weight-change ${changeClass}">${changeSign}${c.weightChange}kg (última semana)</div>
                    </div>
                    <div class="cattle-stats">
                        <div class="cattle-stat">
                            <div class="cattle-stat-value">${c.cochoVisits}</div>
                            <div class="cattle-stat-label">Visitas hoje</div>
                        </div>
                        <div class="cattle-stat">
                            <div class="cattle-stat-value">${c.breed}</div>
                            <div class="cattle-stat-label">Raça</div>
                        </div>
                        <div class="cattle-stat">
                            <div class="cattle-stat-value">${c.age}</div>
                            <div class="cattle-stat-label">Idade</div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }).join('');
    
    // Adiciona click handler
    container.querySelectorAll('.cattle-card').forEach(card => {
        card.addEventListener('click', () => {
            openCattleModal(card.dataset.cattleId);
        });
    });
}

// Carrega alertas
function loadAlerts() {
    const container = document.getElementById('alertsList');
    if (!container) return;
    
    if (MOCK_ALERTS.length === 0) {
        container.innerHTML = `
            <div class="reports-placeholder">
                <div class="placeholder-icon">✅</div>
                <h3>Nenhum Alerta</h3>
                <p>Seu rebanho está saudável! Continue monitorando.</p>
            </div>
        `;
        return;
    }
    
    container.innerHTML = MOCK_ALERTS.map(alert => `
        <div class="alert-item ${alert.type}">
            <div class="alert-icon">${alert.type === 'critical' ? '🚨' : '⚠️'}</div>
            <div class="alert-content">
                <div class="alert-title">${alert.title}</div>
                <div class="alert-description">${alert.description}</div>
                <div class="alert-time">${alert.timestamp}</div>
            </div>
            <button class="alert-action" data-cattle-id="${alert.cattleId}">Ver Animal</button>
        </div>
    `).join('');
    
    // Adiciona click handler
    container.querySelectorAll('.alert-action').forEach(btn => {
        btn.addEventListener('click', () => {
            openCattleModal(btn.dataset.cattleId);
        });
    });
}

// Retorna label do status
function getStatusLabel(status) {
    const labels = {
        healthy: 'Saudável',
        warning: 'Atenção',
        critical: 'Crítico'
    };
    return labels[status] || status;
}

// Configura navegação da sidebar
function setupNavigation() {
    const navItems = document.querySelectorAll('.nav-item');
    const sections = document.querySelectorAll('.content-section');
    const pageTitle = document.getElementById('pageTitle');
    
    const titles = {
        overview: 'Visão Geral',
        cattle: 'Rebanho',
        alerts: 'Alertas',
        reports: 'Relatórios'
    };
    
    navItems.forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            const section = item.dataset.section;
            
            // Atualiza nav ativo
            navItems.forEach(n => n.classList.remove('active'));
            item.classList.add('active');
            
            // Mostra seção correta
            sections.forEach(s => s.classList.remove('active'));
            document.getElementById(section).classList.add('active');
            
            // Atualiza título
            pageTitle.textContent = titles[section];
            
            // Fecha menu mobile
            document.querySelector('.sidebar').classList.remove('active');
        });
    });
}

// Configura modal
function setupModal() {
    const modal = document.getElementById('cattleModal');
    const closeBtn = document.getElementById('modalClose');
    
    closeBtn.addEventListener('click', () => {
        modal.classList.remove('active');
    });
    
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.classList.remove('active');
        }
    });
    
    // Fecha com ESC
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && modal.classList.contains('active')) {
            modal.classList.remove('active');
        }
    });
}

// Abre modal com detalhes do boi
function openCattleModal(cattleId) {
    const cattle = MOCK_CATTLE.find(c => c.id === cattleId);
    if (!cattle) return;
    
    const modal = document.getElementById('cattleModal');
    const content = document.getElementById('modalContent');
    
    const changeClass = cattle.weightChange >= 0 ? 'positive' : 'negative';
    const changeSign = cattle.weightChange >= 0 ? '+' : '';
    
    content.innerHTML = `
        <div class="cattle-detail-header">
            <div>
                <div class="cattle-detail-id">${cattle.name} - ${cattle.id}</div>
                <span class="cattle-status ${cattle.status}">${getStatusLabel(cattle.status)}</span>
                ${cattle.statusReason ? `<p style="color: #666; font-size: 0.9rem; margin-top: 5px;">${cattle.statusReason}</p>` : ''}
            </div>
            <div class="cattle-detail-weight">
                <div class="detail-weight-value">${cattle.weight}kg</div>
                <div class="weight-change ${changeClass}">${changeSign}${cattle.weightChange}kg na última semana</div>
            </div>
        </div>
        
        <div class="photos-section">
            <h4>📷 Últimas Fotos Capturadas (para cálculo do peso)</h4>
            <div class="photos-grid">
                ${cattle.photos.map(photo => `
                    <div class="photo-item">
                        <img src="${photo.url}" alt="${photo.camera}" loading="lazy">
                        <div class="photo-label">${photo.camera}<br>${photo.timestamp}</div>
                    </div>
                `).join('')}
            </div>
        </div>
        
        <div class="info-section">
            <h4>📊 Informações do Animal</h4>
            <div class="info-grid">
                <div class="info-item">
                    <div class="info-value">${cattle.breed}</div>
                    <div class="info-label">Raça</div>
                </div>
                <div class="info-item">
                    <div class="info-value">${cattle.age}</div>
                    <div class="info-label">Idade</div>
                </div>
                <div class="info-item">
                    <div class="info-value">${cattle.cochoVisits}</div>
                    <div class="info-label">Visitas Hoje</div>
                </div>
                <div class="info-item">
                    <div class="info-value">${cattle.avgDailyVisits}</div>
                    <div class="info-label">Média Diária</div>
                </div>
                <div class="info-item">
                    <div class="info-value">${cattle.lastVisit}</div>
                    <div class="info-label">Última Visita</div>
                </div>
                <div class="info-item">
                    <div class="info-value">${cattle.lastWeighing}</div>
                    <div class="info-label">Última Pesagem</div>
                </div>
            </div>
        </div>
        
        <div class="weight-history">
            <h4>📈 Histórico de Peso</h4>
            <div class="history-list">
                ${cattle.weightHistory.map((h, i) => {
                    let change = '';
                    if (i < cattle.weightHistory.length - 1) {
                        const diff = h.weight - cattle.weightHistory[i + 1].weight;
                        const sign = diff >= 0 ? '+' : '';
                        const cls = diff >= 0 ? 'positive' : 'negative';
                        change = `<span class="history-change ${cls}">${sign}${diff}kg</span>`;
                    }
                    return `
                        <div class="history-item">
                            <span class="history-date">${formatDate(h.date)}</span>
                            <span class="history-weight">${h.weight}kg</span>
                            ${change}
                        </div>
                    `;
                }).join('')}
            </div>
        </div>
    `;
    
    modal.classList.add('active');
}

// Formata data
function formatDate(dateStr) {
    const date = new Date(dateStr);
    return date.toLocaleDateString('pt-BR');
}

// Configura filtros
function setupFilters() {
    const searchInput = document.getElementById('searchCattle');
    const weightFilter = document.getElementById('filterWeight');
    const healthFilter = document.getElementById('filterHealth');
    
    const applyFilters = () => {
        loadCattleGrid({
            search: searchInput?.value || '',
            weight: weightFilter?.value || '',
            health: healthFilter?.value || ''
        });
    };
    
    searchInput?.addEventListener('input', debounce(applyFilters, 300));
    weightFilter?.addEventListener('change', applyFilters);
    healthFilter?.addEventListener('change', applyFilters);
}

// Debounce helper
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Mobile menu toggle
function setupMobileMenu() {
    const menuToggle = document.getElementById('menuToggle');
    const sidebar = document.querySelector('.sidebar');
    
    menuToggle?.addEventListener('click', () => {
        sidebar.classList.toggle('active');
    });
}
