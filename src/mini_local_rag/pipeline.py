from abc import ABC, abstractmethod
import time
from typing import Any, Dict
import uuid
from rich import print as rprint
from rich.progress import Progress,TextColumn,BarColumn, TaskProgressColumn

from mini_local_rag.config import Config
from mini_local_rag.logger.structured_logger import StructuredLogger
from mini_local_rag.logger.log_record import LogRecord

class Step(ABC):
    """
    The base class for a step in a pipeline. All pipeline steps must inherit from this class and implement the `execute` method.

    Attributes:
        label (str): A label for identifying the step instance.
    """
    label: str

    @abstractmethod
    def execute(self, context: Dict[str, Any]) -> None:
        """
        Executes the step in the pipeline.

        This method should be overridden by subclasses to define the specific behavior of each pipeline step.
        
        Args:
            context (Dict[str, Any]): The context holding shared data for the pipeline execution.

        Raises:
            NotImplementedError: If not overridden by a subclass.
        """
        pass

class Pipeline:
    """
    A class representing a pipeline of steps to be executed in sequence, with logging, progress tracking, and latency measurement.

    The pipeline consists of a series of steps (`Step` objects) that are executed in order. Each step can modify the shared context and log its execution progress and latency. The pipeline can also capture debug logs, track execution time, and store relevant data.

    Attributes:
        trace_id (str): A unique identifier for this execution instance, generated during initialization.
        steps (List[Step]): A list of steps to be executed in the pipeline.
        latency (Dict[str, float]): A dictionary mapping each step's name to the time it took to execute.
        label (str): A label for identifying the pipeline instance.
        context (Dict[str, Any]): A dictionary of context variables that are shared across all steps.
        debug (bool): Flag indicating whether to enable debug logging.
        config (Config): Configuration object that holds pipeline settings.
        logger (StructuredLogger): Logger used for structured logging during the pipeline's execution.
    """
    trace_id: str
    steps: list[Step]
    latency: Dict[str,float]
    label: str
    context: Dict[str, Any]
    debug: bool
    config: Config
    logger:StructuredLogger
    def __init__(self,label: str,config:Config,context:Dict[str, Any],steps:list[Step],logger:StructuredLogger):
        """
        Initializes a new Pipeline instance.

        The constructor sets up the pipeline's basic attributes such as trace ID, label, context, steps, and logger. It also initializes a log record to track the execution details of the pipeline.

        Args:
            label (str): A label identifying the pipeline.
            config (Config): A configuration object containing pipeline-specific settings.
            context (Dict[str, Any]): A dictionary of context data shared across steps. This context is updated as the pipeline progresses.
            steps (List[Step]): A list of steps (`Step` objects) that will be executed in the pipeline. Each step performs an individual task.
            logger (StructuredLogger): The logger used for structured logging of the pipeline execution.

        Attributes:
            trace_id (str): A unique identifier for this pipeline execution, generated during initialization using `uuid`.
            latency (Dict[str, float]): A dictionary that holds the time durations for each step after execution.
            logger (StructuredLogger): The logger used for recording structured logs during the pipeline run.
            log_record (LogRecord): A log record that tracks the pipeline execution details, including the steps, inputs, and trace ID.
        """
        self.trace_id = str(uuid.uuid4())
        self.label = label
        self.context = context
        self.steps= steps
        self.latency={}
        self.config=config
        self.logger=logger
        log_record=LogRecord.create(trace_id=self.trace_id,plan=[f"{step.label}({step.__class__.__name__})" for step in steps])
        log_record.inputs = context.copy()
        context["log_record"]=log_record

    def execute(self) -> None:
        """
        Executes the pipeline steps sequentially, tracking progress and logging the results.

        This method iterates over all the steps in the pipeline, executing them one by one.
        For each step, it measures the execution time and logs any errors. It also displays
        progress to the console.

        Logs using StructuredLogger after completion
        
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
                    progress.update(task, description=f"{self.label} Status: {step.label}")                                    
                    start = time.time()
                    try:    
                        step.execute(self.context)                   
                    finally:
                        progress.update(task, advance=1)
                        diff = round((time.time() - start) , 2)
                        self.latency [f"{idx}-{step.label}({step.__class__.__name__})"] = diff
        except Exception as e:    
            rprint(f"There was an issue while processing the request trace_id: {self.trace_id}")
            
        log_record =getattr(self.context,"log_record",LogRecord())
        self.logger.log(log_record)