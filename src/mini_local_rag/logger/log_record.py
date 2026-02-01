import traceback
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict


class LogRecord(BaseModel):
    model_config = ConfigDict(extra="allow")
    trace_id: str
    plan: List[str]
    latency: Dict[str, float]
    errors: List[Dict[str, Any]]
    # extra fields..
    # question: Optional[str]
    # retrieval: Optional[List[Dict[str, str]]]
    # draft_tokens: int
    @staticmethod
    def create(trace_id:str,plan: List[str],latency: Optional[Dict[str, float]]={},**kwargs):
        return LogRecord(trace_id=trace_id,plan=plan,latency=latency,errors=[],**kwargs)
    
    def add_error(self,e:Exception):
        stack_trace_string = "".join(traceback.format_exception(type(e), e, e.__traceback__))
        self.errors.append({
            "exception":e.__class__.__name__,
            "message":str(e),
            "stacktrace":stack_trace_string
        
        })