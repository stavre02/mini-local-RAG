import os
from typing import Any, Dict
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions, EasyOcrOptions , AcceleratorDevice, AcceleratorOptions
from mini_local_rag.config import Config
from mini_local_rag.pipeline import Step

class PdfParseStep(Step):
    """
    A step in the pipeline responsible for parsing PDF files, extracting data, and performing OCR and table structure extraction.

    Attributes:
        label (str): The label identifying this step ("Parsing Pdf file").
        _converter (DocumentConverter): The converter responsible for parsing PDFs with options for OCR, table structure, and image generation.
    """
    label="Parsing Pdf file"
    models_folder ="models"
    def __init__(self,config:Config,num_threads=4):
        """
        Initializes the PdfParseStep with options for parsing PDFs, performing OCR, and other related tasks.

        Args:
            num_threads (int): The number of threads to use for acceleration during PDF processing (default is 4).
            config (Config): The configuration for the pipeline containing parameters for the models.
        """
        path = None
        if (config.enable_local_models):
            cwd = os.getcwd()
            path = os.path.join(cwd, config.data_folder,self.models_folder)

        pipeline_options = PdfPipelineOptions(
            do_ocr=True,
            do_table_structure=True,
            generate_picture_images=True,
            generate_page_images=True,
            do_formula_enrichment=True,
            artifacts_path= path,
            table_structure_options={"do_cell_matching": True},
            ocr_options=EasyOcrOptions(),
            accelerator_options=AcceleratorOptions(num_threads, device=AcceleratorDevice.CPU),
        )
        format_options = {InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)}
        self._converter = DocumentConverter(format_options=format_options)

    def execute(self, context: Dict[str, Any]) -> None:
        """
        Executes the PDF parsing step and adds the parsed document to the context.

        Args:
            context (Dict[str, Any]): The context holding shared data for the pipeline execution, including the file path.

        Updates:
            context["pdf"]: The parsed PDF document.
        """
        file_path = str(context["file_path"])

        if not os.path.isabs(file_path):
            cwd = os.getcwd()
            file_path = os.path.join(cwd, file_path)


        context["pdf"] = self._converter.convert(file_path).document