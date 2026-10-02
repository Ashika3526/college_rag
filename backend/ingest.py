import os
import fitz
import chromadb

from sentence_transformers import SentenceTransformer


# ==================================================
# Paths
# ==================================================

BASE_DIR = os.path.dirname(__file__)

DATA_PATH = os.path.join(
    BASE_DIR,
    "data"
)

CHROMA_PATH = os.path.join(
    BASE_DIR,
    "chroma_db"
)

COLLECTION_NAME = "college_knowledge"


# ==================================================
# Load embedding model
# ==================================================

print("Loading embedding model...")

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# ==================================================
# Find all PDF files
# ==================================================

def get_pdf_files():

    pdf_files = []

    for filename in os.listdir(DATA_PATH):

        if filename.lower().endswith(".pdf"):

            pdf_files.append(
                os.path.join(
                    DATA_PATH,
                    filename
                )
            )

    return pdf_files


# ==================================================
# Extract text from all PDFs
# ==================================================

def extract_pdfs():

    pdf_files = get_pdf_files()

    if not pdf_files:

        raise FileNotFoundError(
            "No PDF files found in backend/data/"
        )

    all_pages = []

    for pdf_path in pdf_files:

        filename = os.path.basename(
            pdf_path
        )

        print(
            f"\nReading: {filename}"
        )

        document = fitz.open(pdf_path)

        for page_number, page in enumerate(
            document
        ):

            text = page.get_text()

            if text.strip():

                all_pages.append({

                    "text": text,

                    "page": page_number + 1,

                    "source": filename
                })

        document.close()

    return all_pages


# ==================================================
# Create chunks
# ==================================================

def create_chunks(pages):

    chunks = []

    chunk_size = 800

    overlap = 100


    for page in pages:

        text = page["text"]

        start = 0


        while start < len(text):

            end = start + chunk_size

            chunk_text = text[start:end]


            if chunk_text.strip():

                chunks.append({

                    "text": chunk_text,

                    "page": page["page"],

                    "source": page["source"]

                })


            start = end - overlap


    return chunks


# ==================================================
# Store in ChromaDB
# ==================================================

def store_in_chromadb(chunks):

    print(
        "\nCreating ChromaDB..."
    )

    client = chromadb.PersistentClient(
        path=CHROMA_PATH
    )


    # Remove old collection

    try:

        client.delete_collection(
            COLLECTION_NAME
        )

        print(
            "Old collection deleted."
        )

    except Exception:

        pass


    # Create new collection

    collection = client.create_collection(
        name=COLLECTION_NAME
    )


    # Get text

    texts = [

        chunk["text"]

        for chunk in chunks

    ]


    # Create embeddings

    print(
        "Creating embeddings..."
    )

    embeddings = embedding_model.encode(
        texts,
        show_progress_bar=True
    ).tolist()


    # IDs

    ids = [

        f"chunk_{i}"

        for i in range(len(chunks))

    ]


    # Metadata

    metadatas = [

        {
            "page": chunk["page"],

            "source": chunk["source"]
        }

        for chunk in chunks

    ]


    # Add to ChromaDB

    collection.add(

        ids=ids,

        documents=texts,

        embeddings=embeddings,

        metadatas=metadatas
    )


    print(
        f"\nStored {len(chunks)} chunks."
    )


# ==================================================
# Main
# ==================================================

if __name__ == "__main__":

    print(
        "\n=============================="
    )

    print(
        "COLLEGE RAG INGESTION"
    )

    print(
        "=============================="
    )


    # Find PDFs

    pdf_files = get_pdf_files()


    print(
        f"\nFound {len(pdf_files)} PDF files:"
    )


    for pdf in pdf_files:

        print(
            " -",
            os.path.basename(pdf)
        )


    # Extract

    pages = extract_pdfs()


    print(
        f"\nTotal pages: {len(pages)}"
    )


    # Create chunks

    chunks = create_chunks(pages)


    print(
        f"Total chunks: {len(chunks)}"
    )


    # Store

    store_in_chromadb(chunks)


    print(
        "\n=============================="
    )

    print(
        "RAG KNOWLEDGE BASE CREATED"
    )

    print(
        "=============================="
    )