// Elementos del DOM
const appEl = document.getElementById('app');
const tabs = document.querySelectorAll('.tab');
const themeToggle = document.getElementById('themeToggle');
const aboutBtn = document.getElementById('about');
const privacyBtn = document.getElementById('privacy');
const salirBtn = document.getElementById('salir');

// Modales
const aboutModal = document.getElementById('aboutModal');
const privacyModal = document.getElementById('privacyModal');
const exitModal = document.getElementById('exitModal');

// Botones de cerrar modales
const aboutClose = document.getElementById('aboutClose');
const privacyClose = document.getElementById('privacyClose');
const exitCancel = document.getElementById('exitCancel');
const exitOk = document.getElementById('exitOk');

// Estado de la aplicación
let currentSlide = 0;
let isDarkMode = true;

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
[aboutModal, privacyModal, exitModal].forEach(modal => {
  const closeBtn = modal.querySelector('.close-btn');
  if (closeBtn) {
    closeBtn.addEventListener('click', () => {
      modal.classList.add('hidden');
    });
  }
});

// Cerrar modales al hacer clic fuera
[aboutModal, privacyModal, exitModal].forEach(modal => {
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
                  <div class="slide-icon">🤖</div>
                  <h3 class="slide-title">¿Qué es Atlas?</h3>
                  <p class="slide-text">Atlas es una inteligencia artificial diseñada para ayudarte a organizar y encontrar archivos en tu computadora de forma eficiente. A partir de información lo más específica posible (por ejemplo, documentos de Word, archivos PDF o incluso archivos de código como .js, .py, etc.), Atlas puede crear o localizar rápidamente el archivo que necesitás. Cuando creas archivos, podés incluso pedirle que ponga en el archivo determinado texto, siempre y cuando vos le presentes la información necesaria para que cree un archivo o más con ese texto. Incluso se le puede pedir a Atlas varios archivos al mismo tiempo y de diferentes tipos. También se le puede pedir que le ponga un nombre específico a cada uno de los archivos.</p>
                </div>
                
                <div class="carousel-slide">
                  <div class="slide-icon">⚙️</div>
                  <h3 class="slide-title">¿Cómo funciona?</h3>
                  <p class="slide-text">En lugar de mover el archivo de su ubicación original, Atlas crea una copia, o un nuevo archivo y la pone a tu disposición directamente en el escritorio. De esta manera, el archivo original permanece intacto, evitando romper interacciones con otras carpetas o aplicaciones que dependan de su ubicación original. Es importante tener en cuenta que Atlas solo puede acceder y mostrarte archivos si se le proporciona información lo suficientemente precisa para ubicarlos. En caso de no proporcionar información necesaria se te notificará a través del chat, indicándote qué necesita más detalles para continuar con la búsqueda.</p>
                </div>
                
                <div class="carousel-slide">
                  <div class="slide-icon">💡</div>
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

      <!-- Historial -->
      <section class="history-section">
        <div class="container">
          <h2 class="history-title">Historial de Acciones</h2>
          <div class="history-list" id="historyList">
            <!-- Se llenará dinámicamente -->
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

  // Generar historial de acciones
  generateHistory();
}

// Generar historial de acciones
function generateHistory() {
  const historyList = document.getElementById('historyList');
  if (!historyList) return;

  const actions = [
    {
      icon: '📄',
      title: 'Creación de documentos',
      description: 'Generó 5 archivos Word con plantillas personalizadas',
      time: 'Hace 2 minutos',
      status: 'completed'
    },
    {
      icon: '🗂️',
      title: 'Organización de carpetas',
      description: 'Reorganizó 23 archivos por fecha y tipo',
      time: 'Hace 15 minutos',
      status: 'completed'
    },
    {
      icon: '🔍',
      title: 'Búsqueda avanzada',
      description: 'Encontró 12 archivos PDF creados la semana pasada',
      time: 'Hace 1 hora',
      status: 'completed'
    },
    {
      icon: '📊',
      title: 'Análisis de duplicados',
      description: 'Identificó y eliminó 8 archivos duplicados',
      time: 'Hace 2 horas',
      status: 'completed'
    },
    {
      icon: '🔄',
      title: 'Sincronización en progreso',
      description: 'Procesando 45 archivos de imagen...',
      time: 'Ahora',
      status: 'progress'
    }
  ];

  historyList.innerHTML = actions.map(action => `
    <div class="history-item">
      <div class="history-icon">${action.icon}</div>
      <div class="history-content">
        <div class="history-title-item">${action.title}</div>
        <div class="history-description">${action.description}</div>
        <div class="history-time">${action.time}</div>
      </div>
      <div class="history-status ${action.status}">
        ${action.status === 'completed' ? 'Completado' : 'En progreso'}
      </div>
    </div>
  `).join('');
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
    </div>
  `;

  // Funcionalidad del chat
  initChat();
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
  const data = await res.json();
  data = data.ok
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
      "Content-Type": "application/json"
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