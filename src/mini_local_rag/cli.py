import argparse
import shlex

from mini_local_rag.config import Config
from mini_local_rag.pipeline_builder import PipelineBuilder

def documents_cmd(args: argparse.Namespace) -> None:
    PipelineBuilder(config=Config(show_logs=args.show_logs)).get_documents().execute()

def ingest_cmd(args: argparse.Namespace) -> None:
    PipelineBuilder(config=Config(show_logs=args.show_logs)).get_ingestion_pipeline(file_path=args.file_path).execute()

def ask_cmd(args: argparse.Namespace) -> None:
    PipelineBuilder(config=Config(show_logs=args.show_logs)).get_ask_pipeline(question=args.question).execute()

def interactive_mode(parser:argparse.ArgumentParser)->None:
    print("Entering interactive mode. Type 'exit' to quit.")
    
    while True:
        try:
            user_input = input(">>> ")

            if user_input.lower() == 'exit':
                print("Exiting interactive mode.")
                break

                
            args_list = shlex.split(user_input)
            args = parser.parse_args(args=args_list)
            
            if not args.command:
                parser.print_help()
                return

            args.func(args)
        except SystemExit as e:
            # make args parse not exit te app 
            pass
        except Exception as e:
            pass


def build_parser(interactive:bool) -> argparse.ArgumentParser:
    prog = "" if interactive else None
    parser = argparse.ArgumentParser(
            description="Pipeline command line interface for processing PDF reports and as questions.",
            prog=prog
        )
    subparsers = parser.add_subparsers(dest="command")

    # documents command
    documents = subparsers.add_parser("documents", help="List all documents by path")
    documents.add_argument("--show-logs", action="store_true", help="Display debug logs")
    documents.set_defaults(func=documents_cmd)

    # ingest command
    ingest = subparsers.add_parser("ingest", help="Ingest a document")
    ingest.add_argument("file_path", help="Path to the pdf file to ingest")
    ingest.add_argument("--show-logs", action="store_true", help="Display debug logs")
    ingest.set_defaults(func=ingest_cmd)

    # ask command
    ask = subparsers.add_parser("ask", help="Ask a question")
    ask.add_argument("question", help="Question to ask")
    ask.add_argument("--show-logs", action="store_true", help="Display debug logs")
    ask.set_defaults(func=ask_cmd)

    return parser

def main():
    import sys
    
    
    if '-i' in sys.argv or '--interactive' in sys.argv:
        # If -i is passed, run the interactive mode
        parser = build_parser(interactive=True)
        interactive_mode(parser)
    else:
        parser = build_parser(interactive=False)
        args = parser.parse_args()
    
        if not args.command:
            parser.print_help()
            return

        args.func(args)


if __name__ == "__main__":
    main()