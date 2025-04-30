let ws = new WebSocket("ws://127.0.0.1:8000/ws");

ws.onopen = function() {
    appendMessage("Connected to WebSocket server");
};

ws.onmessage = function(event) {
    appendMessage(event.data);
};

ws.onclose = function() {
    appendMessage("Disconnected from WebSocket server");
};

function sendMessage() {
    let input = document.getElementById("messageInput");
    let message = input.value;
    if (message) {
        ws.send(message);
        appendMessage(`You: ${message}`);
        input.value = "";
    }
}

function appendMessage(message) {
    let messagesDiv = document.getElementById("messages");
    let msgElem = document.createElement("div");
    msgElem.textContent = message;
    messagesDiv.appendChild(msgElem);
    messagesDiv.scrollTop = messagesDiv.scrollHeight; // Auto-scroll
}
