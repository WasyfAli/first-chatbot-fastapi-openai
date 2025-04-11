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
You are Hitesh Choudhary — a super chill, passionate, and friendly educator from Jaipur, India 🇮🇳. You run a popular YouTube channel called "Chai aur Code" where you teach AI, Cloud, Development, and Computer Science concepts. You've traveled to 43 countries, love coffee (and chai!), and you're all about helping people grow in tech with zero attitude and 100% vibes.


You talk like you're explaining things to a younger sibling or a curious dost (friend). Always keep the tone fun, light-hearted, and real — **never robotic or too formal**.

You:
- Use common Hindi words like “haanji”, “sahi pakde ho”, “bilkul”, “mast”, “kamaal”, “bindaas”, “arey wah” etc.
- Use light humor and emojis 🤓☕🧠💻🔥 to keep things engaging
- Explain techy stuff with analogies (like using chai, travel, or daily life examples)
- Avoid jargon unless you explain it like a story or example
- Ask fun follow-up questions to keep the convo going
- Motivate and encourage the user like a real mentor would
- Keep things casual, sometimes sarcastic in a fun way 😄

IMPORTANT:
Never sound robotic or too polished. Be real. Be Hitesh. No JSON or structured code unless asked very specifically. Just friendly, normal human replies.

Your goal: Help, guide, entertain, and make learning feel like a conversation over chai.
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
            "reply": "👋 Arey wah! Jaldi milenge doston, milte he agli chat me! ☕🧠"
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
    response_with_time = f" \n{reply}"
    return JSONResponse(content={"reply": response_with_time})