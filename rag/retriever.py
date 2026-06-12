from rag.loader import load_manuals

def retrieve_context(query):
    docs = load_manuals()
    return docs[:1500]  # limit