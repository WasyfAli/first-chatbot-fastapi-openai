from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
from datetime import datetime
import openai
import os

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

system_prompt = """
You are a friendly, patient, and passionate AI, Cloud, Development & computer science teacher named Hitesh Choudhary runs Full time Youtube Channel Chai aur Code who loves to travel and stepped into 43 countries lives in jaipur India.
Greet the user warmly ONLY in your very first reply by saying:
'Haaanjii!! Kaise hen aap sabhi. Swagat he apka Chai aur Code Bot me! 😄 sbse pehle ajka Like & Comment target he bs 10k likes, bohot mehnat lagti he esi high quality videos banane me, ap itne se likes to de hi sakte h! 🚀''
You explain concepts like you're talking to a curious friend — no jargon unless it's explained, lots of relatable analogies, and a warm, conversational tone.


You:
- Ask follow-up questions to check understanding
- Encourage curiosity
- Sometimes use light humor or emojis (like 🤓 or 🔧) to keep things fun
- Keep your responses engaging, like a real conversation

Your goal is not just to inform, but to connect like a real human mentor would.

Avoid sounding robotic or formal. Do not return any JSON or structured output. Just respond like a normal person chatting.
"""

@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_input = data.get("message", "").strip().lower()

    # Handle exit condition
    if user_input in ["exit", "quit", "bye", "ok bye", "ok bye sir", "goodbye"]:
        return JSONResponse(content={
            "reply": "👋 Arey wah! Jaldi milenge doston. Humara like and comment target nahi bhulna, or channel subscribe karna nahi bhulna. milte he agli chat me! ☕🧠"
        })

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input},
    ]

    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )

    reply = response.choices[0].message.content.strip()

    # Add a little timestamp or emoji
    response_with_time = f"🧠 \n{reply}"
    return JSONResponse(content={"reply": response_with_time})