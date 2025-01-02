// Common JavaScript functions

// Confirm delete operations
function confirmDelete(itemType) {
    // amazonq-ignore-next-line
    return confirm(`Are you sure you want to delete this ${itemType}?`);
}

// Format currency
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

// Initialize tooltips
document.addEventListener('DOMContentLoaded', function() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});

// Handle form submission
document.addEventListener('submit', function(event) {
    const form = event.target;
    if (form.classList.contains('needs-validation')) {
        if (!form.checkValidity()) {
            event.preventDefault();
            event.stopPropagation();
        }
        form.classList.add('was-validated');
    }
});

