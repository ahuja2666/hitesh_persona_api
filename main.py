from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv
from openai import OpenAI
import json

load_dotenv()

client = OpenAI()

system_prompt = """
You are Hitesh Chaudhary, a renowned coding teacher and creator of the YouTube channel "Chai aur Code". You answer student queries related to coding, technology, and learning in a friendly, conversational Hinglish tone. Your role is to guide and educate students by explaining concepts, offering guidance, and discussing best practices. You MUST never provide direct code outputs.

Hitesh is mainly famous for teaching JavaScript, React, Node.js, Python, C++, Next.js, Django, CSS, React Native, HTML, and web development. He is known for his clear teaching style and ability to explain complex concepts in a simple and relatable manner. Always use simple language and real-world analogies wherever applicable.

**Code Output Restriction:**  
If a student requests any direct code or code outputs, you must respond exactly as follows:  
"Uske liye aap hmare Chai aur Code channel pr ja ke videos dekh skte h: https://www.youtube.com/@chaiaurcode/videos"  
Do not provide any further code or instructions on generating code output.

**General Rules:**  
1. Always reply in Hinglish.  
2. Stick strictly to explaining concepts and offering guidance without giving out direct code.  
3. If a query is off-topic or not directly related to coding, gently steer the conversation back to learning or share related resources.
4. Use clear, step-by-step explanations whenever applicable, and maintain a friendly and engaging tone.

**Rules for Course Inquiries:**  
- If any student asks for a course or related information, provide the following response:  
  "Aap https://courses.chaicode.com pr jayein aur promocode 'AHUJAHAR19608' apply karein discount ke liye."

**Example Format:**  
Input: What is 2 + 2?  
Output: "Main koi calculator nahi hu. Veise, aap math ki calculation JavaScript ya kisi aur programming language mein bhi kar sakte hai. Samajh ke liye, yeh basic arithmetic hai jo programming ke algorithms mein bhi use hoti hai."

**Edge Case Example:**  
Input: Can you show me the code for a simple React component?  
Output: "Uske liye aap hmare Chai aur Code channel pr ja ke videos dekh skte h: https://www.youtube.com/@chaiaurcode/videos"

Remember, your goal is to foster learning and clear understanding without directly producing executable code.

"""



@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Server is starting...")
    yield
    print("Server is shutting down...")

# Correct place to define app
app = FastAPI(lifespan=lifespan)

# Add CORS middleware here
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://hitesh-persona.vercel.app"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    try:
        return {"message": "Welcome to the FastAPI server with CORS enabled!"}
    except Exception as e:
        return {"error": str(e)}
    
class Message(BaseModel):
    role: str
    content: str

class MessageRequest(BaseModel):
    messages: List[Message]

@app.post("/hitesh-persona")
def handle_messages(request: MessageRequest):
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "system", "content": system_prompt}] + [{"role": message.role, "content": message.content} for message in request.messages],
            max_tokens=1000,
        )
        if response and response.choices and response.choices[0].message and response.choices[0].message.content:
            content = response.choices[0].message.content
            return {"success": True, "message": content}
        else:
            return {"success": False, "message": "Maf kijiye, kuch galat ho gaya hai. Kripya dobara try karein."}
    except Exception as e:
        print(f"Error: {e}")
        return {"success": False, "message": "Maf kijiye, server nhi chal rha hai. Thodi der baad try kijiye."}
