import os
from typing import Any, Dict
from mini_local_rag.config import Config
from mini_local_rag.pipeline import Step
from langchain_core.documents import Document

from mini_local_rag.tf_idf_retriever import CustomTFIDFRetriever


class InvokeTFIDFRetrieverStep(Step):
    """
    A pipeline step that retrieves documents using a TF-IDF retriever based on a provided question.

    This step uses a local TF-IDF retriever to retrieve relevant documents based on the provided question. 
    If the number of documents is less than 3, it will fall back to invoking the retriever. The retrieved documents
    are then added to the context, and duplicates are avoided based on document ID. The process stops when there are
    at least 3 documents.

    Attributes:
        label (str): The label identifying this step ("Document Retrieval").
        retriever_path (str): The directory where the retriever is located, retrieved from the `config.retriever_path`.
    """
    label="Document Retrieval"
    def __init__(self,config:Config):
        """
        Initializes the step with the provided configuration to locate the retriever.

        Args:
            config (Config): The configuration object containing the path to the retriever.
        """     
        self.retriever_path= config.retriever_path

    def execute(self,context: Dict[str, Any]) -> None:
        """
        Retrieves documents using a TF-IDF retriever based on the provided question in the context.

        If there are fewer than 3 documents in the context, it loads a TF-IDF retriever from the specified directory, 
        invokes the retriever with the question, and adds the retrieved documents to the context. Duplicates are avoided 
        by checking document IDs. The process stops once there are at least 3 documents.

        Args:
            context (Dict[str, Any]): The context containing the documents and the question. The context is updated with 
                                      the retrieved documents under the key `"documents"`.

        Updates:
            context["documents"]: A list of documents that are either from the context or retrieved from the TF-IDF retriever.
        """
        
        documents :list[Document] = context["documents"]
        # top_k
        if (len(documents)>=3):
            return
        
        # fallback
        question = str(context["question"])
        cwd = os.getcwd()
        path = os.path.join(cwd, self.retriever_path)
    
        if not os.path.exists(path):
            return
        
        retriever = CustomTFIDFRetriever.load_local(path,allow_dangerous_deserialization=True)    
        docs =retriever.invoke(question)
        for doc in docs:
            ids = {d.metadata["id"] for d in documents}
            if doc.metadata["id"] not in ids:
                documents.append(doc)

            # top_k
            if (len(documents)>=3):
                return