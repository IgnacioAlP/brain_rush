// unirse_validaciones.js
// Validaciones para la página Unirse a Sala

function validarCodigoSala() {
    const input = document.getElementById('codigo_sala');
    if (!input || input.value.trim() === "") {
        mostrarErrorUnirse('Debes ingresar el código de la sala');
        return false;
    }
    ocultarErrorUnirse();
    return true;
}

function mostrarErrorUnirse(mensaje) {
    let errorDiv = document.getElementById('unirse-error');
    if (!errorDiv) {
        errorDiv = document.createElement('div');
        errorDiv.id = 'unirse-error';
        errorDiv.style.color = 'red';
        errorDiv.style.marginTop = '8px';
        const form = document.querySelector('form');
        if (form) form.appendChild(errorDiv);
    }
    errorDiv.textContent = mensaje;
}

function ocultarErrorUnirse() {
    const errorDiv = document.getElementById('unirse-error');
    if (errorDiv) errorDiv.remove();
}

// Ejemplo de uso: en el botón de unirse
// document.getElementById('unirseSalaBtn').onclick = function(e) {
//     if (!validarCodigoSala()) {
//         e.preventDefault();
//     }
// };
