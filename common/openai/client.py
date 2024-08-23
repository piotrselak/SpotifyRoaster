from django.conf import settings
from openai import OpenAI
from openai.types.chat import ChatCompletionMessage

client = OpenAI(
    organization=settings.OPENAI_ORG_ID,
    project=settings.OPENAI_PROJECT_ID,
    api_key=settings.OPENAI_SECRET
)

def generate_roast(system_message: str, user_message:str) -> ChatCompletionMessage:
    completion = client.chat.completions.create(model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_message},
            {
                "role": "user",
                "content": user_message
            }
        ]
    )

    return completion.choices[0].message # TODO maybe parse all choices? idk