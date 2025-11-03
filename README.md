# BeanRAG - A Retrieval Augmented Generator for the Bean
**!!**

**Om dit pakket te gebruiken moet je een .env file in de main directory plaatsen met daarin MISTRAL_API_KEY=jeAPIKEY. Je kunt een gratis API key aanvragen in je [Mistral AI Studio](https://console.mistral.ai/home) account**

**!!**


In dit softwarepakket programmeren we een RAG zodat de Bean allemaal informatie kan opzoeken over Ziekte & Arbeids wetgeving. 

Een RAG zal de Bean toestaan om een verzameling documenten snel te doorzoeken door een query te sturen naar een LLM. Deze query wordt dan vergeleken op similarity met de data die we in de database toegevoegd hebben.

Dit process werkt in een paar delen:

## Deel 1: Input data processen - `DataProcessing.ipynb`

In een folder genaamd `Documents/` slaan we een aparte folder op voor iedere informatiebron die we willen gebruiken voor de RAG. 

Iedere informatiebron willen we namelijk op een verschillende manier chunken (opsplitsen in kleine deeltjes), afhankelijk van de inhoud. Wetgevingsdocumenten willen we bijvoorbeeld opsplitsen mbv hoofdstukken en artikels. Andere documenten weer op een andere manier. Dit wordt gedaan door voor elke folder een andere chunker(-functie) te gebruiken. Welke functie we gebruiken voor welke folder kun je aanpassen in de dictionary `FOLDER_TO_CHUNKER`. 

Eens klaar, worden de chunks van alle informatiebronnen opgeslagen in een variabele genaamd `structured_chunks.json`. Deze file bevat allemaal dictionaries met tenminste het `'text'` en `'directory'` veld, en mogelijk nog andere velden zoals `'Hoofdstuk'` etc.

## Deel 2: Embedden van de chunks.

Eens de documenten gechunked zijn, willen we iedere chunk representeren in een lager dimensionale vector space, zodat we snel door de chunks heen kunnen zoeken voor relevante informatie.

Er zijn verschillende embedders die we kunnen gebruiken. Omdat de documenten veelal in het Nederlands zijn, heb ik ervoor gekozen om het Mistral-Embed model te gebruiken. Hiermee hoeven we dan ook geen local compute te doen. Als we in de toekomst het allemaal lokaal willen houden, zouden we kunnen overwegen om via ollama een of ander (kleiner) model te gebruiken voor de embeddings. Ik denk echter dat je daar wel wat efficientie mee verliest. Aangezien je niet zo vaak de dataset hoeft te updaten, is het niet zo een probleem om zo nu en dan een niet lokaal model aan te roepen.

Eens we de embeddings berekend hebben, slaan we deze op in een [`faiss`](https://faiss.ai/) vector database. Dit is een speciaal soort database wat toestaat om snel nearest neighbours te vinden van een vector. We gebruiken deze vector database omdat we snel op similarity willen zoeken t.o.v. onze query. De database wordt opgeslagen onder de naam `BeanRAG_VectorDB.faiss`.


## Deel 3: Query + Opzoeken van relevante info.

Nu willen we natuurlijk een query sturen naar Mistral en een antwoord krijgen gebaseerd op de informatie in onze database. Eens de query getyped is door de Bean wordt deze embedded door hetzelfde model en daarna zoeken we de meest similar elementen op in de vector database. Mistral krijgt dan de volgende prompt, waarbij {query} staat voor de vraag en {retrieved_chunks} voor de relevante data:


#### Prompt voor AI assistent
Jij bent een assistent voor een adviseur arbeid & gezondheid.
Jouw doel is om precieze informatie te geven over wet en regelgeving wat betreft arbeid & gezondheidswetgeving en de aanpak van verzuim.
Hieronder vind je informatie die relevant is voor de gestelde vraag.

{retrieved_chunks}

Gegeven deze informatie en niet voorgaande kennis, antwoord de volgende vraag.
Vraag: 

{query}
