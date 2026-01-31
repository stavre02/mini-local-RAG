from typing import Any, Dict
from docling_core.types.doc.document import DoclingDocument
from mini_local_rag.config import Config
from mini_local_rag.pipeline import Step

class MarkdownConvertStep(Step):
    """
    A pipeline step that converts a PDF document to Markdown format.

    Attributes:
        label (str): The label identifying this step ("Convert pdf to markdown").
    """
    label = "Convert pdf to markdown"
    def execute(self, context: Dict[str, Any]) -> None:
        """
        Converts the PDF document in the context to Markdown format and adds it to the context.

        Args:
            context (Dict[str, Any]): The context containing the PDF document and where the converted Markdown will be stored.
        Updates:
            context["markdown"]: The converted document in Markdown format.
        """
        document: DoclingDocument = context["pdf"]
        context["markdown"]= document.export_to_markdown(image_placeholder="")