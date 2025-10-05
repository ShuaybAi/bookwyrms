// Main JavaScript functionality for BookWyrms

// Auto-hide Django messages after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    // Find all alert messages
    const alerts = document.querySelectorAll('.alert');
    
    alerts.forEach(function(alert) {
        // Auto-hide after 5 seconds (5000 milliseconds)
        setTimeout(function() {
            // Use Bootstrap's fade out animation
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
});