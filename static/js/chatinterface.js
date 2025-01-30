document.getElementById('aiChatLink').addEventListener('click', function (e) {
    e.preventDefault(); // Prevent default anchor behavior
  
    const aiChatLink = this.getAttribute('data-page'); // Get the URL for AI Chat content
  
    // Fetch the content of AI Chat dynamically
    fetch(aiChatLink)
        .then(response => response.text())
        .then(data => {
            // Replace main content with fetched HTML
            document.getElementById('main-content').innerHTML = data;
  
            // Now initialize the chat interface
            createChatInterface();
        })
        .catch(error => console.error('Error loading AI Chat page:', error));
  });
  
  function createChatInterface() {
    const chatContainer = document.getElementById('chat-container');
    if (!chatContainer) {
      console.error("Chat container not found!");
      return;
    }
  
    // Reset main container styles
    chatContainer.style.display = 'flex';
    chatContainer.style.flexDirection = 'column';
    chatContainer.style.height = '100vh';
    chatContainer.style.padding = '20px';
    chatContainer.style.maxWidth = '1200px';
    chatContainer.style.margin = '0 auto';
    chatContainer.style.position = 'relative';
  
    // Add profile container at the top (keeping existing styling)
    const profileContainer = document.createElement('div');
    profileContainer.classList.add('profile-container');
    profileContainer.style.display = 'flex';
    profileContainer.style.justifyContent = 'flex-end';
    profileContainer.style.gap = '10px';
    profileContainer.style.padding = '10px';
    profileContainer.style.position = 'absolute';
    profileContainer.style.top = '10px';
    profileContainer.style.right = '20px';
  
   
  
    // Create content area
    const contentArea = document.createElement('div');
    contentArea.id = 'contentArea';
    contentArea.innerHTML = 
      `<h2>Welcome to Legal AI</h2>
      <p>The power of AI at your service - Tame the knowledge !</p>`;
    contentArea.style.textAlign = 'center';
    contentArea.style.marginTop = '60px'; // Add space below profile icons
  
    // Create chat area with adjusted positioning
    const chatArea = document.createElement('div');
    chatArea.id = 'chatArea';
    chatArea.style.width = '885px';
    chatArea.style.height = 'calc(100vh - 280px)'; // Adjusted height
    chatArea.style.overflowY = 'auto';
    chatArea.style.display = 'none';
    chatArea.style.margin = '20px auto';
    chatArea.style.marginTop = '80px'; // Increased top margin to avoid overlap
    chatArea.style.paddingLeft = '20px';
    chatArea.style.paddingRight = '20px';
  
    // Create chat interface
    const chatInterface = document.createElement('div');
    chatInterface.classList.add('chat-interface');
    chatInterface.style.width = '885px';
    chatInterface.style.backgroundColor = '#f5f5f5';
    chatInterface.style.borderRadius = '10px';
    chatInterface.style.padding = '15px';
    chatInterface.style.display = 'flex';
    chatInterface.style.gap = '10px';
    chatInterface.style.alignItems = 'center';
    chatInterface.style.margin = '0 auto';
    chatInterface.style.marginTop = '20px';
    chatInterface.style.boxShadow = '0 2px 6px rgba(0, 0, 0, 0.1)';
  
    // Rest of the code remains the same...
    const messageInput = document.createElement('textarea');
    messageInput.id = 'messageInput';
    messageInput.placeholder = 'Please upload your document';
    messageInput.style.flex = '1';
    messageInput.style.padding = '12px';
    messageInput.style.borderRadius = '8px';
    messageInput.style.border = 'none';
    messageInput.style.resize = 'none';
    messageInput.style.height = '40px';
    messageInput.style.backgroundColor = '#f5f5f5';
    messageInput.style.fontSize = '14px';
  
    const actionsContainer = document.createElement('div');
    actionsContainer.style.display = 'flex';
    actionsContainer.style.gap = '10px';
  
    const fileUpload = document.createElement('input');
    fileUpload.id = 'fileUpload';
    fileUpload.type = 'file';
    fileUpload.accept = '.pdf, .doc, .docx, .txt';
    fileUpload.style.display = 'none';
  
    const fileUploadLabel = document.createElement('button');
    fileUploadLabel.htmlFor = 'fileUpload';
    fileUploadLabel.innerHTML = '<i class="fas fa-paperclip"></i>';
   
    fileUploadLabel.style.border = 'none';
    fileUploadLabel.style.cursor = 'pointer';
    fileUploadLabel.style.padding = '8px';
  
    const sendButton = document.createElement('button');
    sendButton.id = 'sendButton';
    sendButton.title = 'Send Message';
    sendButton.innerHTML = '<i class="fas fa-paper-plane"></i>';
    sendButton.style.backgroundColor = 'transparent';
    sendButton.style.border = 'none';
    sendButton.style.cursor = 'pointer';
    sendButton.style.padding = '8px';
  
    actionsContainer.appendChild(fileUploadLabel);
    actionsContainer.appendChild(sendButton);
  
    chatInterface.appendChild(messageInput);
    chatInterface.appendChild(actionsContainer);
  
    // Assemble the layout
    chatContainer.appendChild(profileContainer);
    chatContainer.appendChild(contentArea);
    chatContainer.appendChild(chatArea);
    chatContainer.appendChild(chatInterface);
  
    // Message handling function remains the same...
    function addMessageToChat(message, isUser = true) {
      if (contentArea.style.display !== 'none') {
        contentArea.style.display = 'none';
        chatArea.style.display = 'block';
      }
  
      const messageContainer = document.createElement('div');
      messageContainer.style.display = 'flex';
      messageContainer.style.justifyContent = isUser ? 'flex-end' : 'flex-start';
      messageContainer.style.width = '100%';
      messageContainer.style.marginBottom = '16px';
  
      const messageDiv = document.createElement('div');
      messageDiv.textContent = message;
      messageDiv.style.background = isUser ? '#0084ff' : '#e9ecef';
      messageDiv.style.color = isUser ? '#fff' : '#000';
      messageDiv.style.borderRadius = '18px';
      messageDiv.style.padding = '8px 16px';
      messageDiv.style.maxWidth = '80%';
      messageDiv.style.fontSize = '14px';
      messageDiv.style.lineHeight = '1.4';
      messageDiv.style.boxShadow = '0 1px 2px rgba(0, 0, 0, 0.1)';
  
      messageContainer.appendChild(messageDiv);
      chatArea.appendChild(messageContainer);
      chatArea.scrollTop = chatArea.scrollHeight;
    }
  
    // Event listeners for sending message and file upload
    sendButton.addEventListener('click', () => {
      const message = messageInput.value.trim();
      if (message) {
        addMessageToChat(message, true);
        messageInput.value = '';
        setTimeout(() => {
          addMessageToChat("This is an AI response.", false);
        }, 1000);
      }
    });
  
    fileUploadLabel.addEventListener('click', () => {
      fileUpload.click();
    });
  
    fileUpload.addEventListener('change', (event) => {
      const file = event.target.files[0];
      if (file) {
        addMessageToChat(`File "${file.name}" uploaded successfully.`, true);
        setTimeout(() => {
          addMessageToChat("File received successfully.", false);
        }, 1000);
      }
    });
  
    messageInput.addEventListener('keydown', (event) => {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault(); // Prevents new line in textarea
            sendButton.click(); // Trigger send button click
        }
    });
  }