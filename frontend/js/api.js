// api.js - Handles communication with the FastAPI backend

const API_BASE = '/api';

async function scanURL(url) {
    try {
        const response = await fetch(`${API_BASE}/scan-url`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ url })
        });
        
        if (!response.ok) {
            throw new Error(`Server returned ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error("API Error:", error);
        return {
            status: 'high_risk',
            risk_score: 100,
            threat_level: "ERROR",
            summary: "Failed to connect to the analysis engine.",
            checks: [
                {
                    id: 'api_error',
                    title: 'Analysis Failed',
                    status: 'DANGER',
                    explanation: 'Could not reach the backend server or a timeout occurred.',
                }
            ],
            recommendations: ["Check your internet connection or try again later."]
        };
    }
}

async function scanMessage(message) {
    try {
        const response = await fetch(`${API_BASE}/scan-message`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message })
        });
        
        if (!response.ok) {
            throw new Error(`Server returned ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error("API Error:", error);
        return {
            status: 'high_risk',
            risk_score: 100,
            threat_level: "ERROR",
            summary: "Failed to connect to the analysis engine.",
            checks: [{
                id: 'api_error',
                title: 'Analysis Failed',
                status: 'DANGER',
                explanation: 'Could not reach the backend server.',
            }],
            recommendations: ["Check your internet connection."]
        };
    }
}

async function scanEmail(sender, subject, body) {
    try {
        const response = await fetch(`${API_BASE}/scan-email`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ sender, subject, body })
        });
        
        if (!response.ok) {
            throw new Error(`Server returned ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error("API Error:", error);
        return {
            status: 'high_risk',
            risk_score: 100,
            threat_level: "ERROR",
            summary: "Failed to connect to the analysis engine.",
            checks: [{
                id: 'api_error',
                title: 'Analysis Failed',
                status: 'DANGER',
                explanation: 'Could not reach the backend server.',
            }],
            recommendations: ["Check your internet connection."]
        };
    }
}

window.API = {
    scanURL,
    scanMessage,
    scanEmail
};
