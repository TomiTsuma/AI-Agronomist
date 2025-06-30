from functools import lru_cache

@lru_cache(maxsize=128)
def cached_retrieval(query: str):
    # Could call your context retrieval function
    from app.services.retrieval import retrieve_context
    return retrieve_context(query)
