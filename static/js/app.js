const API_BASE = "http://127.0.0.1:5000";

/* Upload PDF */
async function uploadPDF() {
    const fileInput = document.getElementById("pdfFile");
    const status = document.getElementById("uploadStatus");

    if (!fileInput.files.length) {
        status.innerText = "Please select a PDF file.";
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    status.innerText = "Uploading...";

    try {
        const response = await fetch(`${API_BASE}/upload`, {
            method: "POST",
            body: formData
        });

        const result = await response.json();
        status.innerText = result.message || "Upload successful";
    } catch (error) {
        status.innerText = "Upload failed";
        console.error(error);
    }
}

/* Ask Question */
async function askQuestion() {
    const input = document.getElementById("questionInput");
    const chatBox = document.getElementById("chatBox");

    const question = input.value.trim();
    if (!question) return;

    addMessage("You", question, "user");
    input.value = "";

    try {
        const response = await fetch(`${API_BASE}/chat`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ question })
        });

        const result = await response.json();
        addMessage("AI", result.answer, "ai");
    } catch (error) {
        addMessage("AI", "Error getting response", "ai");
        console.error(error);
    }
}

/* Add Message to Chat */
function addMessage(sender, text, className) {
    const chatBox = document.getElementById("chatBox");

    const div = document.createElement("div");
    div.classList.add("message", className);
    div.innerHTML = `<strong>${sender}:</strong> ${text}`;

    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
}
