
class SaveDataStep(Step):
    label = "Saving data"
    _vector_store= VectorStore()
    def execute(self, context: Dict[str, Any]) -> None:
        documents: list[Document] = context["documents"]        
        self._vector_store.saveAll(documents)