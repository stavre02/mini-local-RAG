class Config:
    show_logs:bool = False,
    vision_model='gemma3:4b'
    answer_model ='llama3.2:1b'
    image_to_text_prompt="""
    You are a question rephrasing system.
    Describe this image as if you are the author of a report.
    Provide an objective and detailed explanation, including key elements such as the context, purpose, and any notable features or trends that the image conveysAvoid assumptions or personal interpretations.

    Only necessary information should be added, as the output will be directly included in the report.
    Begin your response with 'Image that shows', then provide the answer immediately.
    """
    headers_to_split_on = [
            ("#", "Header 1"),
            ("##", "Header 2"),
        ]

    ## chunk size is 2056 but leave it 2000 just in case
    chunk_size=2000
    chunk_overlap=100
    retriever_path=".data/tf-idf-retriever"
    chromadb_path=".data/chroma_db"
    logs_folder =".data"
    def __init__(self,**kwargs):
        for (key,value) in kwargs.items():
            if hasattr(self,key):
                setattr(self,key,value)