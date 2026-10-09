import os
from app.components.load_pdf import load_pdf, create_text_chunks
from app.components.vector_store import save_vector_store
from app.config.config import DB_FAISS_PATH
from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger = get_logger(__name__)
def process_and_store_pdfs():
    try:
        logger.info("Starting PDF processing and vector store creation")
        documents = load_pdf()
        text_chunks = create_text_chunks(documents)
        save_vector_store(text_chunks)
        logger.info("PDF processing and vector store creation completed successfully")
    except Exception as e:
        error_message = CustomException("failed to create vector store: ", e)
        logger.error(str(error_message))
if __name__ == "__main__":#to use perticular function as main function
    process_and_store_pdfs()