function addMessage(text, className) {
    let box = document.getElementById("chat-box");

    let msg = document.createElement("div");
    msg.className = className;
    msg.innerText = text;

    box.appendChild(msg);
    box.scrollTop = box.scrollHeight;
}

// 🔊 SPEAK
function speak(text) {
    let speech = new SpeechSynthesisUtterance(text);
    window.speechSynthesis.speak(speech);
}

// 📤 SEND QUERY
function sendQuery() {
    let input = document.getElementById("query");
    let query = input.value;

    if (!query) return;

    addMessage("You: " + query, "user");

    fetch("/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ query: query })
    })
    .then(res => res.json())
    .then(data => {
        let answer;

        if (data.answer) {
            answer = data.answer;
        } else if (data.balance) {
            answer = "Your balance is ₹" + data.balance;
        } else {
            answer = JSON.stringify(data);
        }

        addMessage("Bot: " + answer, "bot");

        // 🔥 VOICE OUTPUT
        speak(answer);
    });

    input.value = "";
}

// 🎤 VOICE INPUT
function startVoice() {
    let recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();

    recognition.start();

    recognition.onresult = function(event) {
        let voiceText = event.results[0][0].transcript;

        document.getElementById("query").value = voiceText;

        sendQuery();
    };
}