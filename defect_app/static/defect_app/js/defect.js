let webcamStream = null;

// Get CSRF token from cookie
function getCSRFToken() {
    const name = 'csrftoken';
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

// Show loading state
function showLoading() {
    const submitBtn = document.querySelector('.submit-btn');
    const btnText = submitBtn.querySelector('.btn-text');
    const loader = submitBtn.querySelector('.loader');
    
    btnText.style.opacity = '0';
    loader.style.display = 'block';
    submitBtn.disabled = true;
}

// Hide loading state
function hideLoading() {
    const submitBtn = document.querySelector('.submit-btn');
    const btnText = submitBtn.querySelector('.btn-text');
    const loader = submitBtn.querySelector('.loader');
    
    btnText.style.opacity = '1';
    loader.style.display = 'none';
    submitBtn.disabled = false;
}

// Webcam handling
document.getElementById('webcamButton').addEventListener('click', async () => {
    const video = document.getElementById('webcam');
    const preview = document.getElementById('preview');

    try {
        webcamStream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = webcamStream;
        video.style.display = 'block';
        preview.style.display = 'none';
        video.play();
    } catch (err) {
        showError('Error accessing webcam: ' + err.message);
    }
});

// File upload handling
document.getElementById('image').addEventListener('change', (e) => {
    const preview = document.getElementById('preview');
    const file = e.target.files[0];
    
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            preview.src = e.target.result;
            preview.style.display = 'block';
            document.getElementById('webcam').style.display = 'none';
            if (webcamStream) {
                webcamStream.getTracks().forEach(track => track.stop());
            }
        }
        reader.readAsDataURL(file);
    }
});

// Form submission
document.getElementById('inspectionForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    console.log('Form submitted');
    showLoading();
    
    const formData = new FormData();
    formData.append('name', document.getElementById('name').value);
    formData.append('serial', document.getElementById('serial').value);
    formData.append('model', document.getElementById('model').value);

    const video = document.getElementById('webcam');
    const canvas = document.getElementById('canvas');
    const fileInput = document.getElementById('image');

    try {
        if (video.style.display === 'block') {
            console.log('Using webcam image');
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            canvas.getContext('2d').drawImage(video, 0, 0);
            
            canvas.toBlob((blob) => {
                formData.append('image', blob, 'webcam.jpg');
                submitInspection(formData);
            }, 'image/jpeg');
        } else if (fileInput.files[0]) {
            console.log('Using uploaded file');
            formData.append('image', fileInput.files[0]);
            submitInspection(formData);
        } else {
            throw new Error('Please provide an image for inspection');
        }
    } catch (error) {
        console.error('Error:', error);
        hideLoading();
        showError(error.message);
    }
});

// Submit inspection data
async function submitInspection(formData) {
    try {
        console.log('Submitting inspection...');
        const response = await fetch('/analyze_defect/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCSRFToken(),
            },
            body: formData
        });
        
        console.log('Response received');
        const data = await response.json();
        console.log('Response data:', data);
        
        if (data.success) {
            showResults(data);
            if (webcamStream) {
                webcamStream.getTracks().forEach(track => track.stop());
            }
        } else {
            throw new Error(data.error);
        }
    } catch (error) {
        console.error('Submission error:', error);
        showError('Error during inspection: ' + error.message);
    } finally {
        hideLoading();
    }
}

// Show results
function showResults(data) {
    const resultContainer = document.querySelector('.result-container');
    resultContainer.style.display = 'block';
    
    const resultImage = document.getElementById('resultImage');
    resultImage.src = data.image_url;
    
    const resultsDiv = document.getElementById('defectResults');
    resultsDiv.innerHTML = '<h3>Detected Defects:</h3>';
    
    if (Object.keys(data.results).length === 0) {
        resultsDiv.innerHTML += '<p class="no-defects">No defects detected</p>';
    } else {
        for (const [defectType, count] of Object.entries(data.results)) {
            resultsDiv.innerHTML += `
                <p class="defect-item">
                    <span class="defect-type">${defectType}</span>
                    <span class="defect-count">${count}</span>
                </p>`;
        }
    }
}

// Show error message
function showError(message) {
    const resultsDiv = document.getElementById('defectResults');
    resultsDiv.innerHTML = `<div class="error">${message}</div>`;
    document.querySelector('.result-container').style.display = 'block';
}

// Add these modal functions
function initializeImageModal() {
    // Modal functionality
    window.openModal = function(imageUrl) {
        console.log('Opening modal with image:', imageUrl);
        const modal = document.getElementById('imageModal');
        const modalImg = document.getElementById('modalImage');
        modal.style.display = "block";
        modalImg.src = imageUrl;
    }

    window.closeModal = function() {
        const modal = document.getElementById('imageModal');
        modal.style.display = "none";
    }

    // Close modal when clicking outside
    window.onclick = function(event) {
        const modal = document.getElementById('imageModal');
        if (event.target == modal) {
            closeModal();
        }
    }

    // Close modal with Escape key
    document.addEventListener('keydown', function(event) {
        if (event.key === "Escape") {
            closeModal();
        }
    });
}

// Initialize all functionality when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeImageModal();
    // ... other initializations

    // Get modal elements
    const modal = document.getElementById('imageModal');
    const modalImg = document.getElementById('modalImage');
    const closeBtn = document.querySelector('.close');
    const viewButtons = document.querySelectorAll('.view-image-btn');

    // Add click event to all view image buttons
    viewButtons.forEach(button => {
        button.addEventListener('click', function() {
            const imageUrl = this.getAttribute('data-image');
            console.log('Opening image:', imageUrl);
            modal.style.display = 'block';
            modalImg.src = imageUrl;
        });
    });

    // Close modal when clicking X button
    closeBtn.addEventListener('click', function() {
        modal.style.display = 'none';
    });

    // Close modal when clicking outside
    window.addEventListener('click', function(event) {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });

    // Close modal with Escape key
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape' && modal.style.display === 'block') {
            modal.style.display = 'none';
        }
    });
});
