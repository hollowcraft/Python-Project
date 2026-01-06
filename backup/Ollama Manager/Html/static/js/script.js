let currentModel = null;
let fontSize = 14;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadModels();
    setupEventListeners();
});

function setupEventListeners() {
    document.getElementById('sendBtn').addEventListener('click', sendMessage);
    document.getElementById('messageInput').addEventListener('keypress', e => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    // Settings
    document.getElementById('settingsBtn').addEventListener('click', () => {
        document.getElementById('settingsModal').style.display = 'block';
    });

    document.getElementById('fontSizeSlider').addEventListener('input', e => {
        fontSize = parseInt(e.target.value);
        document.getElementById('fontSizeValue').textContent = fontSize;
        document.getElementById('chatArea').style.fontSize = `${fontSize}px`;
    });

    // Close modal when clicking outside
    window.addEventListener('click', e => {
        if (e.target === document.getElementById('settingsModal')) {
            document.getElementById('settingsModal').style.display = 'none';
        }
    });
}

async function loadModels() {
    try {
        console.log('Fetching models...');
        const response = await fetch('/api/models');
        const data = await response.json();
        console.log('Models response:', data);
        
        if (data.success) {
            const modelsList = document.getElementById('modelsList');
            if (!modelsList) {
                console.error('modelsList element not found');
                return;
            }
            modelsList.innerHTML = '';
            
            data.models.forEach(model => {
                console.log('Adding model:', model);
                const div = document.createElement('div');
                div.className = 'list-item';
                div.textContent = model;
                div.onclick = () => selectModel(model);
                modelsList.appendChild(div);
            });
        } else {
            console.error('Failed to load models:', data.error);
        }
    } catch (error) {
        console.error('Error loading models:', error);
    }
}

async function selectModel(model) {
    currentModel = model;
    highlightSelected('modelsList', model);
    loadChats(model);
}

async function loadChats(model) {
    try {
        const response = await fetch(`/api/chats/${model}`);
        const data = await response.json();
        
        if (data.success) {
            const chatsList = document.getElementById('chatsList');
            chatsList.innerHTML = '';
            
            data.chats.forEach(chat => {
                const div = document.createElement('div');
                div.className = 'list-item';
                div.textContent = chat.date;
                div.onclick = () => loadChatContent(model, chat.id);
                chatsList.appendChild(div);
            });
        }
    } catch (error) {
        console.error('Error loading chats:', error);
    }
}

async function loadChatContent(model, chatId) {
    try {
        const response = await fetch(`/api/chat/${model}/${chatId}`);
        const data = await response.json();
        
        if (data.success) {
            const chatArea = document.getElementById('chatArea');
            chatArea.innerHTML = '';
            
            data.messages.forEach(msg => {
                appendMessage(msg.role, msg.content);
            });
        }
    } catch (error) {
        console.error('Error loading chat content:', error);
    }
}

async function sendMessage() {
    if (!currentModel) {
        alert('Please select a model first');
        return;
    }

    const input = document.getElementById('messageInput');
    const message = input.value.trim();
    
    if (!message) return;

    appendMessage('user', message);
    input.value = '';

    try {
        const response = await fetch(`/api/chat/${currentModel}/send`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                model: currentModel,
                message: message
            })
        });

        const data = await response.json();
        
        if (data.success) {
            appendMessage('assistant', data.response);
        } else {
            appendMessage('error', 'Error: ' + data.error);
        }
    } catch (error) {
        console.error('Error sending message:', error);
        appendMessage('error', 'Error sending message');
    }
}

function appendMessage(role, content) {
    const chatArea = document.getElementById('chatArea');
    const div = document.createElement('div');
    div.className = `message ${role}`;
    div.textContent = content;
    chatArea.appendChild(div);
    chatArea.scrollTop = chatArea.scrollHeight;
}

function highlightSelected(listId, selectedItem) {
    const items = document.getElementById(listId).getElementsByClassName('list-item');
    for (let item of items) {
        item.classList.remove('active');
        if (item.textContent === selectedItem) {
            item.classList.add('active');
        }
    }
}