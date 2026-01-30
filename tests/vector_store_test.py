import pytest
from langchain_core.documents import Document
from mini_local_rag.vector_store import VectorStore


def __clear(store:VectorStore):
    """
    Clears data from vector store for testing
    """
    collection = store._collection
    results = collection.get()
    ids = results.get("ids",[])

    if len(ids)>0 :collection.delete(ids=ids)

@pytest.fixture
def documents():
    """Fixture to set up docs to test."""

    return [
            Document(page_content = "Content of doc 1", metadata={"id": "1", "embeddings": [0.1, 0.2], "headers": "h1", "file_path": "/path/to/doc1"}),
            Document(page_content = "Content of doc 2", metadata={"id": "2", "embeddings": [0.2, 0.3], "headers": "h2", "file_path": "/path/to/doc2"}),
            Document(page_content = "Content of doc 3", metadata={"id": "3", "embeddings": [0.3, 0.4], "headers": "h3", "file_path": "/path/to/doc3"}),
    ]

@pytest.fixture
def vector_store():
    """Fixture to set up and tear down VectorStore instance."""
    # Create the VectorStore instance
    store = VectorStore()

    # Clean up any previous data by clearing the store before each test
    __clear(store)  # Adjust based on how clearing is done in your store

    # Return the vector store instance for use in tests
    return store

def test_vector_store(vector_store,documents):
    """
    Test that documents are saved correctly to the VectorStore.
    """

    # Act: Save documents to the vector store
    vector_store.saveAll(documents)

    # Assert: Check if the documents were saved by querying the document paths
    stored_docs = vector_store.listDocuments()
    assert len(stored_docs) == 3, f"Expected 3 documents, but got {len(stored_docs)}"
    assert "/path/to/doc1" in stored_docs, "Document 1 was not saved correctly."
    assert "/path/to/doc2" in stored_docs, "Document 2 was not saved correctly."
    assert "/path/to/doc3" in stored_docs, "Document 3 was not saved correctly."

    embedding = [0.5, 0.2]
    results = vector_store.query(embedding, top_k=3)

    # Assert: Check that the number of results is correct and they are similar to the query
    assert len(results) == 3, f"Expected 3 results, but got {len(results)}"
    for result in results:
        assert isinstance(result, Document), f"Expected a Document object, but got {type(result)}"

    __clear(vector_store)  

    # Assert: Verify that the store is empty after cleanup
    stored_docs = vector_store.listDocuments()
    assert len(stored_docs) == 0, f"Expected no documents, but got {len(stored_docs)}"

