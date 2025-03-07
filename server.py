from openai import OpenAI
from pathlib import Path

openai_api_key = "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"

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

# notes