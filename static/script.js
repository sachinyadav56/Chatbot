function sendMessage() {
    let inputField = document.getElementById("user-input");
    let userInput = inputField.value.trim();
    if (!userInput) return;

    let chatBox = document.getElementById("chat-box");

    // Show user message
    chatBox.innerHTML += `<div class="user">You: ${escapeHTML(userInput)}</div>`;
    inputField.value = "";

    fetch("/chatbot", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userInput })
    })
    .then(response => response.json())
    .then(data => {
        chatBox.innerHTML += `<div class="bot">Bot: ${escapeHTML(data.reply)}</div>`;
        chatBox.scrollTop = chatBox.scrollHeight;
    })
    .catch(err => {
        console.error("Fetch error:", err);
        chatBox.innerHTML += `<div class="bot">Bot: Server error</div>`;
        chatBox.scrollTop = chatBox.scrollHeight;
    });
}

// Press Enter to send
document.getElementById("user-input").addEventListener("keydown", function(e) {
    if (e.key === "Enter") sendMessage();
});

// Escape HTML to prevent injection
function escapeHTML(text) {
    return text.replace(/[&<>"']/g, function(m) {
        return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' }[m];
    });
}
