import os

import chromadb

from openai import OpenAI

from sentence_transformers import SentenceTransformer

from config import GROQ_API_KEY, GROQ_MODEL


# --------------------------------------------------
# ChromaDB path
# --------------------------------------------------

CHROMA_PATH = os.path.join(
    os.path.dirname(__file__),
    "chroma_db"
)

COLLECTION_NAME = "college_knowledge"


# --------------------------------------------------
# Groq client
# --------------------------------------------------

client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)


# --------------------------------------------------
# Embedding model
# --------------------------------------------------

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# --------------------------------------------------
# ChromaDB
# --------------------------------------------------

chroma_client = chromadb.PersistentClient(
    path=CHROMA_PATH
)

collection = chroma_client.get_collection(
    name=COLLECTION_NAME
)


# --------------------------------------------------
# Ask question
# --------------------------------------------------

def ask_question(question):

    # ----------------------------------------------
    # Convert question into embedding
    # ----------------------------------------------

    question_embedding = embedding_model.encode(
        question
    ).tolist()


    # ----------------------------------------------
    # Search ChromaDB
    # ----------------------------------------------

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=5
    )


    documents = results["documents"][0]

    metadatas = results["metadatas"][0]


    # ----------------------------------------------
    # Build context
    # ----------------------------------------------

    context_parts = []

    for document, metadata in zip(
        documents,
        metadatas
    ):

        page = metadata.get(
            "page",
            "Unknown"
        )

        context_parts.append(
            f"[Page {page}]\n{document}"
        )


    context = "\n\n".join(
        context_parts
    )


    # ----------------------------------------------
    # Prompt
    # ----------------------------------------------

    prompt = f"""
You are a College Knowledge Assistant.

Answer the user's question using ONLY
the information provided in the context.

Do not use outside knowledge.

If the answer cannot be found in the
provided context, say:

"I could not find this information
in the college document."

Keep the answer clear and concise.

Context:
-------------------------
{context}
-------------------------

Question:
{question}

Answer:
"""


    # ----------------------------------------------
    # Send to Groq
    # ----------------------------------------------

    response = client.chat.completions.create(

        model=GROQ_MODEL,

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0
    )


    answer = response.choices[0].message.content


    # ----------------------------------------------
    # Sources
    # ----------------------------------------------

    sources = []

    for metadata in metadatas:

        page = metadata.get(
            "page",
            "Unknown"
        )

        if page not in sources:

            sources.append(page)


    return {
        "answer": answer,
        "sources": sources
    }