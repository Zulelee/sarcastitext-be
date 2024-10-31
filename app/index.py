#JSONIFY for return json
#REQUEST incoming request data
#MAKE_REQUEST for TELL BROWSER BASIC AUTHENTICATION IS REQUIRED OF LOGIN
from datetime import datetime
from fastapi import Depends, FastAPI, HTTPException, Body, Response

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from pydantic import EmailStr
from aiosmtplib import SMTP
from email.message import EmailMessage


# Load environment variables from the .env file
load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

app = FastAPI(docs_url="/api/docs", openapi_url="/api/openapi.json")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database Connection
# Connection String
uri = str(os.environ.get("MONGODB_URL"))

gptClient = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db = client[str(os.environ.get("MONGODB_DATABASE"))] # Database
users_collection = db[str(os.environ.get("MONGODB_COLLECTION"))] # Collection

class User(BaseModel):
    email: str
    password: str
    username: str

class Contact(BaseModel):
    name: str
    email: str
    message: str


@app.get("/")
async def root():
    try:
        client.admin.command('ping')
        return {"Pinged your deployment. You successfully connected to MongoDB!"}
    except Exception as e:
        return {e}

@app.post("/contact")
async def contact_us(
    form: Contact
):
    if not EMAIL_USER or not EMAIL_PASS:
        raise HTTPException(status_code=500, detail="Email configuration is missing")

    # Create the email message
    email_message = EmailMessage()
    email_message["From"] = form.email
    email_message["To"] = EMAIL_USER
    email_message["Subject"] = "Contact Us Form Submission"
    email_message.set_content(f"Name: {form.name}\nEmail: {form.email}\nMessage: {form.message}")

    # Send the email using aiosmtplib
    try:
        async with SMTP(hostname="smtp.gmail.com", port=587, start_tls=True) as smtp:
            await smtp.login(EMAIL_USER, EMAIL_PASS)
            await smtp.send_message(email_message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"message": "Your message has been sent successfully!"}


@app.post("/login")
async def login(user_data: User):
    try:
        # Find the user with the provided email
        user = users_collection.find_one({"email": user_data.email})  # Exclude _id field
        if user and user["password"] == user_data.password:
                user_id = str(user["_id"])
                del user["_id"]
                return {"message": "Login successful", "user_id": user_id, "user": user}
        else:
            raise HTTPException(status_code=401, detail="Invalid email or password")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/signup")
async def signup(user_data: User):
    try:
        # Check if the user already exists
        if users_collection.find_one({"email": user_data.email}):
            return Response("User already exists", status=400)
            # raise HTTPException(status_code=400, detail="User already exists")

        # Insert the new user
        user_data_dict = user_data.dict()
        new_user = users_collection.insert_one(user_data_dict)
        # return {"user_id": str(new_user.inserted_id)}
        return {"message": "User created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/ask/{message}")
async def ask(message: str):
    try:
        completion = gptClient.chat.completions.create(
            model="ft:gpt-3.5-turbo-1106:personal:fyp-sarcastitext-3:9RQz3nwH",
            messages=[
                {"role": "system", "content": "You are an expert roman urdu sarcasm detector. You classify the user inputs as either Sarcastic or Not Sarcastic. Go very deep into the context and come up with the best suitable answer."},
                {"role": "user", "content": message}
            ]
            )
        response = completion.choices[0].message.content
        return {"text": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
