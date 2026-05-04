from src.document_loader_manager import DocumentLoaderManager
# from openai_embedding_manager import EmbeddingManager
from src.huggingface_embedding_manager import HuggingFaceEmbeddingManager

def ingest_file(dir_path):
    print("Hello from ingestion-server!")
    dlm = DocumentLoaderManager(dir_path)
    oss_embedding_model_name = "sentence-transformers/all-MiniLM-L6-v2"
    hg_manager = HuggingFaceEmbeddingManager(oss_embedding_model_name)
    # em = EmbeddingManager("text-embedding-3-small")
    alldocs = dlm.load_document()

    print(f"\n\n\nLoaded {len(alldocs)} documents from directory: {dir_path}")
    chunks = dlm.split_into_chunks(alldocs)
    print(f"Split into {len(chunks)} chunks.")
    global vs
    vs = hg_manager.create_embedding(chunks)
    

def query_embedding(query):
    # query = "Who was ashoka?"
    # lexical + semantic search = contextual search
    # results = vs.similarity_search(query, k=4)

    retriever = vs.as_retriever(search_kwargs={"k": 4})

    results = retriever.invoke(query)

    return results

