from typing import Any, Dict
from mini_local_rag.pipeline import Step
from mini_local_rag.vector_store import VectorStore


class RetrieveFromVectorStoreStep(Step):
    """
    A pipeline step that retrieves documents from a vector store based on a given embedding.

    This step uses a vector store (e.g., `VectorStore`) to query and retrieve documents that are 
    most similar to the provided embedding. The resulting documents are stored in the context under 
    the key `"documents"`.

    Attributes:
        label (str): The label identifying this step ("Document Retrieval").
        vector_store (VectorStore): The vector store instance used to perform the document retrieval based on the embedding.
    """
    label = "Document Retrieval"
    def __init__(self,vector_store:VectorStore):
        """
        Initializes the step with the provided vector store.

        Args:
            vector_store (VectorStore): The vector store instance used for querying and retrieving documents based on embeddings.
        """
        self.vector_store= vector_store

    def execute(self, context: Dict[str, Any]) -> None:
        """
        Retrieves documents from the vector store based on the provided embedding.

        The method queries the vector store with the provided embedding (which is stored in the context),
        retrieves the most relevant documents, and stores them in the context under the key `"documents"`.

        Args:
            context (Dict[str, Any]): The context containing the embedding that will be used to query the vector store.

        Updates:
            context["documents"]: A list of documents retrieved from the vector store based on the embedding.
        """
        embedding : list[float] = context["embedding"]
        context["documents"] = self.vector_store.query(embedding)