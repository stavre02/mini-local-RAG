
from langchain_core.documents import Document
from mini_local_rag.tf_idf_retriever import CustomTFIDFRetriever
import pytest


@pytest.fixture
def retriever():
    documents = [Document(page_content="Document {i}: This is the content of document {i}.") for i in range(10)]
    return CustomTFIDFRetriever.from_documents(documents=documents)

    

def test_retriever_top_k(retriever):
    docs =retriever.invoke("This is the content of document")

    assert len(docs) == retriever.k, "Retriever must return 3 results to change "