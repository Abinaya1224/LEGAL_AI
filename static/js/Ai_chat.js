document.addEventListener('DOMContentLoaded', () => {
  const chatInput = document.getElementById('userInput');
  const chatbox = document.getElementById('chatbox');
  const sendButton = document.getElementById('sendBTN');
  const fileUploadInput = document.getElementById('fileUpload');

  let currentFileId = null; // Store the latest uploaded file_id

  // Function to send a message
  async function sendMessage() {
      const message = chatInput.value.trim();
      if (!message) return;

      if (!currentFileId) {
          alert("Please upload a document first.");
          return;
      }

      // Display user message in the chatbox
      const userMessageElem = document.createElement('li');
      userMessageElem.classList.add('chat-outgoing', 'chat');
      userMessageElem.innerHTML = `<p>${message}</p>`;
      chatbox.appendChild(userMessageElem);

      chatInput.value = ''; // Clear input field

      // Send the message to the server with file_id
      try {
          const response = await fetch('/chat', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ message, file_id: currentFileId }),
          });

          if (!response.ok) {
              throw new Error(`Error: ${response.status}`);
          }

          const data = await response.json();
          const aiMessageElem = document.createElement('li');
          aiMessageElem.classList.add('chat-incoming', 'chat');
          aiMessageElem.innerHTML = `<p>${data.response}</p>`;
          chatbox.appendChild(aiMessageElem);

          chatbox.scrollTop = chatbox.scrollHeight;
      } catch (error) {
          console.error('Error:', error);
          const errorMessageElem = document.createElement('li');
          errorMessageElem.classList.add('chat-incoming', 'chat');
          errorMessageElem.innerHTML = `<p>Sorry, something went wrong. Please try again later.</p>`;
          chatbox.appendChild(errorMessageElem);
          chatbox.scrollTop = chatbox.scrollHeight;
      }
  }

  sendButton.addEventListener('click', sendMessage);

  chatInput.addEventListener('keypress', (event) => {
      if (event.key === 'Enter') {
          event.preventDefault();
          sendMessage();
      }
  });

  // Handle file upload
  fileUploadInput.addEventListener('change', async (event) => {
      const file = event.target.files[0];
      if (!file) return;

      // Display file upload message
      const uploadMessageElem = document.createElement('li');
      uploadMessageElem.classList.add('chat-outgoing', 'chat');
      uploadMessageElem.innerHTML = `<p>Uploading document: ${file.name}...</p>`;
      chatbox.appendChild(uploadMessageElem);

      const formData = new FormData();
      formData.append('file', file);

      try {
          const uploadResponse = await fetch('/upload', {
              method: 'POST',
              body: formData,
          });

          if (!uploadResponse.ok) {
              throw new Error(`Error: ${uploadResponse.status}`);
          }

          const uploadData = await uploadResponse.json();
          currentFileId = uploadData.file_id; // Store file_id for future requests

          const uploadSuccessMessageElem = document.createElement('li');
          uploadSuccessMessageElem.classList.add('chat-incoming', 'chat');
          uploadSuccessMessageElem.innerHTML = `<p>File ${file.name} uploaded successfully.</p>`;
          chatbox.appendChild(uploadSuccessMessageElem);

          chatbox.scrollTop = chatbox.scrollHeight;
      } catch (error) {
          console.error('Upload Error:', error);
          const uploadErrorMessageElem = document.createElement('li');
          uploadErrorMessageElem.classList.add('chat-incoming', 'chat');
          uploadErrorMessageElem.innerHTML = `<p>Sorry, there was an error uploading the file.</p>`;
          chatbox.appendChild(uploadErrorMessageElem);
          chatbox.scrollTop = chatbox.scrollHeight;
      }
  });
});


