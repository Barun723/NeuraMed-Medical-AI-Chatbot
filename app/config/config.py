import os
from dotenv import load_dotenv

# Absolute project root directory
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# Load .env early from BASE_DIR so GROQ_API_KEY is available regardless of import order or cwd
env_path = os.path.join(BASE_DIR, ".env")
if os.path.exists(env_path):
    load_dotenv(dotenv_path=env_path)
else:
    load_dotenv()

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

DB_FAISS_PATH = os.path.join(BASE_DIR, 'vectorstore', 'db_faiss')
DATA_PATH = os.path.join(BASE_DIR, 'data')

CHUNK_SIZE = 500
CHUNK_OVERLAP = 50