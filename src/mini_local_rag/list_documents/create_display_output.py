from typing import Any, Dict
from mini_local_rag.pipeline import Step
from rich.markdown import Markdown
from langchain_core.documents import Document

class CreateDisplayOutputStep(Step):
    """
    A pipeline step that generates a Markdown output displaying a list of documents.

    This step formats the list of documents in a Markdown table and stores the resulting 
    Markdown in the pipeline's context for display or further processing.

    Attributes:
        label (str): A label identifying this step ("Create output").

    Methods:
        execute(context: Dict[str, Any]) -> None:
            Executes the step by generating a Markdown output representing the documents 
            and storing it in the context under the 'output' key.
    """
    label = "Create output"

    def execute(self, context: Dict[str, Any]) -> None:
        """
        Executes the output creation step.

        This method formats the documents into a Markdown table and stores the result in 
        the context under the 'output' key.

        Args:
            context (Dict[str, Any]): The context containing shared data for the pipeline.

        Updates:
            context['output'] (Markdown): A Markdown formatted string containing a table of documents.
        """
        documents:list[Document] = context.get("documents",[])
        
        markdown:list[str] = []
        markdown.append("")
        markdown.append("# Documents")
        markdown.append("| idx | Document |")
        markdown.append("|-----------|---------|")

        for idx, doc in enumerate(documents):
            markdown.append( f"| {1+idx} | {doc} |")

        markdown.append("----")
        markdown.append("")
        context["output"]=Markdown("\n".join(markdown))