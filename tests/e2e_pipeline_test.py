import os
from pathlib import Path
import shutil
from mini_local_rag.config import Config
from mini_local_rag.pipeline_builder import PipelineBuilder
import pytest



@pytest.fixture
def pipelineBuilder():
    cwd = Path().cwd()
    # Remove existing data
    try:
        shutil.rmtree(os.path.join(cwd,".test/data"))
    except FileNotFoundError as e:
        pass
    return PipelineBuilder(config=Config(retriever_path=".test/tf-idf-retriever",chromadb_path=".test/chroma_db"))

def test_pipelines_e2e(pipelineBuilder:PipelineBuilder):
    cwd = Path().cwd()

    full_path = os.path.join(cwd,"tests","test_doc","test_page.pdf")
    pipelineBuilder.get_ingestion_pipeline(file_path=full_path).execute()
    docs =list(pipelineBuilder.vector_store.listDocuments())

    assert len(docs)==1 , "Expected 1 document to be ingested"

    assert docs[0] == full_path , f"Expected document ${full_path} was not ingested"
