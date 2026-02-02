import argparse
import shlex
import sys
from typing import Optional

from mini_local_rag.config import Config
from mini_local_rag.pipeline_builder import PipelineBuilder
from rich import print as rprint


class AppContext:
    """Handles the context for the application, including argument parsing and interactive mode."""

    config: Optional[Config]
    parser: Optional[argparse.ArgumentParser]
    builder: Optional[PipelineBuilder]



    def documents_cmd(self,args: argparse.Namespace) -> None:
        """Handle the 'documents' command: list all documents."""

        self.get_builder().get_documents().execute()

    def ingest_cmd(self,args: argparse.Namespace) -> None:
        """Handle the 'ingest' command: ingest a document from the given file path."""

        self.get_builder().get_ingestion_pipeline(file_path=args.file_path).execute()

    def ask_cmd(self,args: argparse.Namespace) -> None:
        """Handle the 'ask' command: process the given question."""

        self.get_builder().get_ask_pipeline(question=args.question).execute()

    def interactive_mode(self)->None:
        """Start an interactive mode for the user to input commands."""

        rprint("Entering interactive mode. Type 'exit' to quit.")
        
        while True:
            try:
                user_input = input(">>> ")

                if user_input.lower() == 'exit':
                    rprint("Exiting interactive mode.")
                    break

                    
                args_list = shlex.split(user_input)
                args = self.parser.parse_args(args=args_list)
                self.config.show_logs=args.show_logs

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
        """Lazy load the PipelineBuilder, if it's not already initialized.Use only one instance """

        if not hasattr(self,"builder"):
            self.builder = PipelineBuilder(config=self.config)
            return self.builder
        return self.builder

    def build_parser(self) -> None:
        """Build and configure the argument parser with subcommands."""

        prog ="" if '-i' in sys.argv or '--interactive' in sys.argv else None
            
        parser = argparse.ArgumentParser(
                description="Pipeline command line interface for processing PDF reports and as questions.",
                prog=prog
            )
        subparsers = parser.add_subparsers(dest="command")
        
        # documents command
        documents = subparsers.add_parser("documents", help="List all documents by path")
        documents.add_argument("--show-logs", action="store_true", help="Display debug logs")
        documents.set_defaults(func=self.documents_cmd)
        
        # ingest command
        ingest = subparsers.add_parser("ingest", help="Ingest a document")
        ingest.add_argument("file_path", help="Path to the pdf file to ingest")
        ingest.add_argument("--show-logs", action="store_true", help="Display debug logs")
        ingest.set_defaults(func=self.ingest_cmd)

        # ask command
        ask = subparsers.add_parser("ask", help="Ask a question")
        ask.add_argument("question", help="Question to ask")
        ask.add_argument("--show-logs", action="store_true", help="Display debug logs")
        ask.set_defaults(func=self.ask_cmd)

        parser.add_argument("--interactive","-i", action="store_true", help="Interactive mode, Can be used only on start up")
        self.parser = parser


    def run(self) -> None:
        """Run the application: build the parser, parse arguments, and execute commands."""

        self.build_parser()
        args = self.parser.parse_args()


        # add this to true if ./data/models exists with docling models
        # if false it will download them, I added it because of vpn issues when running locally
        self.config = Config(enable_local_models =False)
        
        if (args.interactive):
            self.interactive_mode()
        else:    
            if not args.command:
                self.parser.print_help()
                return
            self.config.show_logs=args.show_logs
            args.func(args)



def main():
    """Main entry point of the application."""
    
    AppContext().run()
    
    


if __name__ == "__main__":
    main()