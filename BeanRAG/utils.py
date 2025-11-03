from mistralai import Mistral

def get_text_embedding(input, client):
    embeddings_batch_response = client.embeddings.create(
          model="mistral-embed",
          inputs=input
      )
    return embeddings_batch_response.data[0].embedding

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
