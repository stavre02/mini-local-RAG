import argparse
import shlex
import sys
from typing import Optional

from mini_local_rag.config import Config
from mini_local_rag.pipeline_builder import PipelineBuilder


class AppContext:
    parser:argparse.ArgumentParser
    interactive:bool = False
    config: Optional[Config]
    parser: Optional[argparse.ArgumentParser]
    builder: Optional[PipelineBuilder]


    def __init__(self):
        if '-i' in sys.argv or '--interactive' in sys.argv: self.interactive=True



    def documents_cmd(self,args: argparse.Namespace) -> None:
        self.get_builder().get_documents().execute()

    def ingest_cmd(self,args: argparse.Namespace) -> None:
        self.get_builder().get_ingestion_pipeline(file_path=args.file_path).execute()

    def ask_cmd(self,args: argparse.Namespace) -> None:
        self.get_builder().get_ask_pipeline(question=args.question).execute()

    def interactive_mode(self)->None:
        print("Entering interactive mode. Type 'exit' to quit.")
        
        while True:
            try:
                user_input = input(">>> ")

                if user_input.lower() == 'exit':
                    print("Exiting interactive mode.")
                    break

                    
                args_list = shlex.split(user_input)
                args = self.parser.parse_args(args=args_list)
                
                if not args.command:
                    self.parser.print_help()
                    return

                args.func(args)
            except SystemExit as e:
                # make args parse not exit te app 
                pass
            except Exception as e:
                pass


    def get_builder(self) -> PipelineBuilder:
        if not hasattr(self,"builder"):
            self.builder = PipelineBuilder(config=self.config)
            return self.builder
        return self.builder

    def build_parser(self) -> None:

        prog = "" if self.interactive else None
        parser = argparse.ArgumentParser(
                description="Pipeline command line interface for processing PDF reports and as questions.",
                prog=prog
            )
        subparsers = parser.add_subparsers(dest="command")
        
        # documents command
        documents = subparsers.add_parser("documents", help="List all documents by path")
        documents.set_defaults(func=self.documents_cmd)

        # ingest command
        ingest = subparsers.add_parser("ingest", help="Ingest a document")
        ingest.add_argument("file_path", help="Path to the pdf file to ingest")
        ingest.set_defaults(func=self.ingest_cmd)

        # ask command
        ask = subparsers.add_parser("ask", help="Ask a question")
        ask.add_argument("question", help="Question to ask")
        ask.set_defaults(func=self.ask_cmd)
        parser.add_argument("--show-logs", action="store_true", help="Display debug logs, can be used only on start up: example '-i --show-logs', '--show-logs documents")
        parser.add_argument("--interactive","-i", action="store_true", help="Interactive mode, Can be used only on start up")
        self.parser = parser


    def run(self) -> None:
        self.build_parser()
        args = self.parser.parse_args()

        self.config = Config(show_logs=args.show_logs)
        if (args.interactive):
            self.interactive_mode()
        else:    
            if not args.command:
                self.parser.print_help()
                return

            args.func(args)



def main():    
    AppContext().run()
    
    


if __name__ == "__main__":
    main()