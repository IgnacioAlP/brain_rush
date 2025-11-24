/**
 * Sistema de Notificaciones Personalizado para Brain RUSH
 * Reemplaza alert(), confirm() y Swal.fire() con notificaciones consistentes
 */

class BrainRushNotifications {
    constructor() {
        this.createContainer();
    }

    createContainer() {
        if (document.getElementById('br-notification-container')) return;
        
        const container = document.createElement('div');
        container.id = 'br-notification-container';
        container.className = 'br-notification-container';
        document.body.appendChild(container);
    }

    /**
     * Muestra una notificación simple (reemplaza alert)
     * @param {string} message - Mensaje a mostrar
     * @param {string} type - Tipo: 'success', 'error', 'warning', 'info'
     * @param {number} duration - Duración en ms (0 = permanente)
     */
    show(message, type = 'info', duration = 4000) {
        const notification = this.createNotification(message, type);
        const container = document.getElementById('br-notification-container');
        container.appendChild(notification);

        // Animación de entrada
        setTimeout(() => notification.classList.add('br-show'), 10);

        // Auto-cerrar
        if (duration > 0) {
            setTimeout(() => this.close(notification), duration);
        }

        return notification;
    }

    /**
     * Muestra una confirmación (reemplaza confirm)
     * @param {string} message - Mensaje de confirmación
     * @param {string} title - Título opcional
     * @returns {Promise<boolean>}
     */
    confirm(message, title = '¿Estás seguro?') {
        return new Promise((resolve) => {
            const overlay = document.createElement('div');
            overlay.className = 'br-modal-overlay';
            
            const modal = document.createElement('div');
            modal.className = 'br-modal br-modal-confirm';
            modal.innerHTML = `
                <div class="br-modal-header">
                    <i class="fas fa-question-circle"></i>
                    <h3>${this.escapeHtml(title)}</h3>
                </div>
                <div class="br-modal-body">
                    <p>${this.escapeHtml(message)}</p>
                </div>
                <div class="br-modal-footer">
                    <button class="br-btn br-btn-cancel" data-action="cancel">
                        <i class="fas fa-times"></i> Cancelar
                    </button>
                    <button class="br-btn br-btn-confirm" data-action="confirm">
                        <i class="fas fa-check"></i> Aceptar
                    </button>
                </div>
            `;

            overlay.appendChild(modal);
            document.body.appendChild(overlay);

            // Animación de entrada
            setTimeout(() => {
                overlay.classList.add('br-show');
                modal.classList.add('br-show');
            }, 10);

            // Manejadores de eventos
            const handleClick = (e) => {
                const action = e.target.closest('[data-action]')?.dataset.action;
                if (action) {
                    this.closeModal(overlay, modal);
                    resolve(action === 'confirm');
                }
            };

            modal.addEventListener('click', handleClick);
            overlay.addEventListener('click', (e) => {
                if (e.target === overlay) {
                    this.closeModal(overlay, modal);
                    resolve(false);
                }
            });
        });
    }

    /**
     * Muestra un diálogo de éxito con animación
     * @param {string} title - Título
     * @param {string} message - Mensaje
     */
    success(title, message = '') {
        return this.dialog(title, message, 'success');
    }

    /**
     * Muestra un diálogo de error
     * @param {string} title - Título
     * @param {string} message - Mensaje
     */
    error(title, message = '') {
        return this.dialog(title, message, 'error');
    }

    /**
     * Muestra un diálogo de advertencia
     * @param {string} title - Título
     * @param {string} message - Mensaje
     */
    warning(title, message = '') {
        return this.dialog(title, message, 'warning');
    }

    /**
     * Muestra un diálogo de información
     * @param {string} title - Título
     * @param {string} message - Mensaje
     */
    info(title, message = '') {
        return this.dialog(title, message, 'info');
    }

    /**
     * Muestra un diálogo modal
     * @param {string} title - Título
     * @param {string} message - Mensaje
     * @param {string} type - Tipo: 'success', 'error', 'warning', 'info'
     */
    dialog(title, message, type = 'info') {
        return new Promise((resolve) => {
            const overlay = document.createElement('div');
            overlay.className = 'br-modal-overlay';
            
            const icons = {
                success: 'fa-check-circle',
                error: 'fa-times-circle',
                warning: 'fa-exclamation-triangle',
                info: 'fa-info-circle'
            };

            const modal = document.createElement('div');
            modal.className = `br-modal br-modal-${type}`;
            modal.innerHTML = `
                <div class="br-modal-icon">
                    <i class="fas ${icons[type]}"></i>
                </div>
                <div class="br-modal-header">
                    <h3>${this.escapeHtml(title)}</h3>
                </div>
                ${message ? `<div class="br-modal-body"><p>${this.escapeHtml(message)}</p></div>` : ''}
                <div class="br-modal-footer">
                    <button class="br-btn br-btn-primary" data-action="ok">
                        <i class="fas fa-check"></i> Aceptar
                    </button>
                </div>
            `;

            overlay.appendChild(modal);
            document.body.appendChild(overlay);

            // Animación de entrada
            setTimeout(() => {
                overlay.classList.add('br-show');
                modal.classList.add('br-show');
            }, 10);

            // Manejador de eventos
            const handleClick = () => {
                this.closeModal(overlay, modal);
                resolve(true);
            };

            modal.querySelector('[data-action="ok"]').addEventListener('click', handleClick);
            overlay.addEventListener('click', (e) => {
                if (e.target === overlay) handleClick();
            });
        });
    }

    /**
     * Crea el elemento de notificación
     */
    createNotification(message, type) {
        const notification = document.createElement('div');
        notification.className = `br-notification br-notification-${type}`;
        
        const icons = {
            success: 'fa-check-circle',
            error: 'fa-times-circle',
            warning: 'fa-exclamation-triangle',
            info: 'fa-info-circle'
        };

        notification.innerHTML = `
            <div class="br-notification-icon">
                <i class="fas ${icons[type]}"></i>
            </div>
            <div class="br-notification-content">
                ${this.escapeHtml(message)}
            </div>
            <button class="br-notification-close">
                <i class="fas fa-times"></i>
            </button>
        `;

        notification.querySelector('.br-notification-close').addEventListener('click', () => {
            this.close(notification);
        });

        return notification;
    }

    /**
     * Cierra una notificación
     */
    close(notification) {
        notification.classList.remove('br-show');
        notification.classList.add('br-hide');
        setTimeout(() => notification.remove(), 300);
    }

    /**
     * Cierra un modal
     */
    closeModal(overlay, modal) {
        modal.classList.remove('br-show');
        overlay.classList.remove('br-show');
        setTimeout(() => overlay.remove(), 300);
    }

    /**
     * Escapa HTML para prevenir XSS
     */
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Instancia global
window.BrainNotify = new BrainRushNotifications();

// Atajos globales compatibles con código existente
window.showNotification = (message, type = 'info') => window.BrainNotify.show(message, type);
window.showSuccess = (title, message = '') => window.BrainNotify.success(title, message);
window.showError = (title, message = '') => window.BrainNotify.error(title, message);
window.showWarning = (title, message = '') => window.BrainNotify.warning(title, message);
window.showInfo = (title, message = '') => window.BrainNotify.info(title, message);
window.confirmAction = (message, title = '¿Estás seguro?') => window.BrainNotify.confirm(message, title);

// Reemplazar alert() nativo (opcional, comentado por defecto)
// window.alert = (message) => window.BrainNotify.show(message, 'info');

// Reemplazar confirm() nativo (opcional, comentado por defecto)
// window.confirm = (message) => window.BrainNotify.confirm(message);
