from docling_core.types.doc.document import PictureItem, DocItemLabel,DoclingDocument
from typing import Any, Dict

import ollama

from mini_local_rag.config import Config
from mini_local_rag.pipeline import Step


class ImageReplaceStep(Step):
    """
    A pipeline step that replaces images in a PDF document with text extracted using a vision model.

    Attributes:
        label (str): The label identifying this step ("Replacing images on pdf with text").
    """
    label = "Replacing images on pdf with text"
    def __init__(self, config: Config) -> None:
        """
        Initializes the image to text prompt used on ollama.
        Initializes the vision model name
        Args:
            config (Config): The configuration for the pipeline containing parameters for the splitters.
        """
        self.vision_model = config.vision_model
        self.prompt= config.image_to_text_prompt
    def execute(self,context: Dict[str, Any]) -> None:
        """
        Replaces images in the PDF document with text extracted using a vision model.

        The method iterates through the PDF document's items, identifies images, and sends each image to the configured vision model to extract text. 
        The extracted text is then added to the document as a replacement for the image.

        Args:
            context (Dict[str, Any]): The context containing the PDF document and other shared data.

        Updates:
            context["pdf"]: The modified document with images replaced by extracted text.
        """
        document: DoclingDocument = context["pdf"]
        replacements = []
        for item, _ in document.iterate_items():
            if isinstance(item, PictureItem):
                img = item.image.uri.path.split(",")[1]
                response = ollama.chat(
                        model=self.vision_model,
                        messages=[
                        ollama.Message(role='user', content=self.prompt, images=[ollama.Image(value=img)])
                    ],)
                
                new_text = document.add_text(
                    label=DocItemLabel.TEXT,
                    text=response.message.content,
                    prov=item.prov[0] if item.prov else None
                )
                replacements.append((item, new_text))
        for old_item, new_item in replacements:
            document.replace_item(new_item=new_item, old_item=old_item)