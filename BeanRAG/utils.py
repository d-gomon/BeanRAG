from mistralai import Mistral
from sentence_transformers import SentenceTransformer
import os
from dotenv import load_dotenv, set_key
import pickle

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




def setup_env():
    env_path = ".env"
    load_dotenv(env_path)
    MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
    if not MISTRAL_API_KEY:
        MISTRAL_API_KEY = input("Geef je Mistral API key: ")
        with open(env_path, "w") as f:
            f.write(f"MISTRAL_API_KEY={MISTRAL_API_KEY}\n")
        os.environ["MISTRAL_API_KEY"] = MISTRAL_API_KEY
    return MISTRAL_API_KEY


def load_from_pickle(filename):
    with open(filename, "rb") as file:
        return pickle.load(file)