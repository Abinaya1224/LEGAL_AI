document.addEventListener('DOMContentLoaded', () => {
    const noChatContainer = document.querySelector(".nochat-container");
    const chatContainer = document.querySelector(".chat-container");
    const chatbox = document.getElementById('chatbox');
    const inputs = document.querySelectorAll(".chatinput-item");
    const sendButtons = document.querySelectorAll(".sendBtn");
    const fileUploads = document.querySelectorAll("input[type='file']");
    let currentFileId = null; // Store latest uploaded file ID

    // Function to show chat container
    function showChatContainer() {
        noChatContainer.classList.add("d-none");
        chatContainer.classList.remove("d-none");
    }

    // Function to send message
    async function sendMessage(inputElement) {
        const message = inputElement.value.trim();
        if (!message) return;

        if (!currentFileId) {
            // Feedback to the user to upload a document
            const uploadMessageElem = document.createElement('li');
            uploadMessageElem.classList.add('chat-incoming', 'chat');

            // Add the figure and image for the incoming message
            uploadMessageElem.innerHTML = `
                <figure class="chat-image">
                    <img src="/static/images/solid-pro.svg" alt="brand-logo" />
                </figure>
                <p>Almost ready to help! 📑 Upload a document, and I'll dive right into your query like a detective on a case! 🕵️‍♂️</p>
            `;
            chatbox.appendChild(uploadMessageElem);
            chatbox.scrollTop = chatbox.scrollHeight;
            return;
        }

        // Display user message
        const userMessageElem = document.createElement('li');
        userMessageElem.classList.add('chat-outgoing', 'chat');
        userMessageElem.innerHTML = `
            
            <p>${message}</p>
        `;
        chatbox.appendChild(userMessageElem);

        inputElement.value = ''; // Clear input

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message, file_id: currentFileId }),
            });

            if (!response.ok) throw new Error(`Error: ${response.status}`);

            const data = await response.json();
            const aiMessageElem = document.createElement('li');
            aiMessageElem.classList.add('chat-incoming', 'chat');

            // Add the figure and img for the incoming message
            aiMessageElem.innerHTML = `
                <figure class="chat-image">
                   <img src="/static/images/solid-pro.svg" alt="brand-logo" />
                </figure>
                <p>${data.response}</p>
            `;
            chatbox.appendChild(aiMessageElem);

            chatbox.scrollTop = chatbox.scrollHeight;
        } catch (error) {
            console.error('Error:', error);
            const errorMessageElem = document.createElement('li');
            errorMessageElem.classList.add('chat-incoming', 'chat');
            errorMessageElem.innerHTML = `
                <figure class="chat-image">
                    <img src="/static/images/solid-pro.svg" alt="brand-logo" />
                </figure>
                <p>Sorry, something went wrong. Please try again later.</p>
            `;
            chatbox.appendChild(errorMessageElem);
            chatbox.scrollTop = chatbox.scrollHeight;
        }
    }

    // Attach event listeners to multiple inputs & buttons
    sendButtons.forEach((btn, index) => {
        btn.addEventListener('click', () => {
            showChatContainer();
            sendMessage(inputs[index]);
        });
    });

    inputs.forEach((input, index) => {
        input.addEventListener('keypress', (event) => {
            if (event.key === 'Enter') {
                event.preventDefault();
                showChatContainer();
                sendMessage(inputs[index]);
            }
        });
    });

    // Handle file uploads
    fileUploads.forEach(fileInput => {
        fileInput.addEventListener('change', async (event) => {
            const file = event.target.files[0];
            if (!file) return;

            showChatContainer();

            // Display file upload message
            const uploadMessageElem = document.createElement('li');
            uploadMessageElem.classList.add('chat-outgoing', 'chat');
            uploadMessageElem.innerHTML = `
                
                <p>Uploading document: ${file.name}...</p>
            `;
            chatbox.appendChild(uploadMessageElem);

            const formData = new FormData();
            formData.append('file', file);

            try {
                const uploadResponse = await fetch('/upload', {
                    method: 'POST',
                    body: formData,
                });

                if (!uploadResponse.ok) throw new Error(`Error: ${uploadResponse.status}`);

                const uploadData = await uploadResponse.json();
                currentFileId = uploadData.file_id;

                const uploadSuccessMessageElem = document.createElement('li');
                uploadSuccessMessageElem.classList.add('chat-incoming', 'chat');
                uploadSuccessMessageElem.innerHTML = `
                    <figure class="chat-image">
<img src="/static/images/solid-pro.svg" alt="brand-logo" />
                    </figure>
                    <p>File ${file.name} uploaded successfully.</p>
                `;
                chatbox.appendChild(uploadSuccessMessageElem);

                chatbox.scrollTop = chatbox.scrollHeight;
            } catch (error) {
                console.error('Upload Error:', error);
                const uploadErrorMessageElem = document.createElement('li');
                uploadErrorMessageElem.classList.add('chat-incoming', 'chat');
                uploadErrorMessageElem.innerHTML = `
                    <figure class="chat-image">
                        <img src="/static/images/solid-pro.svg" alt="brand-logo" />
                    </figure>
                    <p>Sorry, there was an error uploading the file.</p>
                `;
                chatbox.appendChild(uploadErrorMessageElem);
                chatbox.scrollTop = chatbox.scrollHeight;
            }
            
        });
        
    });
    
});
