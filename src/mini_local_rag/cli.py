
from mini_local_rag.config import Config
from mini_local_rag.pipeline_builder import PipelineBuilder


def main() -> None:
    builder = PipelineBuilder(config=Config(enable_local_models=True,show_logs=True))
    # pipeline = builder.get_ingestion_pipeline(file_path=r"""C:\Users\STAVRE02\Documents\dev\mini-local-rag\documents\E3 Structure - Document 2.pdf""")
    pipeline = builder.get_ask_pipeline(question="what is the ICH E3 guidance ")
    pipeline.execute()


if __name__ == "__main__":
    main()