// My Account page JavaScript functionality

// Delete account confirmation functionality
document.addEventListener('DOMContentLoaded', function() {
    const confirmationInput = document.getElementById('confirmationText');
    const confirmDeleteBtn = document.getElementById('confirmDeleteBtn');
    const requiredText = 'DELETE MY ACCOUNT';
    
    // Only run if elements exist (in case user is on different page)
    if (confirmationInput && confirmDeleteBtn) {
        // Enable/disable delete button based on input
        confirmationInput.addEventListener('input', function() {
            if (this.value === requiredText) {
                confirmDeleteBtn.disabled = false;
                confirmDeleteBtn.classList.remove('btn-danger');
                confirmDeleteBtn.classList.add('btn-outline-danger');
            } else {
                confirmDeleteBtn.disabled = true;
                confirmDeleteBtn.classList.remove('btn-outline-danger');
                confirmDeleteBtn.classList.add('btn-danger');
            }
        });
        
        // Handle the actual deletion
        confirmDeleteBtn.addEventListener('click', function() {
            if (confirmationInput.value === requiredText) {
                // Add a final confirmation
                if (confirm('FINAL WARNING: This will permanently delete your account and all data. Are you absolutely sure?')) {
                    // Create a form and submit it as POST request
                    const form = document.createElement('form');
                    form.method = 'POST';
                    form.action = '/my-account/delete-account/';

                    // Add CSRF token
                    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;                     
                    const csrfInput = document.createElement('input');
                    csrfInput.type = 'hidden';
                    csrfInput.name = 'csrfmiddlewaretoken';
                    csrfInput.value = csrfToken;
                    form.appendChild(csrfInput);

                    // Submit the form
                    document.body.appendChild(form);
                    form.submit();
                }
            }
        });
        
        // Clear input when modal is closed
        const deleteModal = document.getElementById('deleteAccountModal');
        if (deleteModal) {
            deleteModal.addEventListener('hidden.bs.modal', function() {
                confirmationInput.value = '';
                confirmDeleteBtn.disabled = true;
                confirmDeleteBtn.classList.remove('btn-outline-danger');
                confirmDeleteBtn.classList.add('btn-danger');
            });
        }
    }
});