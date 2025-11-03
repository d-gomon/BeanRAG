from mistralai import Mistral
from sentence_transformers import SentenceTransformer

def get_text_embedding(input, model):
    return model.encode_query(input)

def run_mistral(user_message, client, model="mistral-large-latest"):
    messages = [
        {
            "role": "user", "content": user_message
        }
    ]
    chat_response = client.chat.complete(
        model=model,
        messages=messages
    )
    return (chat_response.choices[0].message.content)
