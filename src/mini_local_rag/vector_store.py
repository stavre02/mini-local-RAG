import chromadb
from langchain_core.documents import Document

from mini_local_rag.config import Config
     

class VectorStore:
    """
    A class for storing, querying, and managing vector embeddings using ChromaDB.

    This class integrates with the ChromaDB vector database, storing document embeddings
    and metadata, and providing querying capabilities for retrieving similar documents.

    Attributes:
        __collection_name (str): The name of the ChromaDB collection used for storing embeddings.
        __distance_threshold (float): The maximum distance threshold used when filtering query results.
        _collection (chromadb.Collection): The ChromaDB collection instance used for storing data.

    Methods:
        __init__(): Initializes the `VectorStore` by setting up a ChromaDB collection.
        saveAll(documents: list[Document]) -> None: Saves a list of documents to the ChromaDB collection.
        query(query: str, top_k: int = 3) -> list[Document]: Queries the ChromaDB collection to retrieve the most
                                                             similar documents to a given query string.
        listDocuments() -> set[str]: Lists the file paths of all documents currently stored in the collection.
    """

    __collection_name: str = "embeddings_collection"  # The name of the collection in ChromaDB.
    __distance_threshold: float = 0.35  # Threshold for distance when filtering query results.
    def __init__(self,config:Config):
        """
        Initializes the `VectorStore` instance by setting up the ChromaDB client and collection.

        Creates a ChromaDB `PersistentClient` and sets up a collection with cosine similarity
        using the HNSW (Hierarchical Navigable Small World) index for efficient vector search.
        """
        client = chromadb.PersistentClient(path=config.chromadb_path)
        # "hnsw:space": "cosine" -> Use cosine
        self._collection = client.get_or_create_collection(name=self.__collection_name,metadata={"hnsw:space": "cosine"})

    def saveAll(self,documents:list[Document]) -> None:
        """
        Saves a list of documents to the ChromaDB collection.

        Args:
            documents (list[Document]): A list of `Document` objects to be saved in the collection.

        The method extracts the following information from each document's metadata:
        - `id`: Document's unique identifier.
        - `embeddings`: The document's embedding vector.
        - `page_content`: The textual content of the document.
        - `headers` and `file_path`: Metadata associated with the document.

        This information is added to the ChromaDB collection for future querying.
        """
        ids = [doc.metadata["id"] for doc in documents]
        embeddings = [doc.metadata["embeddings"] for doc in documents]
        contents = [doc.page_content for doc in documents]
        metadatas = [{"headers": doc.metadata["headers"], "file_path": doc.metadata["file_path"]} for doc in documents]

        self._collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=contents,
            metadatas=metadatas
        )
    def query(self,embdedding:list[float],top_k = 3) -> list[Document]:
        """
        Queries the ChromaDB collection for the most similar documents to the given query.

        Args:
            embdedding list[float]: The embdedding for which to retrieve similar documents.
            top_k (int, optional): The number of top results to return. Default is 3.

        Returns:
            list[Document]: A list of `Document` objects representing the top-k most similar documents.

        The method computes the cosine distance between the query and stored document embeddings,
        filtering out results that exceed the `__distance_threshold`. It returns documents that
        are within the threshold distance, along with additional metadata, such as `id`, `headers`,
        `file_path`, and a calculated `score` based on the inverse distance.
        """
        results = self._collection.query(
            query_embeddings=embdedding,
            n_results=top_k
        )
        documents:list[Document] =[]
        for id,page_content, metadata,distance in zip(results["ids"][0],results["documents"][0],results["metadatas"][0],results["distances"][0]):
            if ( distance <= self.__distance_threshold):
                documents.append(Document(
                    page_content,
                    metadata ={
                        "id": id,
                        "headers":metadata["headers"],
                        "file_path":metadata["file_path"],
                        "score": (1-distance)
                    }
                ))
        return documents
    
    def listDocuments(self) -> set[str]:
        """
        Lists all documents currently stored in the ChromaDB collection by their file paths.

        Returns:
            set[str]: A set of file paths for all documents in the collection.

        The method retrieves the metadata of all stored documents and extracts the file path (`file_path`)
        to return a unique set of paths.
        """
        results = self._collection.get()
        doc_names = set()
        for metadata in results["metadatas"]:
           file_path = str(metadata['file_path'])
           doc_names.add(file_path)

        return doc_names