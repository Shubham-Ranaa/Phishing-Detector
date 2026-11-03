// ui.js - Handles rendering results and animations

function animateValue(obj, start, end, duration) {
    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        obj.innerHTML = Math.floor(progress * (end - start) + start);
        if (progress < 1) {
            window.requestAnimationFrame(step);
        } else {
            obj.innerHTML = end; // Ensure final value is exact
        }
    };
    window.requestAnimationFrame(step);
}

function showResultDashboard(resultData) {
    // Hide scanner, show dashboard
    document.querySelector('.scanner-container').style.display = 'none';
    const dashboard = document.getElementById('result-dashboard');
    dashboard.style.display = 'block';
    dashboard.classList.add('fade-in');
    
    // 1. Set Threat Level & Colors
    const threatLevelEl = document.getElementById('threat-level');
    threatLevelEl.textContent = resultData.threat_level;
    
    // Reset classes
    threatLevelEl.className = 'threat-level';
    threatLevelEl.classList.add(`threat-${resultData.status}`);
    
    // Score ring color
    let ringColor = '#10b981'; // Green
    if (resultData.status === 'low_risk') ringColor = '#3b82f6';
    if (resultData.status === 'suspicious') ringColor = '#f59e0b';
    if (resultData.status === 'high_risk') ringColor = '#ef4444';
    
    const circle = document.getElementById('score-circle');
    circle.style.stroke = ringColor;
    
    // Animate Score
    const scoreValEl = document.getElementById('score-value');
    animateValue(scoreValEl, 0, resultData.risk_score, 1500);
    
    // Animate SVG Ring (Circumference is 100 for this path)
    // Delay slightly for effect
    setTimeout(() => {
        circle.setAttribute('stroke-dasharray', `${resultData.risk_score}, 100`);
    }, 100);
    
    // 2. Summary Text
    document.getElementById('result-summary').textContent = resultData.summary;
    
    // 3. Why Flagged?
    const flaggedList = document.getElementById('why-flagged-list');
    flaggedList.innerHTML = '';
    const badChecks = resultData.checks.filter(c => c.status === 'WARNING' || c.status === 'DANGER');
    
    if (badChecks.length > 0) {
        badChecks.forEach(check => {
            const li = document.createElement('li');
            li.textContent = check.explanation;
            flaggedList.appendChild(li);
        });
    } else {
        const li = document.createElement('li');
        li.textContent = "No significant risk indicators were found.";
        flaggedList.appendChild(li);
    }
    
    // 4. Recommendations
    const recList = document.getElementById('recommendations-list');
    recList.innerHTML = '';
    resultData.recommendations.forEach(rec => {
        const li = document.createElement('li');
        li.textContent = rec;
        recList.appendChild(li);
    });
    
    // 5. Detailed Checks
    const checksList = document.getElementById('checks-list');
    checksList.innerHTML = '';
    
    // Sort checks by severity
    const statusOrder = { 'DANGER': 0, 'WARNING': 1, 'INFO': 2, 'PASS': 3 };
    const sortedChecks = [...resultData.checks].sort((a, b) => statusOrder[a.status] - statusOrder[b.status]);
    
    sortedChecks.forEach(check => {
        const item = document.createElement('div');
        item.className = `check-item status-${check.status.toLowerCase()}`;
        
        let icon = 'info-circle';
        if (check.status === 'PASS') icon = 'check-circle';
        if (check.status === 'WARNING') icon = 'error';
        if (check.status === 'DANGER') icon = 'x-circle';
        
        item.innerHTML = `
            <div class="check-header">
                <i class='bx bx-${icon}'></i> ${check.title}
            </div>
            <div class="check-desc">${check.explanation}</div>
        `;
        checksList.appendChild(item);
    });
    
    // Scroll to dashboard
    dashboard.scrollIntoView({ behavior: 'smooth' });
}

function resetScanner() {
    document.getElementById('result-dashboard').style.display = 'none';
    document.querySelector('.scanner-container').style.display = 'block';
    
    // Reset SVG ring
    document.getElementById('score-circle').setAttribute('stroke-dasharray', '0, 100');
    document.getElementById('score-value').textContent = '0';
    
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Bind New Scan Button
document.addEventListener('DOMContentLoaded', () => {
    const newScanBtn = document.getElementById('btn-new-scan');
    if (newScanBtn) {
        newScanBtn.addEventListener('click', resetScanner);
    }
});

window.UI = {
    showResult: showResultDashboard,
    reset: resetScanner
};
