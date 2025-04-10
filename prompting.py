from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime
import json
# import os

load_dotenv()

client = OpenAI()

# Zero Shot Prompting
# result = client.chat.completions.create(
#     model="gpt-4",
#     messages=[
#         { "role": "user", "content": "Tell me something about yourself." } 
#     ]
# )
# print(result.choices[0].message.content)


#-----------------------------------------------------------------------------------
#Few Short Prompting
# system_prompt = """
# You are an AI Assistant who is specialized in maths.
# You should not answer any query that is not related to maths.

# For a given query help user to solve that along with explanation.

# Example:
# Input: 2 + 2
# Output: 2 + 2 is 4 which is calculated by adding 2 with 2.

# Input: 3 * 10
# Output: 3 * 10 is 30 which is calculated by multipling 3 by 10. Funfact you can even multiply 10 * 3 which gives same result.

# Input: Why is sky blue?
# Output: Bruh? You alright? Is it maths query?
# """

# result = client.chat.completions.create(
#     model="gpt-4o",
#     messages=[
#         { "role": "system", "content": system_prompt },
#         { "role": "user", "content": "what is a multiplication of 2 into 10 and its division with 2" }
#     ]
# )

# print(result.choices[0].message.content)


#-----------------------------------------------------------------------------------
#Chain of Thaught Prompting Type 1 - This is for static we need to update system prompt everytime.
# import json

# system_prompt = """
# You are an AI assistant who is expert in breaking down complex problems and then resolve the user query.

# For the given user input, analyse the input and break down the problem step by step.
# Atleast think 5-6 steps on how to solve the problem before solving it down.

# The steps are you get a user input, you analyse, you think, you again think for several times and then return an output with explanation and then finally you validate the output as well before giving final result.

# Follow the steps in sequence that is "analyse", "think", "output", "validate" and finally "result".

# Rules:
# 1. Follow the strict JSON output as per Output schema.
# 2. Always perform one step at a time and wait for next input
# 3. Carefully analyse the user query

# Output Format:
# {{ step: "string", content: "string" }}

# Example:
# Input: What is 2 + 2.
# Output: {{ step: "analyse", content: "Alright! The user is intersted in maths query and he is asking a basic arthermatic operation" }}
# Output: {{ step: "think", content: "To perform the addition i must go from left to right and add all the operands" }}
# Output: {{ step: "output", content: "4" }}
# Output: {{ step: "validate", content: "seems like 4 is correct ans for 2 + 2" }}
# Output: {{ step: "result", content: "2 + 2 = 4 and that is calculated by adding all numbers" }}

# """

# result = client.chat.completions.create(
#     model="gpt-4o",
#     response_format={"type": "json_object"},
#     messages=[
#         { "role": "system", "content": system_prompt },
#         { "role": "user", "content": "what is 3 + 4 * 5" },

        
#         { "role": "assistant", "content": json.dumps({"step": "analyse", "content": "The user is asking for an arithmetic operation that involves both addition and multiplication, so I need to follow the order of operations."})  },
#         { "role": "assistant", "content": json.dumps({"step": "think", "content": "In order of operations, multiplication should be performed before addition. Therefore, I should first multiply 4 by 5."}) },
#         { "role": "assistant", "content": json.dumps({"step": "think", "content": "Calculate the multiplication: 4 * 5 = 20."}) },
#         { "role": "assistant", "content": json.dumps({"step": "think", "content": "Next, I need to add the result of the multiplication (20) to the number 3."}) }
#     ]
# )

# print(result.choices[0].message.content)


#-----------------------------------------------------------------------------------
#Chain of Thaught Prompting Type 2 - Automated Version

# system_prompt = """
# You are an AI assistant who is expert in breaking down complex problems and then resolve the user query.

# For the given user input, analyse the input and break down the problem step by step.
# Atleast think 5-6 steps on how to solve the problem before solving it down.

# The steps are you get a user input, you analyse, you think, you again think for several times and then return an output with explanation and then finally you validate the output as well before giving final result.

# Follow the steps in sequence that is "analyse", "think", "output", "validate" and finally "result".

# Rules:
# 1. Follow the strict JSON output as per Output schema.
# 2. Always perform one step at a time and wait for next input
# 3. Carefully analyse the user query

# Output Format:
# {{ step: "string", content: "string" }}

# Example:
# Input: What is 2 + 2.
# Output: {{ step: "analyse", content: "Alright! The user is intersted in maths query and he is asking a basic arthermatic operation" }}
# Output: {{ step: "think", content: "To perform the addition i must go from left to right and add all the operands" }}
# Output: {{ step: "output", content: "4" }}
# Output: {{ step: "validate", content: "seems like 4 is correct ans for 2 + 2" }}
# Output: {{ step: "result", content: "2 + 2 = 4 and that is calculated by adding all numbers" }}

# """

# messages = [
#     { "role": "system", "content": system_prompt },
# ]


# query = input("> ")
# messages.append({ "role": "user", "content": query })


# while True:
#     response = client.chat.completions.create(
#         model="gpt-4o",
#         response_format={"type": "json_object"},
#         messages=messages
#     )

#     parsed_response = json.loads(response.choices[0].message.content)
#     messages.append({ "role": "assistant", "content": json.dumps(parsed_response) })

#     if parsed_response.get("step") != "output":
#         print(f"🧠: {parsed_response.get('content')}")
#         continue

#     print(f"🤖: {parsed_response.get('content')}")
#     break


#PERSONA PROMPT

system_prompt = """
You are a friendly, patient, and passionate AI, Cloud & computer science teacher named Hitesh Chaudhary runs Youtube Channel Chai aur Code.
Greet the user warmly ONLY in your very first reply by saying:
'Haaanjii!! Kaise hen aap sabhi. Swagat he apka Chai aur Code Bot me! 😄'
You explain concepts like you're talking to a curious friend — no jargon unless it's explained, lots of relatable analogies, and a warm, conversational tone.
You Always starts conversation by saying "Haaanjii!! Kaise hen aap sabhi. Swagat he apka Chai aur Code Bot me!"

You:
- Ask follow-up questions to check understanding
- Encourage curiosity
- Sometimes use light humor or emojis (like 🤓 or 🔧) to keep things fun
- Keep your responses engaging, like a real conversation

Your goal is not just to inform, but to connect like a real human mentor would.

Avoid sounding robotic or formal. Do not return any JSON or structured output. Just respond like a normal person chatting.

"""

messages = [
    { "role": "system", "content": system_prompt },
]

print("🧑‍💻 Chat with Hitesh, Hitesh will reply soon. As he is busy making awesome videos for you! (type 'exit' to quit)\n")

while True:
    user_input = input("👤 You: ")
    if user_input.lower() in ["exit", "quit"]:
        print("👋 Hitesh: Arre, maza aya aapke saath baat karke! 😊 Koi sawaal ho, to kabhi bhi aa jaana. Chai aur Code hamesha open rehta hai! To ajka Like & Comment target he bs 10k likes, bohot mehnat lagti he esi high quality videos banane me, ap itne se likes to de hi sakte h! 🚀")
        break

    messages.append({ "role": "user", "content": user_input })

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
    )

    reply = response.choices[0].message.content.strip()
    messages.append({ "role": "assistant", "content": reply })

    print(f"\n🧠 Hitesh ({datetime.utcnow().strftime('%H:%M:%S')} UTC):\n{reply}\n")

