/**
 * FaceBoi - Dados Mockados para MVP
 * Simula dados de bois com RFID, pesos, fotos e passagens pelo cocho
 */

const MOCK_CATTLE = [
    {
        id: "RFID-001-A7B3",
        name: "Sultão",
        weight: 478,
        weightHistory: [
            { date: "2025-12-01", weight: 465 },
            { date: "2025-11-15", weight: 452 },
            { date: "2025-11-01", weight: 438 },
            { date: "2025-10-15", weight: 425 }
        ],
        weightChange: +13,
        lastWeighing: "2025-12-08",
        status: "healthy",
        breed: "Nelore",
        age: "24 meses",
        cochoVisits: 6,
        avgDailyVisits: 5.2,
        lastVisit: "08/12/2025 14:32",
        photos: [
            { camera: "Câmera Frontal", timestamp: "08/12/2025 14:32", url: "../assets/boi1/frente.jpeg" },
            { camera: "Câmera Lateral Esq.", timestamp: "08/12/2025 14:32", url: "../assets/boi1/esquerda.jpeg" },
            { camera: "Câmera Lateral Dir.", timestamp: "08/12/2025 14:32", url: "../assets/boi1/direita.jpeg" },
            { camera: "Câmera Superior", timestamp: "08/12/2025 14:32", url: "../assets/boi1/tras.jpeg" }
        ]
    },
    {
        id: "RFID-002-C4D9",
        name: "Trovão",
        weight: 445,
        weightHistory: [
            { date: "2025-12-01", weight: 438 },
            { date: "2025-11-15", weight: 430 },
            { date: "2025-11-01", weight: 420 },
            { date: "2025-10-15", weight: 408 }
        ],
        weightChange: +7,
        lastWeighing: "2025-12-08",
        status: "healthy",
        breed: "Nelore",
        age: "22 meses",
        cochoVisits: 5,
        avgDailyVisits: 4.8,
        lastVisit: "08/12/2025 13:45",
        photos: [
            { camera: "Câmera Frontal", timestamp: "08/12/2025 13:45", url: "../assets/boi2/frente.jpeg" },
            { camera: "Câmera Lateral Esq.", timestamp: "08/12/2025 13:45", url: "../assets/boi2/esquerda.jpeg" },
            { camera: "Câmera Lateral Dir.", timestamp: "08/12/2025 13:45", url: "../assets/boi2/esquerda.jpeg" },
            { camera: "Câmera Superior", timestamp: "08/12/2025 13:45", url: "../assets/boi2/tras.jpeg" }
        ]
    },
    {
        id: "RFID-003-E2F6",
        name: "Relâmpago",
        weight: 412,
        weightHistory: [
            { date: "2025-12-01", weight: 408 },
            { date: "2025-11-15", weight: 405 },
            { date: "2025-11-01", weight: 398 },
            { date: "2025-10-15", weight: 390 }
        ],
        weightChange: +4,
        lastWeighing: "2025-12-08",
        status: "warning",
        statusReason: "Baixa frequência no cocho - possível problema de saúde",
        breed: "Nelore",
        age: "20 meses",
        cochoVisits: 2,
        avgDailyVisits: 2.1,
        lastVisit: "08/12/2025 09:15",
        photos: [
            { camera: "Câmera Frontal", timestamp: "08/12/2025 09:15", url: "https://images.unsplash.com/photo-1564429238535-0164a85c8dc4?w=400" },
            { camera: "Câmera Lateral Esq.", timestamp: "08/12/2025 09:15", url: "https://images.unsplash.com/photo-1546445317-29f4545e9d53?w=400" },
            { camera: "Câmera Lateral Dir.", timestamp: "08/12/2025 09:15", url: "https://images.unsplash.com/photo-1570042225831-d98fa7577f1e?w=400" },
            { camera: "Câmera Superior", timestamp: "08/12/2025 09:15", url: "https://images.unsplash.com/photo-1527153857715-3908f2bae5e8?w=400" }
        ]
    },
    {
        id: "RFID-004-G8H1",
        name: "Faísca",
        weight: 389,
        weightHistory: [
            { date: "2025-12-01", weight: 385 },
            { date: "2025-11-15", weight: 378 },
            { date: "2025-11-01", weight: 365 },
            { date: "2025-10-15", weight: 352 }
        ],
        weightChange: +4,
        lastWeighing: "2025-12-07",
        status: "healthy",
        breed: "Guzerá",
        age: "18 meses",
        cochoVisits: 7,
        avgDailyVisits: 6.5,
        lastVisit: "08/12/2025 15:20",
        photos: [
            { camera: "Câmera Frontal", timestamp: "08/12/2025 15:20", url: "https://images.unsplash.com/photo-1527153857715-3908f2bae5e8?w=400" },
            { camera: "Câmera Lateral Esq.", timestamp: "08/12/2025 15:20", url: "https://images.unsplash.com/photo-1564429238535-0164a85c8dc4?w=400" },
            { camera: "Câmera Lateral Dir.", timestamp: "08/12/2025 15:20", url: "https://images.unsplash.com/photo-1546445317-29f4545e9d53?w=400" },
            { camera: "Câmera Superior", timestamp: "08/12/2025 15:20", url: "https://images.unsplash.com/photo-1570042225831-d98fa7577f1e?w=400" }
        ]
    },
    {
        id: "RFID-005-I3J7",
        name: "Ventania",
        weight: 356,
        weightHistory: [
            { date: "2025-12-01", weight: 362 },
            { date: "2025-11-15", weight: 368 },
            { date: "2025-11-01", weight: 360 },
            { date: "2025-10-15", weight: 355 }
        ],
        weightChange: -6,
        lastWeighing: "2025-12-08",
        status: "critical",
        statusReason: "Perda de peso detectada - verificar saúde urgente",
        breed: "Nelore",
        age: "19 meses",
        cochoVisits: 1,
        avgDailyVisits: 1.5,
        lastVisit: "08/12/2025 07:40",
        photos: [
            { camera: "Câmera Frontal", timestamp: "08/12/2025 07:40", url: "https://images.unsplash.com/photo-1570042225831-d98fa7577f1e?w=400" },
            { camera: "Câmera Lateral Esq.", timestamp: "08/12/2025 07:40", url: "https://images.unsplash.com/photo-1527153857715-3908f2bae5e8?w=400" },
            { camera: "Câmera Lateral Dir.", timestamp: "08/12/2025 07:40", url: "https://images.unsplash.com/photo-1564429238535-0164a85c8dc4?w=400" },
            { camera: "Câmera Superior", timestamp: "08/12/2025 07:40", url: "https://images.unsplash.com/photo-1546445317-29f4545e9d53?w=400" }
        ]
    },
    {
        id: "RFID-006-K5L2",
        name: "Tornado",
        weight: 495,
        weightHistory: [
            { date: "2025-12-01", weight: 482 },
            { date: "2025-11-15", weight: 468 },
            { date: "2025-11-01", weight: 455 },
            { date: "2025-10-15", weight: 440 }
        ],
        weightChange: +13,
        lastWeighing: "2025-12-08",
        status: "healthy",
        breed: "Nelore",
        age: "26 meses",
        cochoVisits: 6,
        avgDailyVisits: 5.8,
        lastVisit: "08/12/2025 14:10",
        photos: [
            { camera: "Câmera Frontal", timestamp: "08/12/2025 14:10", url: "https://images.unsplash.com/photo-1546445317-29f4545e9d53?w=400" },
            { camera: "Câmera Lateral Esq.", timestamp: "08/12/2025 14:10", url: "https://images.unsplash.com/photo-1570042225831-d98fa7577f1e?w=400" },
            { camera: "Câmera Lateral Dir.", timestamp: "08/12/2025 14:10", url: "https://images.unsplash.com/photo-1527153857715-3908f2bae5e8?w=400" },
            { camera: "Câmera Superior", timestamp: "08/12/2025 14:10", url: "https://images.unsplash.com/photo-1564429238535-0164a85c8dc4?w=400" }
        ]
    },
    {
        id: "RFID-007-M9N4",
        name: "Bravo",
        weight: 428,
        weightHistory: [
            { date: "2025-12-01", weight: 420 },
            { date: "2025-11-15", weight: 410 },
            { date: "2025-11-01", weight: 398 },
            { date: "2025-10-15", weight: 385 }
        ],
        weightChange: +8,
        lastWeighing: "2025-12-07",
        status: "healthy",
        breed: "Tabapuã",
        age: "21 meses",
        cochoVisits: 5,
        avgDailyVisits: 4.9,
        lastVisit: "08/12/2025 12:55",
        photos: [
            { camera: "Câmera Frontal", timestamp: "08/12/2025 12:55", url: "https://images.unsplash.com/photo-1564429238535-0164a85c8dc4?w=400" },
            { camera: "Câmera Lateral Esq.", timestamp: "08/12/2025 12:55", url: "https://images.unsplash.com/photo-1546445317-29f4545e9d53?w=400" },
            { camera: "Câmera Lateral Dir.", timestamp: "08/12/2025 12:55", url: "https://images.unsplash.com/photo-1570042225831-d98fa7577f1e?w=400" },
            { camera: "Câmera Superior", timestamp: "08/12/2025 12:55", url: "https://images.unsplash.com/photo-1527153857715-3908f2bae5e8?w=400" }
        ]
    },
    {
        id: "RFID-008-O6P8",
        name: "Valente",
        weight: 467,
        weightHistory: [
            { date: "2025-12-01", weight: 458 },
            { date: "2025-11-15", weight: 448 },
            { date: "2025-11-01", weight: 435 },
            { date: "2025-10-15", weight: 422 }
        ],
        weightChange: +9,
        lastWeighing: "2025-12-08",
        status: "healthy",
        breed: "Nelore",
        age: "23 meses",
        cochoVisits: 6,
        avgDailyVisits: 5.5,
        lastVisit: "08/12/2025 15:45",
        photos: [
            { camera: "Câmera Frontal", timestamp: "08/12/2025 15:45", url: "https://images.unsplash.com/photo-1527153857715-3908f2bae5e8?w=400" },
            { camera: "Câmera Lateral Esq.", timestamp: "08/12/2025 15:45", url: "https://images.unsplash.com/photo-1564429238535-0164a85c8dc4?w=400" },
            { camera: "Câmera Lateral Dir.", timestamp: "08/12/2025 15:45", url: "https://images.unsplash.com/photo-1546445317-29f4545e9d53?w=400" },
            { camera: "Câmera Superior", timestamp: "08/12/2025 15:45", url: "https://images.unsplash.com/photo-1570042225831-d98fa7577f1e?w=400" }
        ]
    }
];

// Dados de alertas
const MOCK_ALERTS = [
    {
        id: 1,
        type: "critical",
        title: "Perda de Peso Detectada",
        description: "O boi Ventania (RFID-005-I3J7) apresentou perda de 6kg na última semana. Frequência de visitas ao cocho abaixo do normal.",
        cattleId: "RFID-005-I3J7",
        timestamp: "08/12/2025 08:00",
        isRead: false
    },
    {
        id: 2,
        type: "warning",
        title: "Baixa Frequência no Cocho",
        description: "O boi Relâmpago (RFID-003-E2F6) está visitando o cocho com frequência abaixo da média. Média atual: 2.1 visitas/dia (esperado: 5+)",
        cattleId: "RFID-003-E2F6",
        timestamp: "08/12/2025 10:30",
        isRead: false
    }
];

// Atividades recentes (passagens pelo cocho)
const MOCK_RECENT_ACTIVITY = [
    { cattleId: "RFID-008-O6P8", name: "Valente", time: "15:45", weight: 467, cochoVisit: 6 },
    { cattleId: "RFID-004-G8H1", name: "Faísca", time: "15:20", weight: 389, cochoVisit: 7 },
    { cattleId: "RFID-001-A7B3", name: "Sultão", time: "14:32", weight: 478, cochoVisit: 6 },
    { cattleId: "RFID-006-K5L2", name: "Tornado", time: "14:10", weight: 495, cochoVisit: 6 },
    { cattleId: "RFID-002-C4D9", name: "Trovão", time: "13:45", weight: 445, cochoVisit: 5 },
    { cattleId: "RFID-007-M9N4", name: "Bravo", time: "12:55", weight: 428, cochoVisit: 5 },
    { cattleId: "RFID-003-E2F6", name: "Relâmpago", time: "09:15", weight: 412, cochoVisit: 2 },
    { cattleId: "RFID-005-I3J7", name: "Ventania", time: "07:40", weight: 356, cochoVisit: 1 }
];

// Usuário demo
const DEMO_USER = {
    email: "demo@faceboi.com.br",
    password: "demo123",
    name: "João Silva",
    farm: "Fazenda Boa Vista"
};

// Exporta para uso global
window.MOCK_CATTLE = MOCK_CATTLE;
window.MOCK_ALERTS = MOCK_ALERTS;
window.MOCK_RECENT_ACTIVITY = MOCK_RECENT_ACTIVITY;
window.DEMO_USER = DEMO_USER;
