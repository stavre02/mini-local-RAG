
from mini_local_rag.config import Config
from mini_local_rag.pipeline_builder import PipelineBuilder


def main() -> None:
    builder = PipelineBuilder(config=Config())
    pipeline = builder.get_ingestion_pipeline(file_path=r"""C:\Users\STAVRE02\Documents\dev\mini-local-rag\documents\E3 Structure - Document 2.pdf""")
    pipeline.execute()
    print("Completed")

if __name__ == "__main__":
    main()