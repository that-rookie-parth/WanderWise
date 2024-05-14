import concurrent.futures
import math
import os
import time
from dotenv import load_dotenv

from langchain.text_splitter import (
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter,
)
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, PodSpec

load_dotenv()
MAX_WORKERS = 6

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENV")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")

print("Creating the model.")
model_name = "avsolatorio/GIST-Embedding-v0"
model_kwargs = {"device": "cuda"}
# set True to compute cosine similarity
encode_kwargs = {"normalize_embeddings": True}
model = HuggingFaceBgeEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs,
)
print("Created the model.")

index_name = str(PINECONE_INDEX_NAME)
pc = Pinecone(api_key=PINECONE_API_KEY)

if len(pc.list_indexes().names()) > 0:
    print("Deleting the exisiting index.")
    pc.delete_index(index_name)

print("Creating the index.")
pc.create_index(
    name=index_name,
    dimension=768,
    metric="cosine",
    spec=PodSpec(
        environment=str(PINECONE_ENV),
    ),
)
print("Created the index.")

from langchain_community.document_loaders.pdf import PyPDFDirectoryLoader

def process_pdf():
    print("Processing the pdf data.")
    loader = PyPDFDirectoryLoader(
        'output/',
        glob="**/*.pdf"
    )
    pages = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        # Set a really small chunk size, just to show.
        chunk_size=1000,
        chunk_overlap=300,
        length_function=len,
        is_separator_regex=False,
    )
    splits = text_splitter.split_documents(pages)
    print("Processed the pdf data.")
    return splits


def upload_splits(splits, index):
    PineconeVectorStore.from_documents(
        splits,
        model,
        index_name=index_name,
    )
    print(f"Uploaded the split {index}")


def distribute_splits(data: list):
    global MAX_WORKERS
    MAX_WORKERS = min(len(data), MAX_WORKERS)
    print(f"data.length = {len(data)}")
    splits = []
    jump = math.ceil(len(data) / MAX_WORKERS)
    for i in range(0, len(data), jump):
        splits.append(data[i : i + jump])
    print(f"splits.length = {len(splits)}")
    print(f"splits[0].length = {len(splits[0])}")
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [
            executor.submit(upload_splits, split, i) for i, split in enumerate(splits)
        ]
        for i, future in enumerate(futures):
            if future.exception() is not None:
                print(
                    f"uploading the split {i} failed due to exception",
                    future.exception(),
                )


def main():
    pdf_splits = process_pdf()
    init_time = time.time()
    distribute_splits(pdf_splits)
    total_time = time.time() - init_time
    print(f"Total Time taken to upload the data: {total_time}")


if __name__ == "__main__":
    main()
    print("Completed!")
