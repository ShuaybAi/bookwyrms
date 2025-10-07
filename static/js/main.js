// Main JavaScript functionality for BookWyrms

// Auto-hide Django messages after 4 seconds
document.addEventListener('DOMContentLoaded', function() {
    // Find all alert messages
    const alerts = document.querySelectorAll('.alert-success, .alert-danger');
    
    alerts.forEach(function(alert) {
        // Auto-hide after 4 seconds (4000 milliseconds)
        setTimeout(function() {
            // Use Bootstrap's fade out animation
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 4000);
    });
});