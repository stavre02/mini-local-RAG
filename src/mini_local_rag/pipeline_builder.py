from mini_local_rag.ask.draft_response import DraftResponseStep
from mini_local_rag.ask.generate_embedding import GenerateQuestionEmbeddingsStep
from mini_local_rag.ask.log_retrieval import AppendRetrievalLogsStep
from mini_local_rag.ask.retrieve_tf_idf import InvokeTFIDFRetrieverStep
from mini_local_rag.ask.retrieve_vector import RetrieveFromVectorStoreStep
from mini_local_rag.config import Config
from mini_local_rag.embedder import Embedder, Qwen3Embedder
from mini_local_rag.ingest.chunk_markdown import MarkdownChunkingStep
from mini_local_rag.ingest.convert_markdown import MarkdownConvertStep
from mini_local_rag.ingest.generate_embeddings import GenerateEmbeddingsStep
from mini_local_rag.ingest.pdf_parse import PdfParseStep
from mini_local_rag.ingest.persist_changes import PersistChangesStep
from mini_local_rag.ingest.replace_images import ImageReplaceStep
from mini_local_rag.ingest.update_tf_idf_retreiver import UpdateTFIDFRetrieverStep
from mini_local_rag.logger.structured_logger import StructuredLogger
from mini_local_rag.pipeline import Pipeline
from mini_local_rag.vector_store import VectorStore


class PipelineBuilder:
    def __init__(self,config:Config):
        self.config=config
        self.embedder: Embedder = Qwen3Embedder()
        self.vector_store=VectorStore(config=config)
        self.logger = StructuredLogger(config=config)
        self.ingestion_steps =[
                    PdfParseStep(config=config),
                    ImageReplaceStep(config=config),
                    MarkdownConvertStep(),
                    MarkdownChunkingStep(config=config),
                    GenerateEmbeddingsStep(embedder=self.embedder),
                    PersistChangesStep(vector_store=self.vector_store),
                    UpdateTFIDFRetrieverStep(config=config)
                ]
        self.ask_steps = [
            GenerateQuestionEmbeddingsStep(embedder=self.embedder),
            RetrieveFromVectorStoreStep(vector_store=self.vector_store),
            InvokeTFIDFRetrieverStep(config=self.config),
            AppendRetrievalLogsStep(),
            DraftResponseStep(config=self.config)
        ]
        
    def get_ingestion_pipeline(self,file_path:str) -> Pipeline:

        return Pipeline(label=f"Ingesting file: {file_path}",context={"file_path":file_path},steps=self.ingestion_steps,config=self.config,logger=self.logger)
    
    def get_ask_pipeline(self,question:str)-> Pipeline:
        
        return Pipeline(label="Planning answer",context={"question":question},steps=self.ask_steps,config=self.config,logger=self.logger)