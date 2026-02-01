
from unittest.mock import MagicMock
import uuid
from mini_local_rag.ingest.chunk_markdown import MarkdownChunkingStep
import pytest



@pytest.fixture
def mock_config():
    config = MagicMock()
    config.headers_to_split_on = ["#"]  # Example header to split on
    config.chunk_size = 500  # Example chunk size
    config.chunk_overlap = 50  # Example overlap
    return config


@pytest.fixture
def mock_splitters():
    # Mock the splitters
    markdown_splitter = MagicMock()
    text_splitter = MagicMock()

    # Mock the splitting behavior
    markdown_splitter.split_text.return_value = ["Header 1\nContent 1", "Header 2\nContent 2"]
    text_splitter.split_documents.return_value = [
        MagicMock(metadata={"Header 1": "Header 1", "Header 2": "Header 2"}),
        MagicMock(metadata={"Header 1": "Header 3", "Header 2": "Header 4"})
    ]
    
    return markdown_splitter, text_splitter

@pytest.fixture
def mock_uuid():
    # Mock the UUID generation
    mock_uuid = MagicMock(return_value="mock-uuid-1234")
    uuid.uuid4 = mock_uuid
    return mock_uuid

def test_markdown_chunking_step_execute(mock_config, mock_splitters, mock_uuid):
    markdown_splitter, text_splitter = mock_splitters

    # Instantiate the class
    step = MarkdownChunkingStep(mock_config)
    step.markdown_splitter = markdown_splitter
    step.text_splitter = text_splitter

    # Create the mock context
    context = {
        "markdown": "Header 1\nContent 1\nHeader 2\nContent 2",
        "file_path": "/some/path"
    }

    # Execute the method
    step.execute(context)

    # Assertions
    doc1 = context["documents"][0]
    assert "file_path" in doc1.metadata  # File path should be present
    assert "id" in doc1.metadata  # ID should be present
    assert "headers" in doc1.metadata  # Headers should be present
    assert doc1.metadata["headers"] == "Header 1 Header 2"

    doc2 = context["documents"][1]
    assert "file_path" in doc2.metadata  # File path should be present
    assert "id" in doc2.metadata  # ID should be present
    assert "headers" in doc2.metadata  # Headers should be present
    assert doc2.metadata["headers"] == "Header 3 Header 4"


    assert mock_uuid.call_count == 2