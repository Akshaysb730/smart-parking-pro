// Smart Parking Pro - Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide flash messages after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Set minimum datetime for booking inputs
    const datetimeInputs = document.querySelectorAll('input[type="datetime-local"]');
    datetimeInputs.forEach(function(input) {
        const now = new Date();
        now.setMinutes(now.getMinutes() - now.getTimezoneOffset());
        input.min = now.toISOString().slice(0, 16);
    });
});

// Format currency
function formatCurrency(amount) {
    return '₹' + parseFloat(amount).toFixed(2);
}

// Format date
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-IN', {
        day: '2-digit',
        month: 'short',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// AJAX helper
function ajaxRequest(url, method, data, callback) {
    const xhr = new XMLHttpRequest();
    xhr.open(method, url, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            const response = JSON.parse(xhr.responseText);
            callback(response, xhr.status);
        }
    };
    xhr.send(JSON.stringify(data));
}

// Show loading spinner
function showLoading(element) {
    element.innerHTML = '<div class="text-center py-4"><div class="spinner-border text-primary" role="status"></div></div>';
}

// Parking slot visualization
function renderParkingMap(containerId, slots) {
    const container = document.getElementById(containerId);
    if (!container) return;
    
    let html = '<div class="parking-map">';
    slots.forEach(function(slot) {
        const statusClass = slot.is_occupied ? 'occupied' : slot.is_reserved ? 'reserved' : 'available';
        html += `
            <div class="parking-slot ${statusClass}" data-slot-id="${slot.id}">
                <span class="slot-number">${slot.number}</span>
                <span class="slot-type">${slot.type}</span>
            </div>
        `;
    });
    html += '</div>';
    container.innerHTML = html;
}
