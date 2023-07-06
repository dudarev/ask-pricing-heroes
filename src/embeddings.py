"""
Based on
https://python.langchain.com/en/latest/modules/chains/index_examples/vector_db_qa_with_sources.html
"""
import json
from pathlib import Path

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma

from sources import SOURCES_DATA_FILE, get_sources_dict

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

CHROMA_DATA_DIR = Path(__file__).parent.parent / "data/chroma"
CHROMA_DATA_DIR.mkdir(exist_ok=True, parents=True)


def create_embeddings_and_sources():
    sources_dict = get_sources_dict()
    embeddings = OpenAIEmbeddings()
    vectordb = Chroma.from_texts(
        list(sources_dict.values()),
        embeddings,
        metadatas=[{"source": source} for source in sources_dict.keys()],
        persist_directory=str(CHROMA_DATA_DIR),
    )
    vectordb.persist()

    SOURCES_DATA_FILE.write_text(json.dumps(sources_dict))


if __name__ == "__main__":
    create_embeddings_and_sources()
