import os
import tempfile
from langchain_community.document_loaders import PyPDFLoader, UnstructuredWordDocumentLoader, TextLoader
from core.exceptions import IngestionError
from core.logger import setup_logger

logger = setup_logger("ingestion_layer")

class DocumentIngestionLayer:
    """
    Production ingestion engine preserving physical document structure using 
    LangChain native architecture wrappers.
    """
    
    @staticmethod
    def load_document(file_bytes: bytes, filename: str) -> str:
        ext = os.path.splitext(filename)[1].lower()
        logger.info(f"Ingesting file: {filename} with extension: {ext}")
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp_file:
            tmp_file.write(file_bytes)
            tmp_path = tmp_file.name

        try:
            if ext == ".pdf":
                loader = PyPDFLoader(tmp_path)
            elif ext in [".docx", ".doc"]:
                loader = UnstructuredWordDocumentLoader(tmp_path)
            elif ext == ".txt":
                loader = TextLoader(tmp_path, encoding="utf-8")
            else:
                raise IngestionError(f"Unsupported extension: {ext}")

            docs = loader.load()
            full_text = "\n\n".join([doc.page_content for doc in docs])
            
            if not full_text.strip():
                raise IngestionError("The extracted document context is empty.")
                
            return full_text
            
        except Exception as e:
            logger.error(f"Failed parsing document {filename}: {str(e)}")
            raise IngestionError(f"Failed to process {filename}: {str(e)}")
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)