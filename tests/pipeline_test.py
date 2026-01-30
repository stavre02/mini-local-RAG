from typing import Any, Dict
import pytest
from unittest.mock import MagicMock
from mini_local_rag.pipeline import Pipeline,Step 

# Mocking the Step class since it's abstract and doesn't have an implementation
class MockStep(Step):
    def __init__(self, label: str):
        self.label = label

    def execute(self, context: Dict[str, Any]) -> None:
        # Mock execution of the step
        context["executed_steps"].append(self.label)


@pytest.fixture
def pipeline():
    """
    Creates a pipeline with mock steps for testing.
    """
    # Context that will be shared between steps
    context = {"executed_steps": []}

    # Create mock steps
    steps = [MockStep("Step 1"), MockStep("Step 2"), MockStep("Step 3")]

    # Create the pipeline instance
    return Pipeline(label="Test Pipeline", context=context, steps=steps, debug=False)


def test_pipeline_initialization(pipeline):
    """
    Test the initialization of the Pipeline class.
    """
    # Ensure the pipeline has the correct label, trace_id, and steps
    assert pipeline.label == "Test Pipeline"
    assert len(pipeline.steps) == 3
    assert pipeline.context == {"executed_steps": []}
    assert isinstance(pipeline.trace_id, str)


def test_pipeline_execute(pipeline):
    """
    Test the execute method of the Pipeline class.
    This test checks if the steps are executed in sequence.
    """
    pipeline.execute()

    # Check if all steps were executed in order
    executed_steps = pipeline.context["executed_steps"]
    assert executed_steps == ["Step 1", "Step 2", "Step 3"]


def test_pipeline_execute_with_exception(pipeline):
    """
    Test the execute method of the Pipeline class when an exception occurs in one of the steps.
    """
    # Modify the execute method of the second step to raise an exception
    pipeline.steps[1].execute = MagicMock(side_effect=Exception("Step failed"))

    # Run the pipeline and check if it catches the exception
    pipeline.execute()
        

    # Ensure that the error is logged and the correct number of steps are executed before the exception
    executed_steps = pipeline.context["executed_steps"]
    assert executed_steps == ["Step 1"]