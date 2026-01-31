from typing import Any, Dict
from mini_local_rag.logger.log_record import LogRecord
from mini_local_rag.pipeline import Step
from langchain_core.documents import Document


class AppendRetrievalLogsStep(Step):
    label="Append retrieval info to log record"
    def execute(self, context: Dict[str, Any]) -> None:

        documents:list[Document] = context.get("documents",[])
        record:LogRecord = context['log_record']

        record.retrieval = getattr(record,'retrieval',[])
        for doc in documents:
                    record.retrieval.append({
                    "file":doc.metadata["file_path"],
                    "id":doc.metadata["id"],
                    "score":doc.metadata.get("score",None)
            })
                