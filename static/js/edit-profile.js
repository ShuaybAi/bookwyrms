// Edit Profile JavaScript functionality

// Image preview functionality
document.addEventListener('DOMContentLoaded', function() {
    const imageInput = document.querySelector('input[type="file"][accept="image/*"]');
    const imagePreview = document.getElementById('image-preview');
    const previewImg = document.getElementById('preview-img');
    const currentImageContainer = document.getElementById('current-image')?.parentElement;
    
    if (imageInput) {
        imageInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                // Validate file size (5MB)
                if (file.size > 5 * 1024 * 1024) {
                    alert('File size must be less than 5MB');
                    e.target.value = '';
                    return;
                }
                
                // Validate file type
                if (!file.type.startsWith('image/')) {
                    alert('Please select a valid image file');
                    e.target.value = '';
                    return;
                }
                
                const reader = new FileReader();
                reader.onload = function(e) {
                    previewImg.src = e.target.result;
                    imagePreview.classList.remove('d-none');
                    if (currentImageContainer) {
                        currentImageContainer.style.opacity = '0.5';
                    }
                };
                reader.readAsDataURL(file);
            }
        });
    }
});

function clearPreview() {
    const imageInput = document.querySelector('input[type="file"][accept="image/*"]');
    const imagePreview = document.getElementById('image-preview');
    const currentImageContainer = document.getElementById('current-image')?.parentElement;
    
    if (imageInput) {
        imageInput.value = '';
    }
    if (imagePreview) {
        imagePreview.classList.add('d-none');
    }
    if (currentImageContainer) {
        currentImageContainer.style.opacity = '1';
    }
}

function removeProfileImage() {
    if (confirm('Are you sure you want to remove your profile picture?')) {
        const removeForm = document.getElementById('remove-image-form');
        if (removeForm) {
            removeForm.submit();
        }
    }
}

// Form validation
(function() {
    'use strict';
    window.addEventListener('load', function() {
        const forms = document.getElementsByClassName('needs-validation');
        Array.prototype.forEach.call(forms, function(form) {
            form.addEventListener('submit', function(event) {
                if (form.checkValidity() === false) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                form.classList.add('was-validated');
            }, false);
        });
    }, false);
})();