from abc import ABC, abstractmethod
import ollama


class Embedder(ABC):
    """
    An abstract base class that defines the interface for embedding generators.

    This class should be subclassed to implement embedding generation for various models or methods. 
    The `embed` method must be implemented by any subclass to convert input text into a list of floating point numbers representing its embedding.

    Methods:
        embed: An abstract method that takes a text string and returns its embedding as a list of floats.
    """
    
    @abstractmethod
    def embed(self, text: str) -> list[float]:
        """
        Abstract method to generate an embedding for a given text.

        Args:
            text (str): The input string for which the embedding will be generated.

        Returns:
            list[float]: A list of floating point numbers representing the embedding of the input text.
        """
        pass

class Qwen3Embedder(Embedder):
    """
    A concrete implementation of the `Embedder` interface for generating embeddings using the Qwen3 model.

    This class uses the Qwen3 model to generate text embeddings. The model is specified by the class-level attribute `__model`.
    It uses the Ollama API to interact with the model and retrieve the embeddings.

    Attributes:
        __model (str): The identifier of the Qwen3 model to be used for generating embeddings.

    Methods:
        embed: Implements the abstract `embed` method to generate embeddings using the Qwen3 model.
    """

    __model = 'qwen3-embedding:4b' 

    def embed(self, text: str) -> list[float]:
        """
        Generates an embedding for the provided text using the Qwen3 model.

        This method uses the Ollama API to call the Qwen3 model and retrieve the embeddings.
        
        Args:
            text (str): The input text string to be embedded.

        Returns:
            list[float]: A list of floating-point numbers representing the text's embedding.

        Example:
            embedder = Qwen3Embedder()
            embedding = embedder.embed("This is a sample text.")
            print(embedding)  # Outputs the embedding as a list of floats.
        """
        res = ollama.embed(
            model=Qwen3Embedder.__model,
            input=text
        )

        return res['embeddings'][0]