from typing import Any, Dict
from mini_local_rag.pipeline import Step
from mini_local_rag.vector_store import VectorStore


class SearchExistingDocumentsStep(Step):
    """
    A pipeline step that searches for documents in a vector store.

    This step queries the vector store to retrieve the list of documents and stores
    the result in the provided context.

    Attributes:
        label (str): A label identifying this step ("Searching vector store for documents").
        vector_store (VectorStore): The vector store instance used to retrieve documents.

    Methods:
        execute(context: Dict[str, Any]) -> None:
            Executes the step by searching the vector store for documents and 
            storing the result in the context.
    """
    label = "Searching vector store for documents"
    def __init__(self,vector_store:VectorStore):
        """
        Initializes the step with the given vector store.

        Args:
            vector_store (VectorStore): The vector store instance used to search for documents.
        """
        self.vector_store=vector_store

    def execute(self, context: Dict[str, Any]) -> None:
        """
        Executes the document search step.

        Queries the vector store for a list of documents and stores the result 
        in the context under the 'documents' key.

        Args:
            context (Dict[str, Any]): The context containing shared data for the pipeline.

        Updates:
            context['documents'] (List[Document]): The list of documents retrieved from the vector store.
        """
        context['documents'] =self.vector_store.listDocuments()