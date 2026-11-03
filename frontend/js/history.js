// history.js - Manages local storage history

const HISTORY_KEY = 'phishguard_history';
const MAX_HISTORY = 20;

function getHistory() {
    try {
        const history = localStorage.getItem(HISTORY_KEY);
        return history ? JSON.parse(history) : [];
    } catch (e) {
        console.error("Could not read from localStorage", e);
        return [];
    }
}

function addHistoryItem(type, input, score, result) {
    const history = getHistory();
    
    // Create new item
    const newItem = {
        id: Date.now().toString(),
        type,
        input: input.length > 50 ? input.substring(0, 47) + '...' : input,
        score,
        result,
        timestamp: new Date().toISOString()
    };
    
    // Add to beginning of array
    history.unshift(newItem);
    
    // Limit size
    if (history.length > MAX_HISTORY) {
        history.pop();
    }
    
    try {
        localStorage.setItem(HISTORY_KEY, JSON.stringify(history));
    } catch (e) {
        console.error("Could not write to localStorage", e);
    }
    
    renderHistory();
}

function clearHistory() {
    try {
        localStorage.removeItem(HISTORY_KEY);
        renderHistory();
    } catch (e) {
        console.error("Could not clear localStorage", e);
    }
}

function renderHistory() {
    const history = getHistory();
    const tbody = document.getElementById('history-body');
    
    if (!tbody) return;
    
    // Update Stats
    document.getElementById('stat-total').textContent = history.length;
    document.getElementById('stat-safe').textContent = history.filter(i => i.result === 'SAFE').length;
    document.getElementById('stat-suspicious').textContent = history.filter(i => i.result === 'SUSPICIOUS' || i.result === 'LOW RISK').length;
    document.getElementById('stat-high-risk').textContent = history.filter(i => i.result === 'HIGH RISK').length;
    
    // Render Table
    tbody.innerHTML = '';
    
    if (history.length === 0) {
        tbody.innerHTML = '<tr class="empty-row"><td colspan="5">No scan history available.</td></tr>';
        return;
    }
    
    history.forEach(item => {
        const tr = document.createElement('tr');
        
        // Type badge
        let typeIcon = 'globe';
        if (item.type === 'Message') typeIcon = 'message-dots';
        if (item.type === 'Email') typeIcon = 'envelope';
        
        // Result color class
        let resultClass = 'threat-safe';
        if (item.result === 'LOW RISK') resultClass = 'threat-low_risk';
        if (item.result === 'SUSPICIOUS') resultClass = 'threat-suspicious';
        if (item.result === 'HIGH RISK') resultClass = 'threat-high_risk';
        
        // Format Date
        const date = new Date(item.timestamp);
        const timeStr = date.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
        const dateStr = date.toLocaleDateString();
        
        tr.innerHTML = `
            <td><i class='bx bx-${typeIcon}'></i> ${item.type}</td>
            <td title="${item.input}">${item.input}</td>
            <td><strong>${item.score}</strong>/100</td>
            <td><span class="badge ${resultClass}">${item.result}</span></td>
            <td>${dateStr} ${timeStr}</td>
        `;
        tbody.appendChild(tr);
    });
}

// Bind clear button
document.addEventListener('DOMContentLoaded', () => {
    renderHistory();
    const clearBtn = document.getElementById('clear-history');
    if (clearBtn) {
        clearBtn.addEventListener('click', () => {
            if (confirm("Are you sure you want to clear your local scan history?")) {
                clearHistory();
            }
        });
    }
});

window.History = {
    add: addHistoryItem,
    render: renderHistory
};
