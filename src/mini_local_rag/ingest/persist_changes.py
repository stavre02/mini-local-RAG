
from typing import Any, Dict
from langchain_core.documents import Document

from mini_local_rag.pipeline import Step
from mini_local_rag.vector_store import VectorStore


class PersistChangesStep(Step):
    """
    A pipeline step that persists changes to a vector database by saving documents.

    Attributes:
        label (str): The label identifying this step ("Persisting changes to vector db").
        vector_store (VectorStore): The vector store instance responsible for saving documents.
    """
    label = "Persisting changes to vector db"
    def __init__(self,vector_store:VectorStore):
        """
        Initializes the step with a vector store to persist documents.

        Args:
            vector_store (VectorStore): The vector store where the documents will be saved.
        """
        self.vector_store = vector_store
    def execute(self, context: Dict[str, Any]) -> None:
        """
        Persists the documents in the context to the vector database.

        The method retrieves the documents from the pipeline context and saves them to the vector store.

        Args:
            context (Dict[str, Any]): The context containing the documents to be persisted.

        Updates:
            None: This step directly modifies the vector store with the provided documents.
        """
        documents: list[Document] = context["documents"]        
        self.vector_store.saveAll(documents)