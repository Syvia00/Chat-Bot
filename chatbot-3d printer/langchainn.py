from typing import List, Dict
from langchain.chains import RetrievalQA
from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.llms import OpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.prompt import PromptTemplate
from langchain.memory import ConversationBufferMemory
import os
from dotenv import load_dotenv

# Define a function to load all documents in a directory
def load_all_documents_in_directory(directory_path):
    documents = []
    success_count, failed_count = 0, 0
    
    # Get a list of all files in the directory
    all_files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f)) and f.endswith('.txt')]

    # Load each file and concatenate the content to 'documents'
    for file in all_files:
        file_path = os.path.join(directory_path, file)
        try:
            loader = TextLoader(file_path, encoding = 'UTF-8').load()
            documents += loader
            success_count += 1
        except Exception as e:
            failed_count += 1
            print(f"Error loading {file_path}: {str(e)}")
    
    print(f"Loaded {success_count} files, failed to load {failed_count} files.")
    return documents

# Define a function to generate a response from the data provided
def chat_with_bot(question: str):
    try:
        # Custom template for the assistant's response
        custom_template = """
        You are an assistant. Given the chat history and a new question, provide a detailed and comprehensive answer. If you don't know the answer or you don't understand, kindly state that you're unsure. 

        Chat History:
        {chat_history}

        Question: {question}
        Answer respectfully:"""

        CUSTOM_QUESTION_PROMPT = PromptTemplate.from_template(custom_template)

        # Load environment variables from .env file
        load_dotenv()
        os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")

        # Specify the directory path containing documents
        directory_path = "src/real_data/quick-answers"
        directory_path2 = "src/real_data/support-website"
        directory_path3 = "src/real_data/user-guides"
        documents = load_all_documents_in_directory(directory_path)
        documents += load_all_documents_in_directory(directory_path2)
        documents += load_all_documents_in_directory(directory_path3)

        text_splitter = CharacterTextSplitter(chunk_size=2000, chunk_overlap=0)
        documents = text_splitter.split_documents(documents)

        embeddings = OpenAIEmbeddings()
        vectorstore = Chroma.from_documents(documents, embeddings)

        model = ChatOpenAI(model_name="gpt-3.5-turbo-16k", temperature=0.3)
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        
        qa = ConversationalRetrievalChain.from_llm(
            model,
            vectorstore.as_retriever(search_type="similarity_score_threshold", search_kwargs={'score_threshold': 0.8}),
            condense_question_prompt=CUSTOM_QUESTION_PROMPT,
            memory=memory
        )

        result = qa({"question": question})
        response_message = result['answer']

        return response_message

    except Exception as e:
        raise e

