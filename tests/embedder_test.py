from mini_local_rag.embedder import Qwen3Embedder

def test_embed_returns_float_list():
    """
    Test that the embed method returns a list of floats without mocking.
    """

    # Act: Create an instance of Qwen3Embedder and call embed method
    embedder = Qwen3Embedder()
    result = embedder.embed("Test string")

    # Assert: Check that the result is a list of floats
    assert isinstance(result, list), "Result should be a list"
    assert all(isinstance(i, float) for i in result), "All elements should be floats"
    assert len(result) > 0, "Embedding should not be an empty list"