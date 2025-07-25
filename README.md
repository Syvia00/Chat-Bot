# Chat-Bot

##  Introduction
This project is to develop a technical support chatbot for our customers using a Large Language Model API, such as ChatGPT, and training it with Asiga’s database of technical support dialogue. The result will be a web application which can answer customer questions with valid answers in real-time.

A language model, integrated within a web application, that can handle technical support as if it were a member of the support staff, accurately addressing customer issues by leveraging a decade's worth of knowledge from support tickets.

## System Design
The system is designed with fast API as a central controller that facilitates interaction between its key components: a web application that provides a chatbot interface with chatting features and chat history access; a language model trained by us based on OpenAI utilizes user-input generated formatted chatbot messages; MongoDB records user interactions with the chatbot, with each interaction associated with a unique ID, allowing users to Delete a specific session. The framework coordinates communications to provide users with a convenient problem-solving experience with a chatbot while maintaining a comprehensive record of interactions. 

## Technical Components

### 1. Front facing Web application: 
The website is crafted using a combination of JavaScript, HTML, and CSS. HTML provides the basic structural framework of a web page, describing content and layout through elements such as headings, paragraphs, lists, and links. Use CSS to handle the presentation and style of web content, manage layout, color, typography and responsive design to ensure the user's visual experience. JavaScript is a versatile scripting language used for adding interactivity and dynamic behavior to web pages, managing user interactions and fulfilling user requests.
FastAPI, a contemporary Python web framework, is specifically tailored for constructing APIs. It adeptly bridges the frontend, backend, and database to facilitate web application development. Within this project, we've set up several endpoints, including those for login authentication, initiating new chat sessions, submitting messages, and deleting chat sessions. These endpoints are invoked automatically when the web application starts or when specific events, such as pressing the submit button, are triggered.

### 2. Database:
Use MongoDB as the database to store data. MongoDB is a NoSQL database system, has a very flexible model to store data of different structures, and uses JSON-like to store data. The JSON-like format can help members quickly understand the data form and clearly display it to the client. It also provides convenience for front-end and back-end code writing. MongoDB offers robust security features, including authentication, role-based access control, encryption at rest, and auditing capabilities that help protect sensitive data.

### 3. Controller:
This component acts as a pipeline for all the components to talk to each other. It can pull from the database and send to the chatbot backend, then receive that output and send it to the database and frontend. This is a relatively new section and we don’t have a solid understanding of this.

### 4. Language Model:
This is where user input ends up, we give it to a trained language model and it will return an answer/response to the query. This is trained using a conversation data file in a JSONL format. The training is done via OpenAI API calls that handle the file uploading, string tokenizing and language model training for us. These are not formally part of the prototype’s system, but can be included as part of the final product so that future developers can build upon the system. As of writing, the model itself requires further testing and fine-tuning before it can be used as required by the client. This is due to the nature of the data and the time required to format it as well as the sheer amount of data required for a reliable response.

