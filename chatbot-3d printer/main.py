from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request, Form, HTTPException, Depends
from fastapi.responses import HTMLResponse, RedirectResponse,JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from pymongo import MongoClient
from db import authenticate_customer, start_new_chat_session, log_message,get_user_by_id, delete_session, get_messages_from_database, get_database, log_rate, log_feedback
# from chatgpt import chat_with_gpt3
from typing import List, Dict, Any
from langchainn import chat_with_bot


app = FastAPI()
app.mount("/static", StaticFiles(directory="src/static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this as needed for security in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="src/templates")

@app.get("/", response_class=HTMLResponse)
def user_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login") 
async def handle_login(request: Request, username: str = Form(...), password: str = Form(...)):
    # Validate the user credentials
    customer = authenticate_customer(username, password)
    if not customer:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})
    # Redirect to the chat page
    return RedirectResponse(url=f"/chat/{str(customer['_id'])}")

@app.post("/chat/{user_id}", response_class=HTMLResponse)
async def read_root(request: Request, user_id: str):
    customer = get_user_by_id(user_id)
    if not customer:
        raise HTTPException(status_code=404, detail="User not found")
    
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "user": customer["customer_name"], 
        "chat_data": customer["chat_sessions"],
        "user_id": str(customer['_id'])
    })

@app.post("/chat/{user_id}/submit")
async def submit_message(user_id: str, user_message: str = Form(...), session_id: str = Form(...)):
    try:
        # AI response using Langchain
        response_message = chat_with_bot(user_message)
        
        # Log the user's message
        try:
            log_result = log_message(user_id, session_id, "user", user_message)
            if "error" in log_result:
                raise HTTPException(status_code=500, detail=log_result["error"])
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
        # Log the chatbot's response
        try:
            log_result = log_message(user_id, session_id, "chatbot", response_message)
            if "error" in log_result:
                raise HTTPException(status_code=500, detail=log_result["error"])
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
        return JSONResponse(content={"message": response_message})
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))


@app.post("/start-session/{user_id}")
async def start_session(user_id: str):
    try:
        new_session = start_new_chat_session(user_id)
        if "error" in new_session:
            raise HTTPException(status_code=400, detail=new_session["error"])
        return {"session_id": new_session["session_id"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/delete-session/{user_id}/{session_id}")
async def delete_session_endpoint(user_id: str, session_id: str):
    try:
        result = delete_session(user_id, session_id)
        if result:
            return {"message": "Session deleted successfully"}
        else:
            raise HTTPException(status_code=400, detail="Session not found or could not be deleted")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


#hist caht onclick
class ChatMessage(BaseModel):
    _id: str
    sender: str
    content: str
    timestamp: str
    
@app.get("/get-session/{user_id}/{session_id}", response_model=List[ChatMessage])
def get_session(user_id: str, session_id: str, db: MongoClient = Depends(get_database)):
    try:
        print("Fetching messages...")
        messages = get_messages_from_database(user_id, session_id)
        print(f"Messages fetched: {messages}")
        
        if not messages or messages is None:
            print("No messages found, raising 404.")
            raise HTTPException(status_code=404, detail="No messages found for this session")
            
        return messages
    except HTTPException as http_e:
        print(f"HTTPException: {http_e.detail}")
        raise http_e
    except Exception as e:
        print(f"Exception occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    

## rating store
@app.post("/rate/{user_id}/{session_id}/{msg_id}/{rate}")
async def submit_fb(user_id: str, session_id: str, msg_id: str, rate: str):
    # print(f"session_id: {session_id}")
    # Log the user's message
    try:
        log_result = log_rate(user_id, session_id, msg_id, rate)
        if log_result:
            return {"message": "Rate successfully"}
        else:
            raise HTTPException(status_code=400, detail="Session not found or could not be deleted")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
## Feedback store
@app.post("/feedback/{user_id}/{session_id}/{msg_id}/{fb_message}")
async def submit_fb(user_id: str, session_id: str, msg_id: str, fb_message: str):
    # print(f"session_id: {session_id}")
    # Log the user's message
    try:
        log_result = log_feedback(user_id, session_id, msg_id, fb_message)
        if log_result:
            return {"message": "Submit successfully"}
        else:
            raise HTTPException(status_code=400, detail="Session not found or could not be deleted")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))