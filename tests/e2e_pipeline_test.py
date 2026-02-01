import os
from pathlib import Path
import shutil
from mini_local_rag.config import Config
from mini_local_rag.logger.log_record import LogRecord
from mini_local_rag.pipeline_builder import PipelineBuilder
from rich.markdown import Markdown

import pytest



@pytest.fixture
def pipelineBuilder():
    """
    Create a clean PipelineBuilder instance for end-to-end tests.

    This fixture:
    - Ensures test isolation by removing any existing test data
    - Uses test-specific paths for vector store and retriever data
    - Returns a fully configured PipelineBuilder ready for execution

    Returns:
        PipelineBuilder: A pipeline builder configured for test execution.
    """
    cwd = Path().cwd()
    # Remove existing data
    try:
        shutil.rmtree(os.path.join(cwd,".test/data"))
    except FileNotFoundError as e:
        pass
    return PipelineBuilder(config=Config(retriever_path=".test/tf-idf-retriever",chromadb_path=".test/chroma_db"))


def test_pipelines_e2e(pipelineBuilder:PipelineBuilder):
    """
    End-to-end test covering the full pipeline lifecycle.

    This test validates:
    1. Document ingestion
    2. Vector store population
    3. Question answering pipeline execution
    4. Log record correctness
    5. Document retrieval
    6. Output generation
    7. Document listing pipeline

    The goal is to ensure all core pipelines work correctly.
    """
    cwd = Path().cwd()

    full_path = os.path.join(cwd,"tests","test_doc","test_page.pdf")
    pipelineBuilder.get_ingestion_pipeline(file_path=full_path).execute()
    docs =list(pipelineBuilder.vector_store.listDocuments())

    assert len(docs)==1 , "Expected 1 document to be ingested"

    assert docs[0] == full_path , f"Expected document ${full_path} was not ingested"


    pipeline = pipelineBuilder.get_ask_pipeline("what are ICH guidances?")

    pipeline.execute()

    context = pipeline.context

    log_record:LogRecord = context["log_record"]

    assert len(log_record.errors)==0 , f"There where erros while asking a question : {log_record.errors}" 

    documents=context["documents"]

    assert len(documents)>0 , "Expected to find documents"


    output: Markdown =context['output']

    assert len(output.markup)>0 , "Expected to find output"


    pipeline = pipelineBuilder.get_documents()
    pipeline.execute()
    output = pipeline.context.get("output",None)

    assert output is not None , "Expected to have output"