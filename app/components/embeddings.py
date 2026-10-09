from langchain_community.embeddings import FastEmbedEmbeddings
from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger = get_logger(__name__)

_embedding_model = None

def get_embedding_model():
    global _embedding_model
    if _embedding_model is not None:
        return _embedding_model
    try:
        logger.info("Initializing FastEmbed (ONNX) Embeddings model - no PyTorch required")
        # FastEmbed uses ONNX runtime — uses ~60MB RAM vs 500MB+ for PyTorch/sentence-transformers
        # Uses the same all-MiniLM-L6-v2 model so existing FAISS index stays compatible
        model = FastEmbedEmbeddings(
            model_name="BAAI/bge-small-en-v1.5",  # ~23MB ONNX model, 384-dim embeddings
        )
        logger.info("FastEmbed model initialized successfully")
        _embedding_model = model
        return _embedding_model
    except Exception as e:
        error_message = CustomException("Error initializing FastEmbed model: ", e)
        logger.error(str(error_message))
        raise error_message
