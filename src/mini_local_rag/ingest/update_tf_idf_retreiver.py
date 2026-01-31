import os
from typing import Any, Dict
from mini_local_rag.config import Config
from mini_local_rag.pipeline import Step
from langchain_core.documents import Document

from mini_local_rag.tf_idf_retriever import CustomTFIDFRetriever


class UpdateTFIDFRetrieverStep(Step):
    """
    A pipeline step that updates a TF-IDF retriever model with new documents.

    This step loads an existing retriever model (if available), adds new documents to it, 
    and saves the updated model back to the specified path.

    Attributes:
        label (str): The label identifying this step ("update tf idf retriever model").
    """
    label="update tf idf retriever model"
    def __init__(self, config: Config) -> None:
        """
        Initializes the retriever path.

        Args:
            config (Config): The configuration for the pipeline containing parameters for the splitters.
        """
        self.retriever_path = config.retriever_path

    def execute(self,context: Dict[str, Any]) -> None:
        """
        Updates the TF-IDF retriever model by adding new documents to the existing model.

        The method loads the current retriever model (if it exists), combines it with the 
        new documents provided in the pipeline context, and saves the updated model.

        Args:
            context (Dict[str, Any]): The context containing the new documents to be added to the retriever model.
            config (Config): The configuration containing the path to the retriever model.

        """
        cwd = os.getcwd()
        path = os.path.join(cwd, self.retriever_path)
        documents: list[Document] = context["documents"]
        
        if os.path.exists(path):
            retriever = CustomTFIDFRetriever.load_local(folder_path=path,allow_dangerous_deserialization=True)
            old_docs = retriever.docs
            documents = old_docs+documents

        retriever = CustomTFIDFRetriever.from_documents(documents=documents)
        retriever.save_local(folder_path=path)