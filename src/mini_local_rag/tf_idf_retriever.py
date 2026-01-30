from langchain_community.retrievers import TFIDFRetriever

class CustomTFIDFRetriever(TFIDFRetriever):
    """
    A custom implementation of the `TFIDFRetriever` class from LangChain.
    
    This class extends the `TFIDFRetriever` and allows you to customize the number 
    of top results (`k`) returned by the retriever. By default, `k` is set to 3, 
    but it can be adjusted when initializing the `CustomTFIDFRetriever`.

    Attributes:
        k (int): The number of top results to return from the retriever.
                 Default value is 3. You can set it to any positive integer.
    
    Inheritance:
        Inherits from `TFIDFRetriever` and overrides the initialization method 
        to allow customization of the `k` parameter.
    
    Methods:
        __init__(k=3, **kwargs): Initializes the `CustomTFIDFRetriever` with the
                                  specified value for `k` and other parameters.
    """

    def __init__(self, k=3, **kwargs):
        """
        Initializes the `CustomTFIDFRetriever` with a customizable value for `k`.

        Args:
            k (int): The number of top results to retrieve. Defaults to 3.
            **kwargs: Any additional keyword arguments to be passed to the 
                      parent class (`TFIDFRetriever`).
        
        Example:
            retriever = CustomTFIDFRetriever(k=5)  # Retrieves top 5 results
            retriever = CustomTFIDFRetriever(k=10, some_other_param=value)
        
        """
    def __init__(self,k=3, **kwargs):
        super().__init__(**kwargs)
        self.k=k