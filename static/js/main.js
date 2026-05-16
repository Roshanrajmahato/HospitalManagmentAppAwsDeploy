// static/js/main.js
// Main JavaScript Entry Point

console.log('MediCare HMS - Main Script Loaded');

// ============================================
// DOCUMENT READY
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM Content Loaded');
    
    // Initialize components
    initializeTooltips();
    initializePopovers();
    initializeFormHandlers();
    initializeAutoCloseAlerts();
    initializeLoadingStates();
});

// ============================================
// UTILITY FUNCTIONS
// ============================================

/**
 * Get CSRF Token from cookie
 */
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

/**
 * Show notification/toast
 */
function showNotification(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show m-3`;
    alertDiv.role = 'alert';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const mainContent = document.querySelector('.main-content');
    if (mainContent) {
        mainContent.insertBefore(alertDiv, mainContent.firstChild);
    }
    
    // Auto close after 5 seconds
    setTimeout(() => {
        alertDiv.style.animation = 'slideOutRight 0.3s ease-in';
        setTimeout(() => alertDiv.remove(), 300);
    }, 5000);
}

// ============================================
// BOOTSTRAP COMPONENTS INITIALIZATION
// ============================================

/**
 * Initialize Bootstrap Tooltips
 */
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Initialize Bootstrap Popovers
 */
function initializePopovers() {
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
}

// ============================================
// FORM HANDLING
// ============================================

/**
 * Initialize Form Handlers
 */
function initializeFormHandlers() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            // Add loading state to submit button
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Processing...';
                
                // Re-enable after submission
                setTimeout(() => {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = originalText;
                }, 5000);
            }
        });
    });
}

/**
 * Auto Close Alerts after 5 seconds
 */
function initializeAutoCloseAlerts() {
    const alerts = document.querySelectorAll('.alert');
    
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
}

/**
 * Handle Loading States
 */
function initializeLoadingStates() {
    const buttons = document.querySelectorAll('[data-loading-text]');
    
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            const loadingText = this.getAttribute('data-loading-text');
            const originalText = this.innerHTML;
            
            this.disabled = true;
            this.innerHTML = loadingText;
            
            setTimeout(() => {
                this.disabled = false;
                this.innerHTML = originalText;
            }, 3000);
        });
    });
}

// ============================================
// ANIMATION UTILITIES
// ============================================

/**
 * Add animation to element
 */
function addAnimation(element, animationName) {
    element.classList.add(animationName);
    element.addEventListener('animationend', () => {
        element.classList.remove(animationName);
    }, { once: true });
}

/**
 * Fade in element
 */
function fadeIn(element, duration = 300) {
    element.style.animation = `fadeIn ${duration}ms ease-out`;
}

/**
 * Fade out element
 */
function fadeOut(element, duration = 300, callback) {
    element.style.animation = `fadeOut ${duration}ms ease-out`;
    setTimeout(() => {
        element.style.display = 'none';
        if (callback) callback();
    }, duration);
}

// ============================================
// TABLE UTILITIES
// ============================================

/**
 * Make table rows clickable
 */
function makeTableRowsClickable(tableSelector, urlAttribute = 'data-url') {
    const rows = document.querySelectorAll(`${tableSelector} tbody tr[${urlAttribute}]`);
    
    rows.forEach(row => {
        row.style.cursor = 'pointer';
        row.addEventListener('click', function() {
            const url = this.getAttribute(urlAttribute);
            if (url) {
                window.location.href = url;
            }
        });
    });
}

/**
 * Filter table by search input
 */
function filterTable(searchInputSelector, tableBodySelector) {
    const searchInput = document.querySelector(searchInputSelector);
    const tableBody = document.querySelector(tableBodySelector);
    
    if (!searchInput || !tableBody) return;
    
    searchInput.addEventListener('keyup', function() {
        const searchTerm = this.value.toLowerCase();
        const rows = tableBody.querySelectorAll('tr');
        
        rows.forEach(row => {
            const text = row.textContent.toLowerCase();
            row.style.display = text.includes(searchTerm) ? '' : 'none';
        });
    });
}

// ============================================
// EXPORT FUNCTIONS
// ============================================

// Export for use in other scripts
if (typeof window !== 'undefined') {
    window.appUtils = {
        getCookie,
        showNotification,
        addAnimation,
        fadeIn,
        fadeOut,
        makeTableRowsClickable,
        filterTable
    };
}
