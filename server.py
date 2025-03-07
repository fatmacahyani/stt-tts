from openai import OpenAI
from pathlib import Path
from dotenv import load_dotenv # type: ignore
import os

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=openai_api_key)

systemprompt ="You are a helpful assistant for your friend named Yani"
# systemprompt = "You are Service Robot named RISA. This service robot is an advanced, autonomous assistant designed to enhance the experience of students, staff, and visitors at ITS campus. Equipped with cutting-edge technology, the robot provides information, guidance, and interactive services"

while True:
    user_input = input("You: ")
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": systemprompt},
            {"role": "user", "content": user_input}
        ],
        stream=False
    )
    print(response.choices[0].message.content)

# notes xxx