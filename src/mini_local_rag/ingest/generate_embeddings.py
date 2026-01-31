from typing import Any, Dict
from langchain_core.documents import Document

from mini_local_rag.config import Config
from mini_local_rag.embedder import Embedder, Qwen3Embedder
from mini_local_rag.pipeline import Step


class GenerateEmbeddingsStep(Step):
    label = "Embedding generation"
    """
    A pipeline step that generates embeddings for documents using a specified embedder model.

    This step uses an embedder (such as `Qwen3Embedder`) to create embeddings for the provided question 
    and stores the resulting embedding in the context. The embedder is passed as an argument during 
    the initialization of the step.

    Attributes:
        label (str): The label identifying this step ("Embedding generation").
        embedder (Embedder): The embedder instance used to generate embeddings for the question. 
                              The embedder model is passed during initialization.
    """
    def __init__(self,embedder:Embedder):
        """
        Initializes the step with the provided embedder.

        Args:
            embedder (Embedder): The embedder instance used to generate embeddings for the question.
        """
        self.embedder = embedder
    def execute(self, context: Dict[str, Any]) -> None:
        """
        Generates embeddings for each document in the context and stores them in the document's metadata.

        The method iterates through all documents in the context, uses the embedder to generate 
        embeddings for each document's content, and adds the resulting embeddings to the document's metadata.

        Args:
            context (Dict[str, Any]): The context containing the documents for which embeddings need to be generated.

        Updates:
            context["documents"]: Each document in the context will have an "embeddings" field in its metadata.
        """
        documents: list[Document] = context["documents"]
        for doc in documents:
            doc.metadata["embeddings"] = self._embedder.embed(doc.page_content)