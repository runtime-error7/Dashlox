// State variables
let currentChartInstance = null;
let currentChartConfig = null;
let isFileLoaded = false;

const chatHistory = document.getElementById('chat-history');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const placeholder = document.getElementById('chart-placeholder');
const statusBadge = document.getElementById('file-status');

// 1. Polling the backend to check if a CSV was dropped
async function checkStatus() {
    try {
        const res = await fetch('/api/status');
        const data = await res.json();
        
        if (data.active_table && !isFileLoaded) {
            isFileLoaded = true;
            statusBadge.innerHTML = `<span class="inline-block w-2 h-2 rounded-full bg-emerald-500 mr-1"></span>Loaded: <span class="text-emerald-400 font-bold">${data.active_table}</span>`;
            
            // Unlock the chat inputs
            userInput.disabled = false;
            sendBtn.disabled = false;
            
            addMessage('Dashlox', `Successfully loaded <b>${data.active_table}</b>. I detected these columns: <br><br><code>${data.columns.join(', ')}</code><br><br>What would you like to build?`);
        }
    } catch (err) {
        // Backend might be booting up, keep polling quietly
    }
}
// Check every 2 seconds
setInterval(checkStatus, 2000);

// 2. UI Helper to add chat messages
function addMessage(sender, text, isError = false) {
    const div = document.createElement('div');
    div.className = `chat-message p-3 rounded-lg border text-sm ${
        sender === 'You' 
            ? 'bg-indigo-950/40 border-indigo-900/50 text-indigo-200 self-end rounded-tr-none ml-8' 
            : isError
                ? 'bg-red-950/50 border-red-900/50 text-red-400 rounded-tl-none mr-8'
                : 'bg-slate-800 border-slate-700 text-slate-300 rounded-tl-none mr-8'
    }`;
    div.innerHTML = `<b>${sender}:</b><br>${text}`;
    chatHistory.appendChild(div);
    chatHistory.scrollTop = chatHistory.scrollHeight;
}

// 3. Handle sending the prompt to the AI
async function sendPrompt() {
    const prompt = userInput.value.trim();
    if (!prompt) return;

    addMessage('You', prompt);
    userInput.value = '';
    
    // Disable inputs while thinking
    userInput.disabled = true;
    sendBtn.disabled = true;
    sendBtn.innerText = 'Thinking...';

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                prompt: prompt, 
                current_chart: currentChartConfig 
            })
        });
        
        const data = await response.json();
        
        if (data.chart_config) {
            currentChartConfig = data.chart_config;
            renderChart(currentChartConfig);
            addMessage('Dashlox', 'Chart updated successfully! ✨');
        } else if (data.error) {
            addMessage('System', data.error, true);
        }
    } catch (err) {
        addMessage('System', 'Error communicating with backend. Check the terminal console.', true);
    } finally {
        // Re-enable inputs
        userInput.disabled = false;
        sendBtn.disabled = false;
        sendBtn.innerText = 'Send';
        userInput.focus();
    }
}

// Event listeners for sending
sendBtn.addEventListener('click', sendPrompt);
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendPrompt();
});

// 4. Render the Chart using Chart.js
function renderChart(config) {
    // Hide the placeholder text
    if (placeholder) placeholder.style.display = 'none';

    const ctx = document.getElementById('dashloxChart').getContext('2d');
    
    // Destroy previous chart to prevent glitching/overlapping
    if (currentChartInstance) {
        currentChartInstance.destroy();
    }
    
    // Apply a default dark-mode friendly font color globally for the new chart
    Chart.defaults.color = '#94a3b8'; // Tailwind slate-400
    
    currentChartInstance = new Chart(ctx, config);
}

// 5. Code Ejector (Copies current Chart JSON to clipboard)
document.getElementById('eject-btn').addEventListener('click', () => {
    if(!currentChartConfig) {
        alert("Generate a chart via the AI chat first!");
        return;
    }
    
    const exportString = `// Production Ready Chart.js Object\nconst chartData = ${JSON.stringify(currentChartConfig, null, 2)};`;
    navigator.clipboard.writeText(exportString);
    
    const btn = document.getElementById('eject-btn');
    const originalText = btn.innerText;
    btn.innerText = 'Copied! ✅';
    btn.classList.replace('bg-indigo-600', 'bg-emerald-600');
    
    setTimeout(() => {
        btn.innerText = originalText;
        btn.classList.replace('bg-emerald-600', 'bg-indigo-600');
    }, 2000);
});
