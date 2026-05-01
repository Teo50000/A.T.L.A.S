// Elementos del DOM
const appEl = document.getElementById('app');
const tabs = document.querySelectorAll('.tab');
const themeToggle = document.getElementById('themeToggle');
const aboutBtn = document.getElementById('about');
const privacyBtn = document.getElementById('privacy');
const salirBtn = document.getElementById('salir');
const authTrigger = document.getElementById('authTrigger');
const logoutBtn = document.getElementById('logoutBtn');

// Modales
const aboutModal = document.getElementById('aboutModal');
const privacyModal = document.getElementById('privacyModal');
const exitModal = document.getElementById('exitModal');
const authModal = document.getElementById('authModal');

// Botones de cerrar modales
const aboutClose = document.getElementById('aboutClose');
const privacyClose = document.getElementById('privacyClose');
const exitCancel = document.getElementById('exitCancel');
const exitOk = document.getElementById('exitOk');
const authCloseBtn = document.getElementById('authCloseBtn');
const loginTab = document.getElementById('loginTab');
const registerTab = document.getElementById('registerTab');
const loginForm = document.getElementById('loginForm');
const registerForm = document.getElementById('registerForm');
const authFeedback = document.getElementById('authFeedback');

// Estado de la aplicación
let currentSlide = 0;
let isDarkMode = true;
const SESSION_STORAGE_KEY = 'atlas_auth_session';
const API_BASE_URL = 'http://127.0.0.1:5000';
const historyActions = [
  {
    title: 'Creación de documentos',
    description: 'Generó 5 archivos Word con plantillas personalizadas',
    time: 'Hace 2 minutos',
    status: 'completed'
  },
  {
    title: 'Organización de carpetas',
    description: 'Reorganizó 23 archivos por fecha y tipo',
    time: 'Hace 15 minutos',
    status: 'completed'
  },
  {
    title: 'Búsqueda avanzada',
    description: 'Encontró 12 archivos PDF creados la semana pasada',
    time: 'Hace 1 hora',
    status: 'completed'
  },
  {
    title: 'Análisis de duplicados',
    description: 'Identificó y eliminó 8 archivos duplicados',
    time: 'Hace 2 horas',
    status: 'completed'
  },
  {
    title: 'Sincronización en progreso',
    description: 'Procesando 45 archivos de imagen...',
    time: 'Ahora',
    status: 'progress'
  }
];
let historyOutsideClickHandler = null;

function getSession() {
  try {
    const raw = localStorage.getItem(SESSION_STORAGE_KEY);
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
}

function saveSession(sessionData) {
  localStorage.setItem(SESSION_STORAGE_KEY, JSON.stringify(sessionData));
}

function clearSession() {
  localStorage.removeItem(SESSION_STORAGE_KEY);
}

function updateAuthTriggerText() {
  if (!authTrigger) return;
  const session = getSession();
  const displayName = session?.name || session?.username;
  authTrigger.textContent = displayName ? `Hola, ${displayName}` : 'Iniciar sesión';
  logoutBtn?.classList.toggle('hidden', !session?.username);
}

function parseJwtPayload(jwtToken) {
  try {
    const tokenParts = jwtToken.split('.');
    if (tokenParts.length !== 3) return null;
    const base64 = tokenParts[1].replace(/-/g, '+').replace(/_/g, '/');
    const padded = base64 + '='.repeat((4 - (base64.length % 4)) % 4);
    const payload = atob(padded);
    return JSON.parse(payload);
  } catch {
    return null;
  }
}

function setAuthFeedback(message, status = '') {
  if (!authFeedback) return;
  authFeedback.textContent = message;
  authFeedback.classList.remove('error', 'success');
  if (status) authFeedback.classList.add(status);
}

function setAuthMode(mode) {
  const isLoginMode = mode === 'login';
  loginTab?.classList.toggle('is-active', isLoginMode);
  registerTab?.classList.toggle('is-active', !isLoginMode);
  loginForm?.classList.toggle('hidden', !isLoginMode);
  registerForm?.classList.toggle('hidden', isLoginMode);
  setAuthFeedback('');
}

async function registerUserBackend({ name, username, password }) {
  const response = await fetch(`${API_BASE_URL}/regis`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ nombre: name, usuario: username, contraseña: password })
  });
  return response.json();
}

async function loginUserBackend({ username, password }) {
  const response = await fetch(`${API_BASE_URL}/iniSesion`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ usuario: username, contraseña: password })
  });
  return response.json();
}

function initAuth() {
  if (!authTrigger || !authModal) return;

  updateAuthTriggerText();

  authTrigger.addEventListener('click', () => {
    authModal.classList.remove('hidden');
    setAuthMode('login');
  });

  logoutBtn?.addEventListener('click', () => {
    clearSession();
    token = "";
    updateAuthTriggerText();
    setAuthFeedback('');
    loginForm?.reset();
    registerForm?.reset();
  });

  authCloseBtn?.addEventListener('click', () => {
    authModal.classList.add('hidden');
  });

  loginTab?.addEventListener('click', () => setAuthMode('login'));
  registerTab?.addEventListener('click', () => setAuthMode('register'));

  loginForm?.addEventListener('submit', async (event) => {
    event.preventDefault();
    const username = document.getElementById('loginUser')?.value.trim();
    const password = document.getElementById('loginPassword')?.value;

    if (!username || !password) {
      setAuthFeedback('Completá usuario y contraseña.', 'error');
      return;
    }

    try {
      const data = await loginUserBackend({ username, password });
      const rawMessage = data?.mensaje;
      const backendToken = typeof rawMessage === 'string' ? rawMessage : '';

      if (!backendToken || backendToken.includes('incorrecta') || backendToken.includes('no encontrado') || backendToken.includes('requeridos')) {
        setAuthFeedback(rawMessage || 'No se pudo iniciar sesión.', 'error');
        return;
      }

      token = backendToken;
      const payload = parseJwtPayload(backendToken);
      const name = payload?.name || username;
      saveSession({
        name,
        username,
        token: backendToken,
        loggedAt: new Date().toISOString()
      });
      updateAuthTriggerText();
      setAuthFeedback('Inicio de sesión exitoso.', 'success');
      loginForm.reset();
      setTimeout(() => authModal.classList.add('hidden'), 700);
    } catch {
      setAuthFeedback('Error al conectar con el backend.', 'error');
    }
  });

  registerForm?.addEventListener('submit', async (event) => {
    event.preventDefault();
    const name = document.getElementById('registerName')?.value.trim();
    const username = document.getElementById('registerUser')?.value.trim();
    const password = document.getElementById('registerPassword')?.value;

    if (!name || !username || !password) {
      setAuthFeedback('Completá nombre, usuario y contraseña.', 'error');
      return;
    }

    try {
      const data = await registerUserBackend({ name, username, password });
      const message = data?.mensaje || 'No se pudo crear la cuenta.';
      const success = String(message).toLowerCase().includes('exitosamente');
      setAuthFeedback(message, success ? 'success' : 'error');
      if (success) {
        registerForm.reset();
        setAuthMode('login');
      }
    } catch {
      setAuthFeedback('Error al conectar con el backend.', 'error');
    }
  });
}

// Router simple
const routes = {
  '/': renderHome,
  '/assistant': renderAssistant
};

// Navegación
function navigate(path) {
  window.history.pushState({}, '', path);
  tabs.forEach(t => t.classList.toggle('is-active', t.dataset.route === path));
  routes[path]?.();
}

// Event listeners para navegación
tabs.forEach(btn => btn.addEventListener('click', () => navigate(btn.dataset.route)));

// Cambio de tema
themeToggle.addEventListener('click', () => {
  isDarkMode = !isDarkMode;
  document.body.classList.toggle('light', !isDarkMode);
  
  // Actualizar texto del botón
  const themeText = themeToggle.querySelector('.theme-text');
  themeText.textContent = isDarkMode ? 'Modo claro' : 'Modo oscuro';
});

// Event listeners para modales
aboutBtn.addEventListener('click', () => {
  aboutModal.classList.remove('hidden');
});

privacyBtn.addEventListener('click', () => {
  privacyModal.classList.remove('hidden');
});

salirBtn.addEventListener('click', () => {
  exitModal.classList.remove('hidden');
});

// Cerrar modales
aboutClose.addEventListener('click', () => {
  aboutModal.classList.add('hidden');
});

privacyClose.addEventListener('click', () => {
  privacyModal.classList.add('hidden');
});

exitCancel.addEventListener('click', () => {
  exitModal.classList.add('hidden');
});

exitOk.addEventListener('click', async () => {
  exitModal.classList.add('hidden');
  // Close the application directly without any confirmation dialog
  try {
    if (window.atlas?.confirmExit) {
      await window.atlas.confirmExit();
    }
    window.close();
  } catch (error) {
    console.log('Error closing window:', error);
    window.close();
  }
});

// Handle close button clicks for all modals
[aboutModal, privacyModal, exitModal, authModal].forEach(modal => {
  if (!modal) return;
  const closeBtn = modal.querySelector('.close-btn');
  if (closeBtn) {
    closeBtn.addEventListener('click', () => {
      modal.classList.add('hidden');
    });
  }
});

// Cerrar modales al hacer clic fuera
[aboutModal, privacyModal, exitModal, authModal].forEach(modal => {
  if (!modal) return;
  modal.addEventListener('click', (e) => {
    if (e.target === modal) {
      modal.classList.add('hidden');
    }
  });
});

// Carrusel de información
function initCarousel() {
  const carouselContent = document.querySelector('.carousel-content');
  const dots = document.querySelectorAll('.carousel-dot');
  const prevButton = document.getElementById('carouselPrev');
  const nextButton = document.getElementById('carouselNext');
  
  function updateCarousel() {
    if (carouselContent) {
      carouselContent.style.transform = `translateX(-${currentSlide * 100}%)`;
    }
    
    dots.forEach((dot, index) => {
      dot.classList.toggle('active', index === currentSlide);
    });
  }
  
  function goToSlide(index) {
    currentSlide = index;
    updateCarousel();
  }
  
  function nextSlide() {
    currentSlide = (currentSlide + 1) % 3;
    updateCarousel();
  }
  
  function prevSlide() {
    currentSlide = (currentSlide - 1 + 3) % 3;
    updateCarousel();
  }
  
  // Event listeners para los puntos
  dots.forEach((dot, index) => {
    dot.addEventListener('click', () => goToSlide(index));
  });
  
  // Event listeners para las flechas
  if (prevButton) {
    prevButton.addEventListener('click', prevSlide);
  }
  
  if (nextButton) {
    nextButton.addEventListener('click', nextSlide);
  }
  
  // Auto-avance del carrusel
  setInterval(() => {
    nextSlide();
  }, 15000);
}

// Página de inicio
function renderHome() {
  appEl.innerHTML = `
    <div class="home-page">
      <!-- Hero Section -->
      <section class="hero">
        <div class="hero-content">
          <h1>ATLAS</h1>
          <p>Tu asistente de inteligencia artificial para la gestión inteligente de archivos. Automatiza la creación, organización y búsqueda de archivos con comandos naturales.</p>
          <a href="#" class="cta-button" id="startButton">Comencemos</a>
        </div>
      </section>

      <!-- Información -->
      <section class="info-section">
        <div class="container">
          <div class="carousel">
            <div class="carousel-header">
              <h2 class="carousel-title">Conoce ATLAS</h2>
              <p class="carousel-subtitle">Descubre cómo nuestra IA puede revolucionar tu gestión de archivos</p>
            </div>
            
            <div class="carousel-wrapper">
              <button class="carousel-arrow carousel-arrow-left" id="carouselPrev">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <polyline points="15,18 9,12 15,6"></polyline>
                </svg>
              </button>
              
              <div class="carousel-content">
                <div class="carousel-slide">
                  <h3 class="slide-title">¿Qué es Atlas?</h3>
                  <p class="slide-text">Atlas es una inteligencia artificial diseñada para ayudarte a organizar y encontrar archivos en tu computadora de forma eficiente. A partir de información lo más específica posible (por ejemplo, documentos de Word, archivos PDF o incluso archivos de código como .js, .py, etc.), Atlas puede crear o localizar rápidamente el archivo que necesitás. Cuando creas archivos, podés incluso pedirle que ponga en el archivo determinado texto, siempre y cuando vos le presentes la información necesaria para que cree un archivo o más con ese texto. Incluso se le puede pedir a Atlas varios archivos al mismo tiempo y de diferentes tipos. También se le puede pedir que le ponga un nombre específico a cada uno de los archivos.</p>
                </div>
                
                <div class="carousel-slide">
                  <h3 class="slide-title">¿Cómo funciona?</h3>
                  <p class="slide-text">En lugar de mover el archivo de su ubicación original, Atlas crea una copia, o un nuevo archivo y la pone a tu disposición directamente en el escritorio. De esta manera, el archivo original permanece intacto, evitando romper interacciones con otras carpetas o aplicaciones que dependan de su ubicación original. Es importante tener en cuenta que Atlas solo puede acceder y mostrarte archivos si se le proporciona información lo suficientemente precisa para ubicarlos. En caso de no proporcionar información necesaria se te notificará a través del chat, indicándote qué necesita más detalles para continuar con la búsqueda.</p>
                </div>
                
                <div class="carousel-slide">
                  <h3 class="slide-title">¿Cómo lo uso?</h3>
                  <p class="slide-text">Para que ATLAS ubique los archivos que necesitas tendrás que especificar lo que querés crear a través de la barra de texto, lo más detallado posible. Ej: tipo de archivo, nombre del archivo, qué día lo creó, a qué hora, etc. ATLAS también se puede usar como una forma de automatizar la creación de archivos, como por ejemplo que quieras generar múltiples archivos que ambos tengan escrita la siguiente información* Y luego le proporcionas la información que querés. También puede buscar un conjunto de archivos siempre y cuando tengan una similitud que cumplen todos (Como por ejemplo, "Todos los archivos word creados ayer").</p>
                </div>
              </div>
              
              <button class="carousel-arrow carousel-arrow-right" id="carouselNext">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <polyline points="9,18 15,12 9,6"></polyline>
                </svg>
              </button>
            </div>
            
            <div class="carousel-nav">
              <button class="carousel-dot active"></button>
              <button class="carousel-dot"></button>
              <button class="carousel-dot"></button>
            </div>
          </div>
        </div>
      </section>

      <!-- Estadísticas -->
      <section class="stats-section">
        <div class="container">
          <div class="stats-grid">
            <div class="stat-card">
              <div class="stat-icon">⏱️</div>
              <div class="stat-value">1.5</div>
              <div class="stat-label">Horas ahorradas</div>
            </div>
            <div class="stat-card">
              <div class="stat-icon">📁</div>
              <div class="stat-value">127</div>
              <div class="stat-label">Archivos procesados</div>
            </div>
            <div class="stat-card">
              <div class="stat-icon">🎯</div>
              <div class="stat-value">98%</div>
              <div class="stat-label">Precisión</div>
            </div>
          </div>
        </div>
      </section>
    </div>
  `;

  // Inicializar carrusel
  initCarousel();

  // Botón "Comencemos"
  const startButton = document.getElementById('startButton');
  startButton.addEventListener('click', (e) => {
    e.preventDefault();
    navigate('/assistant');
  });
}

function buildHistoryMarkup() {
  return historyActions.map(action => {
    const initials = action.title
      .split(' ')
      .filter(Boolean)
      .slice(0, 2)
      .map(word => word[0])
      .join('')
      .toUpperCase();

    return `
      <div class="history-item">
        <div class="history-icon">${initials}</div>
        <div class="history-content">
          <div class="history-title-item">${action.title}</div>
          <div class="history-description">${action.description}</div>
          <div class="history-time">${action.time}</div>
        </div>
        <div class="history-status ${action.status}">
          ${action.status === 'completed' ? 'Completado' : 'En progreso'}
        </div>
      </div>
    `;
  }).join('');
}

function initHistoryPanel() {
  const toggle = document.getElementById('historyToggle');
  const panel = document.getElementById('historyPanel');
  const closeBtn = document.getElementById('historyClose');
  const list = document.getElementById('historyPanelList');

  if (!toggle || !panel || !list) {
    if (historyOutsideClickHandler) {
      document.removeEventListener('click', historyOutsideClickHandler);
      historyOutsideClickHandler = null;
    }
    return;
  }

  list.innerHTML = buildHistoryMarkup();

  const setVisible = (isVisible) => {
    panel.classList.toggle('is-visible', isVisible);
    panel.setAttribute('aria-hidden', String(!isVisible));
    toggle.setAttribute('aria-expanded', String(isVisible));
  };

  toggle.addEventListener('click', (event) => {
    event.stopPropagation();
    setVisible(!panel.classList.contains('is-visible'));
  });

  panel.addEventListener('click', (event) => {
    event.stopPropagation();
  });

  closeBtn?.addEventListener('click', () => setVisible(false));

  if (historyOutsideClickHandler) {
    document.removeEventListener('click', historyOutsideClickHandler);
  }

  historyOutsideClickHandler = (event) => {
    if (!document.body.contains(panel)) {
      document.removeEventListener('click', historyOutsideClickHandler);
      historyOutsideClickHandler = null;
      return;
    }

    if (
      panel.classList.contains('is-visible') &&
      event.target instanceof Node &&
      !panel.contains(event.target) &&
      !toggle.contains(event.target)
    ) {
      setVisible(false);
    }
  };

  document.addEventListener('click', historyOutsideClickHandler);
}

// Página del asistente
function renderAssistant() {
  appEl.innerHTML = `
    <div class="chat-page">
      <div class="chat-header">
        <div class="chat-avatar">A</div>
        <div class="chat-info">
          <h3>ATLAS</h3>
          <p>Asistente de Archivos IA</p>
        </div>
        <div class="chat-status">
          <button class="history-toggle" id="historyToggle" aria-expanded="false" title="Abrir historial de acciones">
            Historial
          </button>
          <div class="status-dot"></div>
          <span>En línea</span>
        </div>
      </div>
      
      <div class="chat-body" id="chatBody">
        <div class="message ai">
          <div class="message-text">¡Hola! Soy ATLAS. ¿En qué puedo ayudarte hoy?</div>
        </div>
      </div>
      
      <div class="chat-input">
        <input type="text" id="chatInput" placeholder="Escribe tu mensaje a ATLAS..." />
        <button class="send-button" id="sendButton">Enviar</button>
      </div>
      <section class="history-panel" id="historyPanel" aria-hidden="true">
        <div class="history-panel-header">
          <h4>Historial de acciones</h4>
          <button class="history-close" id="historyClose" aria-label="Cerrar historial">×</button>
        </div>
        <div class="history-panel-body">
          <div class="history-list" id="historyPanelList"></div>
        </div>
      </section>
    </div>
  `;

  // Funcionalidad del chat
  initChat();
  initHistoryPanel();
}
let token = ""
// Inicializar chat
async function initChat() {
  const chatBody = document.getElementById('chatBody');
  const chatInput = document.getElementById('chatInput');
  const sendButton = document.getElementById('sendButton');
  
  if(token != ""){
  const res = await fetch("http://127.0.0.1:5000/mensajeViejo", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      "Authorization": token
    },
  });
  const dataRes = await res.json();
  const data = dataRes.ok || [];
  for(let i = 0; i<data.length; i++){
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${data[i].isUser ? 'user' : 'ai'}`;
    
    const messageText = document.createElement('div');
    messageText.className = 'message-text';
    messageText.textContent = data[i].texto; 

    messageDiv.appendChild(messageText);
    chatBody.appendChild(messageDiv);
    chatBody.scrollTop = chatBody.scrollHeight;
  }
  }
  


  async function addMessage(text, isUser = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user' : 'ai'}`;
    
    const messageText = document.createElement('div');
    messageText.className = 'message-text';
    messageText.textContent = text; 

    messageDiv.appendChild(messageText);
    chatBody.appendChild(messageDiv);
    chatBody.scrollTop = chatBody.scrollHeight;
    if(token != ""){
    const res = await fetch("http://127.0.0.1:5000/mensajeNuevo", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": token
      },
      body: JSON.stringify({ text, isUser })
    });
  }
    
  }

  function sendMessage() {
    const text = chatInput.value.trim();
    if (!text) return;

    // Agregar mensaje del usuario
    addMessage(text, true);
    chatInput.value = '';

    // Simular respuesta de la IA
    setTimeout(async() => {
      const papa = await enviar(text)
      addMessage(papa);
    }, 1000 + Math.random() * 2000);
  }

  // Event listeners
  sendButton.addEventListener('click', sendMessage);
  chatInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
      sendMessage();
    }
  });

  // Focus en el input
  chatInput.focus();
}

// Manejar navegación del navegador
window.onpopstate = () => {
  const path = window.location.pathname;
  routes[path]?.();
};


async function enviar(prompt) {
  const nombre = prompt
  
  const res = await fetch("http://127.0.0.1:5000/prompt", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...(token ? { "Authorization": token } : {})
    },
    body: JSON.stringify({ nombre })
  });
  
  const data = await res.json();
  console.log(data.mensaje)
  return data.mensaje
}


// Inicializar aplicación
function init() {
  // Aplicar tema inicial
  document.body.classList.toggle('light', !isDarkMode);
  
  // Inicializar texto del botón de tema
  const themeText = themeToggle.querySelector('.theme-text');
  themeText.textContent = isDarkMode ? 'Modo claro' : 'Modo oscuro';
  
  // Navegar a la ruta inicial
  const initialPath = window.location.pathname in routes ? window.location.pathname : '/';
  navigate(initialPath);
  token = getSession()?.token || "";
  initAuth();
}

// Inicializar cuando el DOM esté listo
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init);
} else {
  init();
}
// Espera a que el video termine y muestra el contenido principal
window.addEventListener("DOMContentLoaded", () => {
  const splash = document.querySelector(".video-splash");
  const main = document.getElementById("main-content");
  const video = splash.querySelector("video");

  video.addEventListener("ended", () => {
    splash.classList.add("fade-out");
    setTimeout(() => {
      splash.remove();
      main.style.display = "block";
    }, 1000); // 1 segundo para la animación
  });
});