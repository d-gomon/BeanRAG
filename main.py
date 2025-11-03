#https://docs.mistral.ai/capabilities/embeddings/rag_quickstart

import faiss
import json
import os
import numpy as np
from mistralai import Mistral
from dotenv import load_dotenv
from BeanRAG.utils import *

def main():
    #In this function, we want to allow the user to query a model
    #Then calculate the embedding using Mistral API
    #Then compare similarity (we can use euclidean distance as Mistral normalizes its embeddings)
    #Then attach query to user query indicating that it is supposed to find most relevant information about Labour & Health law from most similar entries
    #Then provide user the output
    
    #-----------Load Mistral API key--------------------#
    load_dotenv()
    MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
    if not MISTRAL_API_KEY:
        raise ValueError("No Mistral API key found. Set the MISTRAL_API_KEY environment variable in a .env file in the main directory.")

    #--------------Authenticate Mistral Model----------------#
    client = Mistral(api_key=MISTRAL_API_KEY)

    #---------------Load vector database---------------------#
    BeanRAG_VectorDB = faiss.read_index("BeanRAG_VectorDB.faiss")
    # Also load the .json file, to get context
    # Pad naar je JSON-bestand
    json_path = "structured_chunks.json"

    # JSON-bestand inlezen, om relevante metadata ook te returnen
    with open(json_path, "r", encoding="utf-8") as f:
        chunks = json.load(f)
    


    #----------------Let user input query & embed--------------------#
    query = input('Hallo hardwerkende Boon, welk werkprobleem zit jij vandaag mee? \n')
    query_embedding = get_text_embedding(input=query, client=client)

    #-----------Find relevant information from query---------------------#
    D, I = BeanRAG_VectorDB.search(np.array([query_embedding]), k=3) # distance, index
    retrieved_chunks = [chunks[i] for i in I.tolist()[0]]

    #----------Prompt the LLM to return most relevant info------------------#

    prompt = f"""
    Jij bent een assistent voor een adviseur arbeid & gezondheid.
    Jouw doel is om precieze informatie te geven over wet en regelgeving wat betreft arbeid & gezondheidswetgeving en de aanpak van verzuim.
    Hieronder vind je informatie die relevant is voor de gestelde vraag.
    ---------------------
    {retrieved_chunks}
    ---------------------
    Gegeven deze informatie en niet voorgaande kennis, antwoord de volgende vraag.
    Vraag: {query}
    """

    answer = run_mistral(user_message=prompt, client=client)
    print(answer, "\n")


main()
    