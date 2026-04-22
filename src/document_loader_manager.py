from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


class DocumentLoaderManager:
    def __init__(self, document_path):
        self.document_path = document_path

    def load_document(self):
        """Load documents based on file type."""
        path = Path(self.document_path)
        
        # Handle single PDF file
        if path.is_file() and path.suffix.lower() == '.pdf':
            loader = PyPDFLoader(str(path))
            return loader.load()
        
        # Handle directory of PDF files
        elif path.is_dir():
            all_docs = []
            for pdf_file in path.glob('**/*.pdf'):
                loader = PyPDFLoader(str(pdf_file))
                all_docs.extend(loader.load())
            return all_docs
        
        else:
            raise ValueError(f"Invalid path or unsupported file type: {self.document_path}")
    
    def split_into_chunks(self, docs):
        rec_text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=5)
        chunks = rec_text_splitter.split_documents(docs)
        return chunks
