from typing import Any, Dict
from langchain_core.documents import Document

from mini_local_rag.config import Config
from mini_local_rag.embedder import Qwen3Embedder
from mini_local_rag.pipeline import Step


class GenerateEmbeddingsStep(Step):
    label = "Embedding generation"
    _embedder = Qwen3Embedder()
    """
    A pipeline step that generates embeddings for documents using a specified embedder model.

    This step uses an embedder to create embeddings for each document in the pipeline, 
    and stores the generated embeddings in the document's metadata.

    Attributes:
        label (str): The label identifying this step ("Embedding generation").
        _embedder (Qwen3Embedder): The embedder instance used to generate embeddings for the document content.
    """
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