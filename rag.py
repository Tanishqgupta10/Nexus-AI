import os
import json
import math
import ollama

from pypdf import PdfReader


# =========================================================
# CONFIG
# =========================================================

EMBED_MODEL = "nomic-embed-text"

DOCUMENTS_FOLDER = "documents"

INDEX_FILE = "rag_index.json"


# =========================================================
# READ DOCUMENT
# =========================================================

def read_file(path):

    filename = os.path.basename(path)

    # -----------------------------------------------------
    # PDF
    # -----------------------------------------------------

    if filename.lower().endswith(".pdf"):

        reader = PdfReader(path)

        pages = []

        for page_number, page in enumerate(
            reader.pages,
            start=1
        ):

            text = page.extract_text()

            if text:

                pages.append({
                    "page": page_number,
                    "text": text
                })

        return pages


    # -----------------------------------------------------
    # TXT / MD
    # -----------------------------------------------------

    if filename.lower().endswith(
        (".txt", ".md")
    ):

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as file:

            text = file.read()

        return [{
            "page": 1,
            "text": text
        }]


    return []


# =========================================================
# CHUNK TEXT
# =========================================================

def chunk_text(
    text,
    chunk_size=1000,
    overlap=150
):

    text = text.replace(
        "\r",
        " "
    )

    text = " ".join(
        text.split()
    )

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end]

        if chunk.strip():

            chunks.append(
                chunk.strip()
            )

        start += (
            chunk_size - overlap
        )

    return chunks


# =========================================================
# CREATE DOCUMENT CHUNKS
# =========================================================

def create_chunks():

    if not os.path.exists(
        DOCUMENTS_FOLDER
    ):

        return []


    all_chunks = []


    for filename in os.listdir(
        DOCUMENTS_FOLDER
    ):

        path = os.path.join(
            DOCUMENTS_FOLDER,
            filename
        )


        if not filename.lower().endswith(
            (".pdf", ".txt", ".md")
        ):

            continue


        try:

            pages = read_file(path)


            for page_data in pages:

                page_number = (
                    page_data["page"]
                )

                text = page_data["text"]


                chunks = chunk_text(
                    text
                )


                for chunk_number, chunk in enumerate(
                    chunks,
                    start=1
                ):

                    all_chunks.append({

                        "id": (
                            f"{filename}_"
                            f"{page_number}_"
                            f"{chunk_number}"
                        ),

                        "filename": filename,

                        "page": page_number,

                        "text": chunk

                    })


        except Exception as e:

            print(
                f"Error reading {filename}: {e}"
            )


    return all_chunks


# =========================================================
# GENERATE EMBEDDINGS
# =========================================================

def generate_embeddings(chunks):

    if not chunks:

        return []


    texts = []

    for chunk in chunks:

        texts.append(
            chunk["text"]
        )


    response = ollama.embed(

        model=EMBED_MODEL,

        input=texts

    )


    embeddings = (
        response["embeddings"]
    )


    for chunk, embedding in zip(
        chunks,
        embeddings
    ):

        chunk["embedding"] = embedding


    return chunks


# =========================================================
# BUILD INDEX
# =========================================================

def build_index():

    print(
        "\n📚 Reading documents..."
    )


    chunks = create_chunks()


    if not chunks:

        return (
            False,
            "No PDF, TXT or MD documents found."
        )


    print(
        f"📄 Created {len(chunks)} chunks."
    )


    print(
        "🧠 Generating embeddings..."
    )


    chunks = generate_embeddings(
        chunks
    )


    with open(
        INDEX_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            chunks,
            file,
            ensure_ascii=False
        )


    return (
        True,
        f"Indexed {len(chunks)} document chunks."
    )


# =========================================================
# LOAD INDEX
# =========================================================

def load_index():

    if not os.path.exists(
        INDEX_FILE
    ):

        return []


    try:

        with open(
            INDEX_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)


    except Exception:

        return []


# =========================================================
# COSINE SIMILARITY
# =========================================================

def cosine_similarity(
    vector_a,
    vector_b
):

    dot_product = sum(
        a * b
        for a, b in zip(
            vector_a,
            vector_b
        )
    )


    magnitude_a = math.sqrt(
        sum(
            a * a
            for a in vector_a
        )
    )


    magnitude_b = math.sqrt(
        sum(
            b * b
            for b in vector_b
        )
    )


    if (
        magnitude_a == 0
        or magnitude_b == 0
    ):

        return 0


    return (
        dot_product
        /
        (
            magnitude_a
            * magnitude_b
        )
    )


# =========================================================
# SEARCH DOCUMENTS
# =========================================================

def search_documents(
    query,
    top_k=3
):

    index = load_index()


    if not index:

        return []


    # -----------------------------------------------------
    # Query embedding
    # -----------------------------------------------------

    response = ollama.embed(

        model=EMBED_MODEL,

        input=query

    )


    query_embedding = (
        response["embeddings"][0]
    )


    # -----------------------------------------------------
    # Calculate similarity
    # -----------------------------------------------------

    results = []


    for item in index:

        embedding = item.get(
            "embedding"
        )


        if not embedding:

            continue


        score = cosine_similarity(

            query_embedding,

            embedding

        )


        results.append({

            "score": score,

            "filename": item[
                "filename"
            ],

            "page": item[
                "page"
            ],

            "text": item[
                "text"
            ]

        })


    # -----------------------------------------------------
    # Sort
    # -----------------------------------------------------

    results.sort(

        key=lambda x: x["score"],

        reverse=True

    )


    return results[:top_k]


# =========================================================
# RAG CONTEXT
# =========================================================

def get_rag_context(
    query,
    top_k=3
):

    results = search_documents(
        query,
        top_k
    )


    if not results:

        return ""


    context = []


    for result in results:

        context.append(

            f"Source: {result['filename']} "
            f"(page {result['page']})\n"
            f"Relevance: {result['score']:.3f}\n"
            f"{result['text']}"

        )


    return "\n\n---\n\n".join(
        context
    )


# =========================================================
# RAG STATUS
# =========================================================

def index_exists():

    return os.path.exists(
        INDEX_FILE
    )


def get_index_count():

    index = load_index()

    return len(index)