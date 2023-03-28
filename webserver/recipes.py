import os
import openai

openai.api_key = "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"

comletition = openai.ChatCompletion.create(
    model = "gpt-3.5-turbo",
    messages = [
        {
            "role": "user", "content": "Tell me recipes with the following ingredients:"
        }
    ]
)

print(comletition.choices[0].messages.content)