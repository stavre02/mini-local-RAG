from abc import ABC, abstractmethod
import time
from typing import Any, Dict
import uuid
from rich import print as rprint
from rich.progress import Progress,TextColumn,BarColumn, TaskProgressColumn

from mini_local_rag.config import Config

class Step(ABC):
    """
    The basic step for a pipeline

    Attributes:
        label (str): A label for identifying the step instance.
    """
    label: str
    def __init__(self,label:str):
        self.label=label

    @abstractmethod
    def execute(self, context: Dict[str, Any]) -> None:
        """
        Pipeline step execution
        This will be executed when pipeline reaches this step
        """
        pass

class Pipeline:
    """
    A class representing a pipeline of steps to be executed in sequence, with logging, progress tracking, and latency measurement.

    Attributes:
        trace_id (str): A unique identifier for this execution instance.
        steps (List[Step]): A list of steps to be executed in the pipeline.
        latency (Dict[str, float]): A dictionary mapping each step's name to the time it took to execute.
        label (str): A label for identifying the pipeline instance.
        context (Dict[str, Any]): A dictionary of context variables that are shared across all steps.
        debug (bool): Flag indicating whether to enable debug logging.
        config (Config): Configuration object that holds pipeline settings.
    """
    trace_id: str
    steps: list[Step]
    latency: Dict[str,float]
    label: str
    context: Dict[str, Any]
    debug: bool
    config: Config
    def __init__(self,label: str,config:Config,context:Dict[str, Any],steps:list[Step]):
        """
        Initializes a new Pipeline instance.

        Args:
            label (str): A label identifying the pipeline.
            config (Config): A configuration object containing pipeline-specific settings.
            context (Dict[str, Any]): A dictionary of context data shared across steps.
            steps (List[Step]): A list of steps to be executed in the pipeline.
            debug (bool): Flag indicating whether to enable debug logging.

        Attributes:
            trace_id (str): A unique identifier for this pipeline execution, generated during initialization.
            latency (Dict[str, float]): A dictionary that will hold the time durations for each step after execution.
        """
        self.trace_id = str(uuid.uuid4())
        self.label = label
        self.context = context
        self.steps= steps
        self.latency={}
        self.config=config
    def execute(self) -> None:
        """
        Executes the pipeline steps sequentially, tracking progress and logging the results.

        This method iterates over all the steps in the pipeline, executing them one by one.
        For each step, it measures the execution time and logs any errors. It also displays
        progress to the console.

        Raises:
            Exception: If an error occurs during execution, it logs the error and stops the pipeline
        """
        try:
            with Progress(TextColumn("[progress.description]{task.description}"),
                            BarColumn(),
                            TaskProgressColumn(),
                            transient=False) as progress:
                task = progress.add_task(self.label, total=len(self.steps), time_remaining=None)
                
                for idx,step in enumerate(self.steps):
                    start = time.time()
                    try:                                        
                        step.execute(self.context)                   
                    finally:
                        progress.update(task, advance=1)
                        diff = round((time.time() - start) , 2)
                        self.latency [f"{idx}-{step.label}({step.__class__.__name__})"] = diff
        except Exception as e:    
            rprint(f"There was an issue while processing the request trace_id: {self.trace_id}")

