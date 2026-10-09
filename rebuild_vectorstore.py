"""
Script to rebuild the FAISS vectorstore using FastEmbed (ONNX) instead of sentence-transformers.
Run this after installing fastembed: python rebuild_vectorstore.py
"""
import sys
import os
sys.path.insert(0, os.path.abspath("."))

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import FastEmbedEmbeddings

DATA_PATH = os.path.join("data", "The_GALE_ENCYCLOPEDIA_of_MEDICINE_SECOND.pdf")
DB_FAISS_PATH = os.path.join("vectorstore", "db_faiss")

print("Loading PDF...")
loader = PyPDFLoader(DATA_PATH)
documents = loader.load()
print(f"Loaded {len(documents)} pages")

print("Splitting into chunks...")
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(documents)
print(f"Created {len(chunks)} chunks")

print("Initializing FastEmbed model (BAAI/bge-small-en-v1.5)...")
embeddings = FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")

print("Building FAISS index (this may take a few minutes)...")
db = FAISS.from_documents(chunks, embeddings)

print(f"Saving FAISS index to {DB_FAISS_PATH}...")
db.save_local(DB_FAISS_PATH)
print("Done! Vectorstore rebuilt successfully.")
