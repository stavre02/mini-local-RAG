from typing import Any, Dict
import uuid
from mini_local_rag.config import Config
from mini_local_rag.pipeline import Step
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

class MarkdownChunkingStep(Step):
    """
    A pipeline step that splits a Markdown document into smaller chunks based on header structure and character length.

    Attributes:
        label (str): The label identifying this step ("Splitting Markdown into chunks").
        markdown_splitter (MarkdownHeaderTextSplitter): The splitter used to break the Markdown text based on headers.
        text_splitter (RecursiveCharacterTextSplitter): The splitter used to break the text into smaller chunks of a specified size.
    """
    label = "Splitting Markdown into chunks"

    def __init__(self, config: Config) -> None:
        """
        Initializes the splitters used to chunk the Markdown document.

        Args:
            config (Config): The configuration for the pipeline containing parameters for the splitters.
        """
        self.markdown_splitter = MarkdownHeaderTextSplitter(config.headers_to_split_on, strip_headers=True)
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=config.chunk_size, chunk_overlap=config.chunk_overlap)

    def execute(self, context: Dict[str, Any]) -> None:
        """
        Splits the Markdown document into chunks based on headers and character length, and adds metadata to each chunk.

        The method first splits the Markdown document by its headers and then further splits the resulting text into smaller chunks.
        Metadata, including file path and chunk identifier, is added to each chunk.

        Args:
            context (Dict[str, Any]): The context containing the Markdown document and file path.

        Updates:
            context["documents"]: A list of document chunks with metadata.
        """

        documents = self.markdown_splitter.split_text(str(context["markdown"]))
        file_path = str(context["file_path"])
        chunks: list[Document] = self.text_splitter.split_documents(documents)
        for doc in chunks:
            doc.metadata['file_path'] = file_path
            doc.metadata['id']= str(uuid.uuid4())
            doc.metadata['headers']= (doc.metadata.get("Header 1") or "" +" "+ doc.metadata.get("Header 2") or "")
            doc.metadata.pop("Header 1",None)
            doc.metadata.pop("Header 2",None)

        context["documents"] = chunks