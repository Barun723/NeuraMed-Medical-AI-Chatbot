from langchain_community.vectorstores import FAISS
import os
from app.common.logger import get_logger
from app.common.custom_exception import CustomException
from app.components.embeddings import get_embedding_model
from app.config.config import DB_FAISS_PATH

logger = get_logger(__name__)

_vector_store = None

def load_vector_store(force_reload: bool = False):  # existing vector store use
    global _vector_store
    if _vector_store is not None and not force_reload:
        return _vector_store
    try:
        embedding_model = get_embedding_model()  # initialize embedding model
        if os.path.exists(DB_FAISS_PATH):
            logger.info(" loaded existing vector store successfully")
            _vector_store = FAISS.load_local(DB_FAISS_PATH, embedding_model, allow_dangerous_deserialization=True)
            return _vector_store
        else:
            logger.warning("No existing vector store found at %s.", DB_FAISS_PATH)
            return None
    except Exception as e:
        error_message = CustomException("Error loading FAISS vector store: ", e)
        logger.error(str(error_message))
        raise error_message

def save_vector_store(text_chunks):  # create vector store to use
    global _vector_store
    try:
        if not text_chunks:
            raise CustomException("No text chunks provided for vector store creation.")
        embedding_model = get_embedding_model()
        logger.info("Creating FAISS vector store from text chunks")
        db = FAISS.from_documents(text_chunks, embedding_model)
        logger.info("Saving FAISS vector store....")
        db.save_local(DB_FAISS_PATH)
        logger.info("FAISS vector store saved successfully")
        _vector_store = db
        return db
    except Exception as e:
        error_message = CustomException("Error saving FAISS vector store: ", e)
        logger.error(str(error_message))
        raise error_message
