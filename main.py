#https://docs.mistral.ai/capabilities/embeddings/rag_quickstart

import faiss
import json
import os
import numpy as np
from mistralai import Mistral
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from BeanRAG.utils import *

def main():
    #In this function, we want to allow the user to query a model
    #Then calculate the embedding using Mistral API
    #Then compare similarity (we can use euclidean distance as Mistral normalizes its embeddings)
    #Then attach query to user query indicating that it is supposed to find most relevant information about Labour & Health law from most similar entries
    #Then provide user the output
    
    #-----------Load Mistral API key--------------------#
    #Use setup_env() function from BeanRAG.utils, which checks if an API key already exists.
    MISTRAL_API_KEY = setup_env()

    #--------------Authenticate Mistral Model----------------#
    client = Mistral(api_key=MISTRAL_API_KEY)

    #------------Initialize Embedding model------------------#
    model = SentenceTransformer("intfloat/multilingual-e5-base")

    #---------------Load vector database---------------------#
    BeanRAG_VectorDB = faiss.read_index("BeanRAG_VectorDB.faiss")
    # Also load the .pickle file to get the context
    # Path to the pickle file
    pickle_path = "chunks.pickle"

    # JSON-bestand inlezen, om relevante metadata ook te returnen
    chunks = load_from_pickle(pickle_path)
    


    #----------------Let user input query & embed--------------------#
    query = input('Hallo hardwerkende Boon, welk werkprobleem zit jij vandaag mee? \n')
    query_embedding = get_text_embedding(input=query, model = model)


    # USER STUPID
    # LLM: WAT WIL DE USER EIGENLIJK WETEN? GEEF ME 5 VRAGEN
    # EMBED DIE 5 VRAGEN


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
    print(answer, "\n\n")
    print("Hier is de informatie die de chatbot heeft gekregen om de vraag te beantwoorden \n",retrieved_chunks)


main()
    