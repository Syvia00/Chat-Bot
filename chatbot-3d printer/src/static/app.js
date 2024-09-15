const chatForm = document.querySelector('#chatForm');
const userInput = document.querySelector('.user-input');
const chatContainer = document.querySelector('.chat-container');
let isFirstMessage = true; 
const submitBtn = document.querySelector('#submit');
const commonQuestionsContainer = document.querySelector('.common-questions');
let msgID = 0;

// Common questions
userInput.addEventListener('focus', function() {
    commonQuestionsContainer.style.display = 'none';
});

userInput.addEventListener('blur', function() {
    if (isFirstMessage) 
        commonQuestionsContainer.style.display = 'flex';
});

document.querySelectorAll('.common-question').forEach(button => {
    button.addEventListener('click', function() {
        console.log("executed!");
        userInput.value = this.textContent;
        commonQuestionsContainer.style.display = 'none';
        generateMsg(); // Send the message
    });
});

// Submit & generate message
submitBtn.addEventListener('click', async function(e) {
    e.preventDefault();
    await generateMsg();
});

//create current date and time
const getReadableTime = () => {

    const now = new Date();
    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, '0'); // months are 0-based in JavaScript
    const date = String(now.getDate()).padStart(2, '0');
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const seconds = String(now.getSeconds()).padStart(2, '0');
  
    const readableTime = `${year}/${month}/${date} ${hours}:${minutes}:${seconds}`;
    return readableTime;
  }

  // enable and disable input & btn----------------
const disableInput = () => {
    document.querySelector(".user-input").disabled = true;
    document.querySelector(".user-input").style.cursor = "no-drop";
    document.getElementById("submit").disabled = true;
    document.getElementById("submit").style.cursor = "no-drop";
}

const enableInput = () => {
    document.querySelector(".user-input").disabled = false;
    document.querySelector(".user-input").style.cursor = '';
    document.getElementById("submit").disabled = false;
    document.getElementById("submit").style.cursor = 'pointer';
}

// Generate message function
const generateMsg = async () => {
    const userMessage = userInput.value;

    // Check for an empty message
    if (userMessage.trim() === "") return;

    // Extract user ID
    const user_id = document.getElementById('user_id').value;

    // Start a session
    if (isFirstMessage) {
        const newSessionId = await startNewChatSession(user_id);
        console.log('runrunrun3');
        if (newSessionId) {
            document.getElementById('session_id').value = newSessionId; // Set the hidden input value
        }
        isFirstMessage = false;
    }

    // User message
    const userMessageDiv = document.createElement('div');
    userMessageDiv.className = 'user-message message';
    userMessageDiv.innerHTML = `<p>${userMessage}</p>`;
    chatContainer.appendChild(userMessageDiv);

    // Add temporary chatbot message to indicate it's processing
    const tempChatbotMessageWrapper = document.createElement('div');
    tempChatbotMessageWrapper.className = 'chatbot-message-wrapper temp-response';
    const tempChatbotIcon = document.createElement('img');
    tempChatbotIcon.src = "/static/resource/robot.png";
    tempChatbotIcon.alt = "Robot Icon";
    tempChatbotIcon.className = "robot-icon";
    tempChatbotMessageWrapper.appendChild(tempChatbotIcon);
    const tempChatbotMessageDiv = document.createElement('div');
    tempChatbotMessageDiv.className = 'chatbot-message message loading-animation';
    tempChatbotMessageDiv.innerHTML = `<p></p>`;
    tempChatbotMessageWrapper.appendChild(tempChatbotMessageDiv);
    chatContainer.appendChild(tempChatbotMessageWrapper);

    // Send message to the backend
    const formData = new FormData(chatForm);
    // Clear the user input after you have made the formData
    userInput.value = "";

    const response = await fetch(`/chat/${user_id}/submit`, {
        method: 'POST',
        body: formData
    });

    const data = await response.json();
    const chatbotResponse = data.message;

    // Remove temporary chatbot message
    const tempResponse = document.querySelector('.temp-response');
    if (tempResponse) tempResponse.remove();

    // Create and append the actual chatbot message to the chat container
    const chatbotMessageWrapper = document.createElement('div');
    chatbotMessageWrapper.className = 'chatbot-message-wrapper';
    msgID = msgID + 2;
    chatbotMessageWrapper.setAttribute("id", msgID);
    const chatbotIcon = document.createElement('img');
    chatbotIcon.src = "/static/resource/robot.png";
    chatbotIcon.alt = "Robot Icon";
    chatbotIcon.className = "robot-icon";
    chatbotMessageWrapper.appendChild(chatbotIcon);
    const chatbotMessageDiv = document.createElement('div');
    chatbotMessageDiv.className = 'chatbot-message message';
    chatbotMessageDiv.innerHTML = `<p>Asiga GPT: ${chatbotResponse}</p>`;
    chatbotMessageWrapper.appendChild(chatbotMessageDiv);
    chatContainer.appendChild(chatbotMessageWrapper);

    // Append the thumb icons
    const thumbUpIcon = document.createElement('i');
    thumbUpIcon.className = 'material-icons thumb-icon';
    thumbUpIcon.textContent = 'thumb_up';
    chatbotMessageWrapper.appendChild(thumbUpIcon);

    const thumbDownIcon = document.createElement('i');
    thumbDownIcon.className = 'material-icons thumb-icon';
    thumbDownIcon.textContent = 'thumb_down';
    chatbotMessageWrapper.appendChild(thumbDownIcon);

    const fbIcon = document.createElement('div');
    fbIcon.className = 'material-icons fb-icon';
    fbIcon.textContent = 'feedback';
    chatbotMessageWrapper.appendChild(fbIcon);

    chatContainer.appendChild(chatbotMessageWrapper);

    chatContainer.scrollTop = chatContainer.scrollHeight;
};


// Start a new chat session function when click new chat btn
const startNewChatSession = async (user_id) => {
    const response = await fetch(`/start-session/${user_id}`, {
        method: 'POST',
    });

    const data = await response.json();
    if (data.error) {
        console.error(data.error);
        return null;
    }

    // Create a new session element for the interface
    const historyContainer = document.querySelector('.history');
    const newSessionElement = document.createElement('div');
    newSessionElement.classList.add('history-item');
    newSessionElement.setAttribute('data-session-id', data.session_id);

    // Add the chat icon to the new session element
    const chatIcon = document.createElement('img');
    chatIcon.src = "/static/resource/chat1.png"; 
    chatIcon.alt = "Chat Icon";
    chatIcon.className = "chat-icon";
    newSessionElement.appendChild(chatIcon);

    // Add session start timestamp
    const newSessionTimestamp = document.createElement('p');
    newSessionTimestamp.textContent = getReadableTime();
    newSessionElement.appendChild(newSessionTimestamp);

    // Add delete icon
    const deleteIcon = document.createElement('div');
    deleteIcon.classList.add('delete-icon');
    deleteIcon.innerHTML = '&#10006;';
    newSessionElement.appendChild(deleteIcon);


    // Append the new session to the top of the history container
    historyContainer.prepend(newSessionElement);

    // Hide the common questions when a new chat is started
    commonQuestionsContainer.style.display = 'none';

    return data.session_id;
};


//---------------------user-input text area---------------------------------------

//text area adjustions
userInput.addEventListener('keydown', function(event) {
  // If Enter key is pressed and Shift key is not pressed
  if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault(); 
      generateMsg();
      this.style.height = '50px'; 
  }
});

// adjust textarea height function
userInput.addEventListener('input', function(e) {
  if (this.scrollHeight > this.clientHeight) {
      this.style.height = 'auto'; 
      this.style.height = (this.scrollHeight) + 'px';
  }
});

// Adjust textarea height on Shift+Enter
userInput.addEventListener('keydown', function(e) {
  if (e.key === 'Enter' && e.shiftKey) {
      this.style.height = 'auto'; 
      this.style.height = (this.scrollHeight) + 'px';
  }
});

//------------Collapse btn---------------------------
const sidebar = document.querySelector('.side-bar');
const mainContent = document.querySelector('.main');
const collapseBtn = document.getElementById('collapseBtn');
const openBtn = document.getElementById('openBtn');

collapseBtn.addEventListener('click', function() {
    if (sidebar.classList.contains('collapsed')) {
        // Expand the sidebar
        sidebar.classList.remove('collapsed');
        mainContent.classList.remove('with-collapsed-sidebar');
        // collapseBtn.innerHTML = "<<<";
        openBtn.style.display = 'none';
    } else {
        // Collapse the sidebar
        sidebar.classList.add('collapsed');
        mainContent.classList.add('with-collapsed-sidebar');
        // collapseBtn.innerHTML = ">>>";
        openBtn.style.display = 'block';
    }
});

openBtn.addEventListener('click', function() {
    sidebar.classList.remove('collapsed');
    mainContent.classList.remove('with-collapsed-sidebar');
    // collapseBtn.innerHTML = "<<<";
    openBtn.style.display = 'none';
});

// -----------New Chat -----------------------------------
const newChatBtn = document.querySelector('.new-chat-btn');

newChatBtn.addEventListener('click', function(e) {
    e.stopPropagation();
    startNewChatInterface();
});

const startNewChatInterface = () => {
    // Clear chat messages
    chatContainer.innerHTML = '';

    // Reset isFirstMessage flag
    isFirstMessage = true;

    // Add the initial chatbot message again.
    const chatbotMessageWrapper = document.createElement('div');
    chatbotMessageWrapper.className = 'chatbot-message-wrapper';

    const robotIcon = document.createElement('img');
    robotIcon.src = "/static/resource/robot.png";
    robotIcon.alt = "Robot Icon";
    robotIcon.className = "robot-icon";
    chatbotMessageWrapper.appendChild(robotIcon);

    const chatbotMessageDiv = document.createElement('div');
    chatbotMessageDiv.className = 'chatbot-message message';
    chatbotMessageDiv.innerHTML = `<p>Asiga GPT: How can I help you?</p>`;
    chatbotMessageWrapper.appendChild(chatbotMessageDiv);

    chatContainer.appendChild(chatbotMessageWrapper);

    //add comon questions back
    commonQuestionsContainer.style.display = 'flex';

    enableInput();
}



//----------- history chat session onclicked & delete----------------------------

document.addEventListener('click', async function(e) {
    let historyItem = e.target.closest('.history-item');
    
    // If the direct target of the event is the delete icon, handle delete action
    if (e.target && e.target.classList.contains('delete-icon')) {
        e.stopPropagation();
    
        if (historyItem) {
            const sessionId = historyItem.getAttribute('data-session-id');
            const user_id = document.getElementById('user_id').value;
            
            if (sessionId && user_id) {
                try {
                    const response = await fetch(`/delete-session/${user_id}/${sessionId}`, {
                        method: 'DELETE'
                    });
                    
                    if (response.ok) {
                        historyItem.remove();
    
                        // Check if the deleted session is the current session
                        const currentSessionId = document.getElementById('session_id').value;
                        console.log("checking here!!!  "+(currentSessionId === sessionId));
                        if (currentSessionId === sessionId) {
                            startNewChatInterface();
                        }
                        
                    } else {
                        console.error("Failed to delete session from backend.");
                    }
                } catch (err) {
                    console.error("Error:", err);
                }
            }
        }
        return;
    }

    // View history Only: **Haven't deal with removing viewing history refresh chat window yet**
    if (historyItem && !e.target.classList.contains('delete-icon')) {
        const sessionId = historyItem.getAttribute('data-session-id');
        const user_id = document.getElementById('user_id').value;

        commonQuestionsContainer.style.display = 'none'; // Set this to false so that the common questions are not shown

        // Show the loading animation before fetching the data
        const chatContainer = document.querySelector('.chat-container');
        chatContainer.innerHTML = '<div class="ring">Loading<span></span></div>';

        if (sessionId && user_id) {
            try {
                const response = await fetch(`/get-session/${user_id}/${sessionId}`, {
                    method: 'GET'
                });
                const data = await response.json();
                
                // Clear the loading animation now
                chatContainer.innerHTML = '';
                
                if (data && data.length > 0) {
                    populateChatHistory(data);
                } else {
                    console.error("No messages found for this session.");
                }
            } catch (err) {
                chatContainer.innerHTML = '<p>Error loading chat history.</p>';
                console.error("Error:", err);
            }
        }
        
        disableInput();
    }
});


// Function to populate the chat history
const populateChatHistory = (messages) => {
    chatContainer.innerHTML = ''; 
    messages.forEach(msg => {
        const messageDiv = document.createElement('div');
        messageDiv.className = msg.sender === 'user' ? 'user-message message' : 'chatbot-message message';
        messageDiv.innerHTML = `<p>${msg.sender === 'user' ? '' : 'Asiga GPT: '}${msg.content}</p>`;
        chatContainer.appendChild(messageDiv);
    });
}

// initially hide the common questions when the chat page loads if it's not the first message
if (!isFirstMessage) {
    commonQuestionsContainer.style.display = 'none';
}

// --------rate ----------
const submit_rate = async(msg_id, rate) =>{
    // Extract user ID
    const user_id = document.getElementById('user_id').value;
    const session_id = document.getElementById('session_id').value;
       
    const response = await fetch(`/rate/${user_id}/${session_id}/${msg_id}/${rate}`, {
        method: 'POST',
        // body: JSON.stringify(rate)
    });
}

//upvoke and downvote
document.addEventListener('click', function(event) {
    if (event.target && event.target.matches('.thumb-icon')) {
        const siblingThumb = (event.target.textContent === 'thumb_up') ? event.target.nextElementSibling : event.target.previousElementSibling;
        
        if (event.target.classList.contains('clicked')) {
            event.target.classList.remove('clicked');
            // remove upvote or downvote
        } else {
            event.target.classList.add('clicked');
            siblingThumb.classList.remove('clicked');
             // Extract user ID
            const msg_id = event.target.parentNode.id;

            if (event.target.textContent === 'thumb_up') {
                console.log('Upvoted!');
                // Your upvote logic here...
                submit_rate(msg_id.toString(), 'up');
            } else if (event.target.textContent === 'thumb_down') {
                console.log('Downvoted!');
                // Your downvote logic here...
                submit_rate(msg_id.toString(), 'down');
            }
        }
    }
});



// -------- feedback function ---------//

const submit_fb = async(fb_msg, msg_id) =>{
    if (fb_msg.trim() === "") return;

    // Extract user ID
    const user_id = document.getElementById('user_id').value;
    const session_id = document.getElementById('session_id').value;

    const response = await fetch(`/feedback/${user_id}/${session_id}/${msg_id}/${fb_msg}`, {
        method: 'POST',
        // body: JSON.stringify(fb_msg)
    });
}

// open feedback box
const openFB = async(a, msg_id) =>{
    // let feedback_section = a;
    let closeFB = null;
    let feedback_text = null;
    let feedback_submit = null;
    if (!a.classList.contains('feedback-open')){
        // open textbox
        const feedback = document.createElement('div');
        feedback.className = 'feedback-open';

        const feedback_t = document.createElement('div');
        feedback_t.className = 'feedback-textbox';

        const fb_textarea = document.createElement('textarea');
        fb_textarea.className = 'feedback-textarea';
        fb_textarea.setAttribute("name", "user_feedback");
        feedback_t.appendChild(fb_textarea);

        const fb_submit = document.createElement('button');
        fb_submit.className = 'submit-fb';
        fb_submit.setAttribute("id", "fb-submit-btn");
        fb_submit.innerHTML = 'submit';
        feedback_t.appendChild(fb_submit);

        const fb_close = document.createElement('button');
        fb_close.className = 'closefb-btn';
        fb_close.setAttribute("id", "fb-close-btn");
        feedback_t.appendChild(fb_close);

        feedback.appendChild(feedback_t);
        a.appendChild(feedback);
        // document.body.appendChild(feedback);

        closeFB = fb_close;
        feedback_text = fb_textarea;
        feedback_submit = fb_submit;
        a.classList.add('feedback-open');

        // close 
        closeFB.addEventListener('click', function() {
            // document.body.removeChild(feedback);
            a.classList.remove('feedback-open');
            a.removeChild(feedback)
        });

        // textarea submit feedback
        feedback_submit.addEventListener('click', function()  {
            console.log(feedback_text.value);
            if (feedback_text.value == ""){
                alert("Please provide valid feedback")
            }
            else{
                submit_fb(feedback_text.value, msg_id.toString());
                alert("Successfully Submit!!")
                // feedback_text.value = "";
                a.classList.remove('feedback-open');
                a.removeChild(feedback)
            }
        });
    }
}

document.addEventListener('click', function(event) {
    if (event.target && event.target.matches('.fb-icon')) {

            // event.target.classList.add('clicked');
             // Extract user ID
            const msg_id = event.target.parentNode.id;
            openFB(event.target.parentNode, msg_id);
        }
    
});