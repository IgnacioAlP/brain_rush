// registro.js
// Lógica de registro para Brain Rush

let step = 1;
let selectedOption = null;
let userData = {};

function createStepIndicator() {
  return `
    <div class="step-indicator">
      <div class="step-dot ${step >= 1 ? 'active' : ''}"></div>
      <div class="step-dot ${step >= 2 ? 'active' : ''}"></div>
      <div class="step-dot ${step >= 3 ? 'active' : ''}"></div>
      <div class="step-dot ${step >= 4 ? 'active' : ''}"></div>
    </div>
  `;
}

function showError(message, inputId = null) {
  const errorDiv = document.createElement('div');
  errorDiv.className = 'error-message';
  errorDiv.style.display = 'block';
  errorDiv.textContent = message;
  
  if (inputId) {
    const input = document.getElementById(inputId);
    input.parentNode.insertBefore(errorDiv, input.nextSibling);
    input.style.borderColor = '#e74c3c';
  }
}

function clearErrors() {
  document.querySelectorAll('.error-message').forEach(el => el.remove());
  document.querySelectorAll('input, select').forEach(el => {
    el.style.borderColor = '#aaa';
  });
}

function validateEmail(email) {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return re.test(email);
}

function renderStep4() {
  document.getElementById('register-content').innerHTML = `
    ${createStepIndicator()}
    <h2>Brain Rush</h2>
    <div class="subtitle">Registrate con tu email</div>
    <input type="email" placeholder="email@domain.com" id="email" required>
    <button class="btn" onclick="finishRegister()">Continuar</button>
    <hr>
    <div style="margin: 10px 0;">o continúa con</div>
    <button class="google-btn" onclick="alert('Google Auth')">
      <img src="https://upload.wikimedia.org/wikipedia/commons/5/53/Google_%22G%22_Logo.svg" alt="Google">Continuar con google
    </button>
    <div class="terms">
      Al hacer clic en continuar, aceptas nuestros <a href="#">Términos de servicio</a> y <a href="#">Política de privacidad</a>
    </div>
  `;
}

function renderStep3() {
  document.getElementById('register-content').innerHTML = `
    ${createStepIndicator()}
    <h2>Brain Rush</h2>
    <div class="subtitle">Crear nombre de usuario</div>
    <input type="text" placeholder="Nombre de usuario" id="username" required>
    <button class="btn" onclick="validateAndNext()">Continuar</button>
    <div class="terms">
      Al hacer clic en continuar, aceptas nuestros <a href="#">Términos de servicio</a> y <a href="#">Política de privacidad</a>
    </div>
  `;
}

function renderStep2() {
  document.getElementById('register-content').innerHTML = `
    ${createStepIndicator()}
    <h2>Brain Rush</h2>
    <div class="subtitle">Ingresa tu fecha de nacimiento</div>
    <div style="display: flex; gap: 10px;">
      <div style="flex:1;">
        <label>Año</label>
        <select id="year" required>
          <option value="">Seleccionar</option>
          ${Array.from({length: 100}, (_, i) => `<option value="${2025-i}">${2025-i}</option>`).join('')}
        </select>
      </div>
      <div style="flex:1;">
        <label>Mes</label>
        <select id="month" required>
          <option value="">Seleccionar</option>
          ${Array.from({length: 12}, (_, i) => `<option value="${i+1}">${i+1}</option>`).join('')}
        </select>
      </div>
      <div style="flex:1;">
        <label>Día</label>
        <select id="day" required>
          <option value="">Seleccionar</option>
          ${Array.from({length: 31}, (_, i) => `<option value="${i+1}">${i+1}</option>`).join('')}
        </select>
      </div>
    </div>
    <button class="btn" onclick="validateAndNext()">Continuar</button>
    <div class="terms">
      Al hacer clic en continuar, aceptas nuestros <a href="#">Términos de servicio</a> y <a href="#">Política de privacidad</a>
    </div>
  `;
}

function renderStep1() {
  document.getElementById('register-content').innerHTML = `
    ${createStepIndicator()}
    <h2>Brain Rush</h2>
    <div class="subtitle">Describe tu lugar de trabajo</div>
    <div class="icons-row">
      <div class="option" onclick="selectWork('escuela')" id="escuela">
        <img src="https://img.icons8.com/ios/100/school-building.png" alt="Escuela">
        <div>ESCUELA</div>
      </div>
      <div class="option" onclick="selectWork('superior')" id="superior">
        <img src="https://img.icons8.com/ios/100/graduation-cap.png" alt="Educación Superior">
        <div>EDUCACIÓN SUPERIOR</div>
      </div>
      <div class="option" onclick="selectWork('admin')" id="admin">
        <img src="https://img.icons8.com/ios/100/briefcase.png" alt="Administración Escolar">
        <div>ADMINISTRACION ESCOLAR</div>
      </div>
      <div class="option" onclick="selectWork('negocio')" id="negocio">
        <img src="https://img.icons8.com/ios/100/company.png" alt="Negocio">
        <div>NEGOCIO</div>
      </div>
    </div>
    <button class="btn" onclick="validateAndNext()" ${!selectedOption ? 'disabled' : ''}>Continuar</button>
    <div class="terms">
      Al hacer clic en continuar, aceptas nuestros <a href="#">Términos de servicio</a> y <a href="#">Política de privacidad</a>
    </div>
  `;
  highlightSelected();
}

function validateAndNext() {
  clearErrors();
  let isValid = true;

  if (step === 1) {
    if (!selectedOption) {
      showError('Por favor selecciona una opción');
      isValid = false;
    } else {
      userData.workplace = selectedOption;
    }
  } else if (step === 2) {
    const year = document.getElementById('year').value;
    const month = document.getElementById('month').value;
    const day = document.getElementById('day').value;

    if (!year || !month || !day) {
      showError('Por favor completa tu fecha de nacimiento');
      isValid = false;
    } else {
      userData.birthDate = { year, month, day };
    }
  } else if (step === 3) {
    const username = document.getElementById('username').value.trim();
    if (!username) {
      showError('El nombre de usuario es requerido', 'username');
      isValid = false;
    } else if (username.length < 3) {
      showError('El nombre de usuario debe tener al menos 3 caracteres', 'username');
      isValid = false;
    } else {
      userData.username = username;
    }
  }

  if (isValid) {
    nextStep();
  }
}

function nextStep() {
  step++;
  if (step === 2) renderStep2();
  else if (step === 3) renderStep3();
  else if (step === 4) renderStep4();
}

function selectWork(option) {
  selectedOption = option;
  highlightSelected();
  // Habilitar botón
  const btn = document.querySelector('.btn');
  if (btn) {
    btn.disabled = false;
  }
}

function highlightSelected() {
  ['escuela','superior','admin','negocio'].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.classList.remove('selected');
  });
  if (selectedOption) {
    const el = document.getElementById(selectedOption);
    if (el) el.classList.add('selected');
  }
}

function finishRegister() {
  clearErrors();
  const email = document.getElementById('email').value.trim();
  
  if (!email) {
    showError('El email es requerido', 'email');
    return;
  }
  
  if (!validateEmail(email)) {
    showError('Por favor ingresa un email válido', 'email');
    return;
  }

  userData.email = email;
  
  // Aquí enviarías los datos al servidor
  console.log('Datos del usuario:', userData);
  
  // Redirigir o mostrar mensaje de éxito
  alert('¡Registro completado exitosamente!');
  window.location.href = window.location.origin + "/maestra"; // Redirigir a la página principal
}

// Inicializa la primera pantalla
renderStep1();
