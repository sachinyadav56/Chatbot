function sendMessage() {
    let userInput = document.getElementById("user-input").value;
    if (userInput === "") return;

    let chatBox = document.getElementById("chat-box");

    chatBox.innerHTML += `<div class="user">You: ${userInput}</div>`;
    document.getElementById("user-input").value = "";

    fetch("/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: userInput })
    })
    .then(response => response.json())
    .then(data => {
        chatBox.innerHTML += `<div class="bot">Bot: ${data.reply}</div>`;
        chatBox.scrollTop = chatBox.scrollHeight;
    });
}
