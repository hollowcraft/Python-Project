document.getElementById('send-btn').addEventListener('click', sendMessage);

function sendMessage() {
    const userInput = document.getElementById('user-input').value;
    if (userInput.trim() === "") return;

    // Ajouter le message de l'utilisateur à la boîte de chat
    appendMessage('user', userInput);

    // Envoyer le message au serveur Python
    fetch('http://localhost:5000/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: userInput }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.response) {
            appendMessage('ai', data.response);
        } else {
            appendMessage('ai', 'Erreur: Impossible de recevoir une réponse de l\'IA.');
        }
    })
    .catch(error => {
        console.error('Erreur:', error);
        appendMessage('ai', 'Erreur: Impossible de communiquer avec le serveur.');
    });

    // Effacer le champ de saisie
    document.getElementById('user-input').value = '';
}

function appendMessage(sender, message) {
    const chatBox = document.getElementById('chat-box');
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', sender);
    messageElement.textContent = message;
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight;
}