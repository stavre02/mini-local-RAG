from typing import Any, Dict
from mini_local_rag.logger.log_record import LogRecord
from mini_local_rag.pipeline import Step
from langchain_core.documents import Document


class AppendRetrievalLogsStep(Step):
    """
    A pipeline step that appends document retrieval information to a log record.

    This step iterates through the retrieved documents in the context, extracts metadata such as the file path, 
    document ID, and retrieval score, and appends this information to the `retrieval` field of the log record. 
    If the `retrieval` field does not exist, it will be initialized as an empty list.

    Attributes:
        label (str): The label identifying this step ("Append retrieval info to log record").
    """
    label="Append retrieval info to log record"
    def execute(self, context: Dict[str, Any]) -> None:
        """
        Appends retrieval-related information from the context's documents to the log record.

        The method checks the context for the `"documents"` key and retrieves the document metadata (such as 
        the file path, document ID, and score) and appends it to the `"retrieval"` list in the log record. 
        If the `retrieval` list does not exist in the log record, it will be created.

        Args:
            context (Dict[str, Any]): The context containing the documents and the log record. The context must
                                      contain a `"documents"` key with a list of `Document` objects and a
                                      `"log_record"` key with a `LogRecord` object.

        Updates:
            context["log_record"].retrieval (List[Dict]): A list of dictionaries containing the file path, document ID,
                                                         and score (if available) for each document in the retrieval process.
        """    
        documents:list[Document] = context.get("documents",[])
        record:LogRecord = context['log_record']

        record.retrieval = getattr(record,'retrieval',[])
        for doc in documents:
                    record.retrieval.append({
                    "file":doc.metadata["file_path"],
                    "id":doc.metadata["id"],
                    "score":doc.metadata.get("score",None)
            })
                