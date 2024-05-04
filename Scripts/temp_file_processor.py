import os

from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
# 加载embedding
embedding_model_dict = {
    "ernie-tiny": "nghuyong/ernie-3.0-nano-zh",
    "ernie-base": "nghuyong/ernie-3.0-base-zh",
    "text2vec": "GanymedeNil/text2vec-large-chinese",
    "text2vec2": "uer/sbert-base-chinese-nli",
    "text2vec3": "shibing624/text2vec-base-chinese",
}

def load_documents(directory="books"):
    """
    Load files under the 'books' directory and split them.
    :param directory: The path to the directory containing the documents.
    :return: A list of loaded documents.
    """
    loader = DirectoryLoader(directory)  # Specify encoding here
    documents = loader.load()
    text_spliter = CharacterTextSplitter(chunk_size=256, chunk_overlap=0)
    split_docs = text_spliter.split_documents(documents)
    return split_docs


def load_embedding_model(model_name="ernie-tiny"):
    """
    Load the embedding model.
    :param model_name: The name of the model to load.
    :return: The loaded model.
    """
    encode_kwargs = {"normalize_embeddings": False}
    model_kwargs = {"device": "cuda:0"}
    return HuggingFaceEmbeddings(
        model_name=embedding_model_dict[model_name],
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )

def store_chroma(docs, embeddings, persist_directory="VectorStore"):
    """
    Vectorize the documents and store them in the vector database.
    :param docs: The documents to vectorize.
    :param embeddings: The embeddings to use for vectorization.
    :param persist_directory: The directory to store the vector database.
    :return: The vector database.
    """
    db = Chroma.from_documents(docs, embeddings, persist_directory=persist_directory)
    db.persist()
    return db


embeddings = load_embedding_model('text2vec3')
if not os.path.exists('VectorStore'):
    documents = load_documents()
    db = store_chroma(documents, embeddings)
else:
    db = Chroma(persist_directory = 'VectorStore', embedding_function = embeddings)