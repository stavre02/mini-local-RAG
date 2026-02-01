import re
from typing import Any, Dict

from ollama import chat
from langchain_core.documents import Document
from rich.markdown import Markdown

from mini_local_rag.config import Config
from mini_local_rag.logger.log_record import LogRecord
from mini_local_rag.pipeline import Step

class DraftResponseStep(Step):
    """
    A pipeline step that drafts a response to a given question based on the context provided by documents.

    This step uses a model to generate a response to the question, augmented with information extracted from 
    the relevant documents. The context and response are formatted into a markdown response, including citations
    to the documents used to generate the answer.

    Attributes:
        label (str): The label identifying this step ("Draft response").
        instruction (str): A predefined instruction to the model explaining its task.
        answer_model (str): The model used to generate the answer to the question.
    """
    label = "Draft response"
    # better leave this here and not in config class because we modify the str with it.
    instruction  = """
    You are a Retrieval-Augmented Generation answering system.
    Your task is to answer the given question based only on information from the reports provided context provided, which is uploaded in the format of relevant pages extracted using RAG.
    """
    def __init__(self,config:Config):
        """
        Initializes the step with the provided configuration for the answer model.

        Args:
            config (Config): The configuration object containing the model information.
        """
         
        self.answer_model =config.answer_model
    def execute(self, context: Dict[str, Any]) -> None:
        """
        Drafts a response to the given question based on the documents in the context.

        The method constructs a prompt by combining the predefined instruction and the context (documents) 
        and sends it to the model for generating a response. The model's answer is then processed to create
        a markdown-formatted response, including citations to the relevant documents used for answering.

        Args:
            context (Dict[str, Any]): The context containing the documents and the question. The context is updated
                                      with the generated response in markdown format under the key `"output"`.

        Updates:
            context["output"]: A markdown-formatted string containing the response and citations.
        """
        documents:list[Document] = context.get("documents",[])

        question = str(context['question'])


        ct = [doc.page_content for doc in documents]       

        prompt = self.instruction+f"""
            ---
            Here is the context:
            \"\"\"
            {ct}
            \"\"\"

            ---

            Here is the question:
            "{question}"

            - Your response can be a markdown string if needed, for example to display tables. 

        """
        response = chat(
                    model=self.answer_model,
                    messages=[{'role': 'user', 'content': prompt}],
                )
        
        draft_response = response.message.content
        
        record:LogRecord = context['log_record']

        record.draft_tokens = len(re.split(r"[\s,!?]+", draft_response))


        # Table header
        markdown = "\n"
        markdown += "# Response \n"
        markdown += draft_response
        markdown += "\n\n"
        markdown += "| Document | Section | \n"
        markdown += "|-----------|---------|\n"

        # Table rows for each citation
        added_combinations = set()

        for doc in documents:
            file_path = doc.metadata['file_path']
            section = doc.metadata['headers']
            entry = f"| {file_path} | {section} |\n"
            # ensure unique sections are displayed, we might have multiple chunks in one section so display once
            if entry not in added_combinations:
                added_combinations.add(entry)
                markdown += entry

        markdown += "----\n" 
        
        context['output']=Markdown(markdown)