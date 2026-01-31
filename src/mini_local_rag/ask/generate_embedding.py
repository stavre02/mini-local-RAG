
from typing import Any, Dict
from mini_local_rag.embedder import Embedder
from mini_local_rag.pipeline import Step


class GenerateQuestionEmbeddingsStep(Step):
    """
    A pipeline step that generates embeddings for a question using a specified embedder model.

    This step uses an embedder (such as `Qwen3Embedder`) to create embeddings for the provided question 
    and stores the resulting embedding in the context. The embedder is passed as an argument during 
    the initialization of the step.

    Attributes:
        label (str): The label identifying this step ("Embedding generation").
        embedder (Embedder): The embedder instance used to generate embeddings for the question. 
                              The embedder model is passed during initialization.
    """  
    label = "Embedding generation"
    def __init__(self,embedder:Embedder):
        """
        Initializes the step with the provided embedder.

        Args:
            embedder (Embedder): The embedder instance used to generate embeddings for the question.
        """
        self.embedder = embedder
    def execute(self, context: Dict[str, Any]) -> None:
        """
        Generates an embedding for the question provided in the context and stores it in the context.

        The method takes the question from the context, generates its embedding using the embedder, 
        and adds the embedding to the context under the key `"embedding"`.

        Args:
            context (Dict[str, Any]): The context containing the question for which the embedding needs to be generated.

        Updates:
            context["embedding"]: The generated embedding for the question is added to the context.
        """
        context["embedding"] = self.embedder.embed(str(context["question"]))