// scanner.js - Handles form submission and loading states

const loadingSteps = ["Checking structure...", "Inspecting data...", "Calculating risk..."];

async function startScan(type, inputData, apiCall) {
    const activeForm = document.querySelector('.tab-content.active form');
    const scanBtn = activeForm.querySelector('.btn-scan');
    const loadingState = document.getElementById('loading-state');
    const loadingText = document.getElementById('loading-text');
    const steps = document.querySelectorAll('.loading-steps .step');
    
    // Hide form elements, show loading
    Array.from(activeForm.children).forEach(child => {
        if (!child.classList.contains('loading-state')) {
            child.style.display = 'none';
        }
    });
    
    scanBtn.disabled = true;
    loadingState.style.display = 'block';
    loadingText.textContent = `Analyzing ${type}...`;
    
    // Animate steps for visual effect (backend is usually fast)
    let stepIdx = 0;
    const stepInterval = setInterval(() => {
        steps.forEach(s => s.classList.remove('active'));
        if (stepIdx < steps.length) {
            steps[stepIdx].classList.add('active');
            steps[stepIdx].textContent = loadingSteps[stepIdx % loadingSteps.length];
            stepIdx++;
        }
    }, 600);
    
    try {
        // Minimum visual delay so user sees the cool animation
        const minDelay = new Promise(resolve => setTimeout(resolve, 2000));
        
        // Execute API Call
        const [result, _] = await Promise.all([apiCall(), minDelay]);
        
        clearInterval(stepInterval);
        
        // Ensure forms are visible again for next time
        Array.from(activeForm.children).forEach(child => {
            if (!child.classList.contains('loading-state')) {
                child.style.display = '';
            }
        });
        loadingState.style.display = 'none';
        scanBtn.disabled = false;
        
        // Show result
        window.UI.showResult(result);
        
        // Add to history
        let historyInput = inputData;
        if (type === 'Email') {
            historyInput = `Subject: ${inputData.subject}`;
        }
        window.History.add(type, historyInput, result.risk_score, result.threat_level);
        
    } catch (error) {
        console.error("Scan error:", error);
        clearInterval(stepInterval);
        loadingState.style.display = 'none';
        scanBtn.disabled = false;
        Array.from(activeForm.children).forEach(child => {
            if (!child.classList.contains('loading-state')) {
                child.style.display = '';
            }
        });
        alert("An error occurred during scanning. Please try again.");
    }
}

document.addEventListener('DOMContentLoaded', () => {
    
    // URL Form
    const urlForm = document.getElementById('url-form');
    if (urlForm) {
        urlForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const url = document.getElementById('url-input').value.trim();
            if (url) {
                startScan('URL', url, () => window.API.scanURL(url));
            }
        });
    }
    
    // Message Form
    const messageForm = document.getElementById('message-form');
    if (messageForm) {
        messageForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const message = document.getElementById('message-input').value.trim();
            if (message) {
                startScan('Message', message, () => window.API.scanMessage(message));
            }
        });
    }
    
    // Email Form
    const emailForm = document.getElementById('email-form');
    if (emailForm) {
        emailForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const sender = document.getElementById('email-sender').value.trim();
            const subject = document.getElementById('email-subject').value.trim();
            const body = document.getElementById('email-body').value.trim();
            
            if (sender && subject && body) {
                const data = { sender, subject, body };
                startScan('Email', data, () => window.API.scanEmail(sender, subject, body));
            }
        });
    }
    
    // Example Buttons
    document.querySelectorAll('.example-btn:not(.email-example)').forEach(btn => {
        btn.addEventListener('click', () => {
            const inputId = btn.getAttribute('data-input');
            const val = btn.getAttribute('data-val');
            const input = document.getElementById(inputId);
            if (input) {
                input.value = val;
                input.dispatchEvent(new Event('input')); // trigger clear button logic if any
            }
        });
    });
    
    document.querySelectorAll('.email-example').forEach(btn => {
        btn.addEventListener('click', () => {
            document.getElementById('email-sender').value = btn.getAttribute('data-sender');
            document.getElementById('email-subject').value = btn.getAttribute('data-subject');
            document.getElementById('email-body').value = btn.getAttribute('data-body');
        });
    });
});
