/*function sendMessage() {
    let userMessage = document.getElementById("userInput").value;
    
    fetch("http://127.0.0.1:5000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMessage })
    })
    .then(response => response.json())
    .then(data => {
        let chatbox = document.getElementById("chatbox");
        chatbox.innerHTML += `<p>User: ${userMessage}</p>`;
        chatbox.innerHTML += `<p>Bot: ${data.response}</p>`;
    });
}
    */


/*

// only user speak
// Function to send message and get response
function sendMessage() {
    let userMessage = document.getElementById("userInput").value;
    if (!userMessage.trim()) return;

    fetch("http://127.0.0.1:5000/chat", {  // Ensure API URL is correct
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMessage })
    })
    .then(response => response.json())
    .then(data => {
        let chatbox = document.getElementById("chatbox");
        chatbox.innerHTML += `<p>User: ${userMessage}</p>`;
        chatbox.innerHTML += `<p>Bot: ${data.response}</p>`;

        // Convert bot response to speech
        speak(data.response);
    });

    document.getElementById("userInput").value = "";  // Clear input field
}

// Function for speech synthesis (Text-to-Speech)
function speak(text) {
    let speech = new SpeechSynthesisUtterance(text);
    speech.lang = "en-US"; // Set language (change if needed)
    speech.volume = 1;
    speech.rate = 1;
    speech.pitch = 1;
    window.speechSynthesis.speak(speech);
}

// Function for voice input (Speech-to-Text)
function startListening() {
    let recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = "en-US"; // Set language
    recognition.start();

    recognition.onresult = function(event) {
        let userMessage = event.results[0][0].transcript;
        document.getElementById("userInput").value = userMessage;
        sendMessage();  // Send the recognized speech as input
    };
}

*/


/*
// Function to send message and get response
function sendMessage() {
    let userMessage = document.getElementById("userInput").value;
    if (!userMessage.trim()) return;

    fetch("http://127.0.0.1:5000/chat", {  // Ensure API URL is correct
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMessage })
    })
    .then(response => response.json())
    .then(data => {
        let chatbox = document.getElementById("chatbox");
        chatbox.innerHTML += `<p>User: ${userMessage}</p>`;
        chatbox.innerHTML += `<p>Bot: ${data.response}</p>`;

        // Bot speaks the response
        speak(data.response);
    });

    document.getElementById("userInput").value = "";  // Clear input field
}

// Function for speech synthesis (Text-to-Speech)
function speak(text) {
    let speech = new SpeechSynthesisUtterance(text);
    speech.lang = "en-US"; // Set language (change if needed)
    speech.volume = 1; // Adjust volume (0 to 1)
    speech.rate = 1; // Adjust speed (0.5 to 2)
    speech.pitch = 1; // Adjust pitch (0 to 2)
    window.speechSynthesis.speak(speech);
}

// Function for voice input (Speech-to-Text)
function startListening() {
    let recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = "en-US"; // Set language
    recognition.start();

    recognition.onresult = function(event) {
        let userMessage = event.results[0][0].transcript;
        document.getElementById("userInput").value = userMessage;
        sendMessage();  // Send the recognized speech as input
    };
}

*/




// Function to send message and get response

function sendMessage() {
    let userMessage = document.getElementById("userInput").value;
    if (!userMessage.trim()) return;

    fetch("http://127.0.0.1:5000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMessage })
    })
    .then(response => response.json())
    .then(data => {
        let chatbox = document.getElementById("chatbox");
        chatbox.innerHTML += `<p>User: ${userMessage}</p>`;
        chatbox.innerHTML += `<p>Bot: ${data.response}</p>`;

        // Bot speaks the response and changes animation
        speak(data.response);
    });

    document.getElementById("userInput").value = "";
}

// Function for speech synthesis (Text-to-Speech)
function speak(text) {
    let speech = new SpeechSynthesisUtterance(text);
    speech.lang = "en-US";
    speech.volume = 1;
    speech.rate = 1;
    speech.pitch = 1;

    // Change bot image to speaking animation
    document.getElementById("botImage").src = "static/bot_speaking.gif";

    speech.onend = function() {
        // Change back to idle image after speaking
        document.getElementById("botImage").src = "static/bot_idle.png";
    };

    window.speechSynthesis.speak(speech);
}

// Function for voice input (Speech-to-Text)
function startListening() {
    let recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = "en-US";
    recognition.start();

    recognition.onresult = function(event) {
        let userMessage = event.results[0][0].transcript;
        document.getElementById("userInput").value = userMessage;
        sendMessage();
    };
}


document.getElementById("facultyBtn").addEventListener("click", function () {
    document.getElementById("facultyLinks").classList.toggle("show");
});








/*

function sendMessage() {
    let userText = document.getElementById("userInput").value.trim();
    if (userText === "") return;

    // Display user message
    let chatbox = document.getElementById("chatbox");
    let userMessage = document.createElement("p");
    userMessage.classList.add("user");
    userMessage.innerText = userText;
    chatbox.appendChild(userMessage);

    // Generate quiz link if the user asks for a quiz
    if (userText.toLowerCase().includes("quiz on")) {
        let subject = userText.replace(/quiz on/i, "").trim();
        let quizLink = generateQuizLink(subject);

        let botMessage = document.createElement("p");
        botMessage.classList.add("bot");
        botMessage.innerHTML = `Here is a quiz on <b>${subject}</b>: <a href="${quizLink}" target="_blank">${quizLink}</a>`;
        chatbox.appendChild(botMessage);
    } else {
        // Default chatbot response
        let botMessage = document.createElement("p");
        botMessage.classList.add("bot");
        botMessage.innerText = "I'm here to help! Ask me for a quiz by saying 'Quiz on [subject]'.";
        chatbox.appendChild(botMessage);
    }

    // Clear input
    document.getElementById("userInput").value = "";
}

// Function to generate quiz links
function generateQuizLink(subject) {
    let baseURL = "https://example-quiz-platform.com/quiz"; // Replace with your actual quiz platform
    let formattedSubject = subject.replace(/\s+/g, "-").toLowerCase();
    return `${baseURL}/${formattedSubject}`;
}

*/

/*
function sendMessage() {
    let userText = document.getElementById("userInput").value.trim();
    if (userText === "") return;

    let chatbox = document.getElementById("chatbox");

    // Display user message
    let userMessage = document.createElement("p");
    userMessage.classList.add("user");
    userMessage.innerText = userText;
    chatbox.appendChild(userMessage);

    let botResponse = "";

    // Check if the user asks for a quiz
    if (userText.toLowerCase().includes("quiz on")) {
        let subject = userText.replace(/quiz on/i, "").trim();
        let quizLink = generateQuizLink(subject);
        botResponse = `Here is a quiz on ${subject}: ${quizLink}`;

        let botMessage = document.createElement("p");
        botMessage.classList.add("bot");
        botMessage.innerHTML = `Here is a quiz on <b>${subject}</b>: <a href="${quizLink}" target="_blank">${quizLink}</a>`;
        chatbox.appendChild(botMessage);
    } else {
        // Default chatbot response
        botResponse = "I'm here to help! Ask me for a quiz by saying 'Quiz on [subject]'.";

        let botMessage = document.createElement("p");
        botMessage.classList.add("bot");
        botMessage.innerText = botResponse;
        chatbox.appendChild(botMessage);
    }

    // Speak the bot response
    speakResponse(botResponse);

    // Clear input field
    document.getElementById("userInput").value = "";
}

// Function to generate quiz links
function generateQuizLink(subject) {
    let baseURL = "https://example-quiz-platform.com/quiz"; // Replace with your actual quiz platform
    let formattedSubject = subject.replace(/\s+/g, "-").toLowerCase();
    return `${baseURL}/${formattedSubject}`;
}

// Function to make the bot speak
function speakResponse(text) {
    let speech = new SpeechSynthesisUtterance(text);
    speech.lang = "en-US";
    speech.rate = 1.0;
    speech.pitch = 1.0;
    window.speechSynthesis.speak(speech);
}

// Voice input function
function startListening() {
    let recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = "en-US";

    recognition.onresult = function (event) {
        let userText = event.results[0][0].transcript;
        document.getElementById("userInput").value = userText;
        sendMessage();
    };

    recognition.start();
}

*/

/*
function sendMessage() {
    let userInput = document.getElementById("userInput").value.trim().toLowerCase();
    let chatbox = document.getElementById("chatbox");

    if (userInput === "") return;

    // Append user message
    let userMessage = document.createElement("p");
    userMessage.className = "user";
    userMessage.innerText = userInput;
    chatbox.appendChild(userMessage);

    // Bot response logic
    let botMessage = document.createElement("p");
    botMessage.className = "bot";

    let quizBaseURL = "https://www.geeksforgeeks.org/quizzes/";

    // Extract subject name from the user input
    let subjectMatch = userInput.match(/quiz on (.+)|(.+) quiz/i);
    if (subjectMatch) {
        let subject = subjectMatch[1] || subjectMatch[2]; // Extracted subject name
        let formattedSubject = subject.toLowerCase().replace(/\s+/g, "-"); // Convert to URL-friendly format
        let quizURL = `${quizBaseURL}${formattedSubject}-quiz-questions-and-answers/`;

        botMessage.innerHTML = `Here is a ${subject} quiz for you: <a href="${quizURL}" target="_blank">Click here</a>`;
    } else {
        botMessage.innerText = "I am here to assist you!";
    }

    chatbox.appendChild(botMessage);

    // Speak the response
    speakResponse(botMessage.innerText);

    document.getElementById("userInput").value = ""; // Clear input field
}

// Function to speak the bot's response
function speakResponse(text) {
    let speech = new SpeechSynthesisUtterance();
    speech.text = text;
    speech.lang = "en-US";
    speech.volume = 1;
    speech.rate = 1;
    speech.pitch = 1;
    window.speechSynthesis.speak(speech);
}

*/
