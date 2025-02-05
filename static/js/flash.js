document.addEventListener("DOMContentLoaded", function () {
    fetch("/get_flash_messages")
        .then(response => response.json())
        .then(data => {
            if (data.messages.length > 0) {
                showFlashMessages(data.messages);
            }
        })
        .catch(error => console.error("Error fetching flash messages:", error));
});

function showFlashMessages(messages) {
    const flashContainer = document.getElementById("flash-message-container");

    messages.forEach(msg => {
        const flashMessage = document.createElement("div");
        flashMessage.classList.add("flash-message", msg.category);
        flashMessage.textContent = msg.message;

        flashContainer.appendChild(flashMessage);

        // Remove message after 3 seconds
        setTimeout(() => {
            flashMessage.remove();
        }, 3000);
    });
}
