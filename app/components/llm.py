import os
from langchain_groq import ChatGroq
from app.config.config import GROQ_API_KEY
from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger = get_logger(__name__)

_llm_instance = None
_cached_model_name = None

def load_llm(model_name: str = "openai/gpt-oss-120b", groq_api_key: str = None):
    global _llm_instance, _cached_model_name
    key = groq_api_key or GROQ_API_KEY or os.environ.get("GROQ_API_KEY")
    if _llm_instance is not None and _cached_model_name == model_name:
        return _llm_instance

    try:
        logger.info("Loading LLM model: %s", model_name)
        if not key:
            raise CustomException("GROQ_API_KEY is not set. Please add it to your .env file.")

        llm = ChatGroq(
            groq_api_key=key,
            model_name=model_name,
            temperature=0.7,
            max_tokens=512,
        )
        logger.info("loaded llm successfully from groq..")
        _llm_instance = llm
        _cached_model_name = model_name
        return llm
    except Exception as e:
        error_message = CustomException("Failed to load llm model: ", e)
        logger.error(str(error_message))
        return None