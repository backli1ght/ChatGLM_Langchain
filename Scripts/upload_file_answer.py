# import time
#
# import os
# import gradio as gr
# from langchain_community.document_loaders import DirectoryLoader
# from langchain_community.llms import ChatGLM
# from langchain.prompts import PromptTemplate
# from langchain.text_splitter import CharacterTextSplitter
# from langchain.embeddings.huggingface import HuggingFaceEmbeddings
# from langchain_community.vectorstores import Chroma
# from langchain.chains import RetrievalQA
#
# # 加载embedding
# embedding_model_dict = {
#     "ernie-tiny": "nghuyong/ernie-3.0-nano-zh",
#     "ernie-base": "nghuyong/ernie-3.0-base-zh",
#     "text2vec": "GanymedeNil/text2vec-large-chinese",
#     "text2vec2": "uer/sbert-base-chinese-nli",
#     "text2vec3": "shibing624/text2vec-base-chinese",
# }
#
#
# def load_documents(directory="documents"):
#     """
#     加载books下的文件，进行拆分
#     :param directory:
#     :return:
#     """
#     loader = DirectoryLoader(directory)
#     documents = loader.load()
#     text_spliter = CharacterTextSplitter(chunk_size=256, chunk_overlap=0)
#     split_docs = text_spliter.split_documents(documents)
#     return split_docs
#
#
# def load_embedding_model(model_name="ernie-tiny"):
#     """
#     加载embedding模型
#     :param model_name:
#     :return:
#     """
#     encode_kwargs = {"normalize_embeddings": False}
#     model_kwargs = {"device": "cuda:0"}
#     return HuggingFaceEmbeddings(
#         model_name=embedding_model_dict[model_name],
#         model_kwargs=model_kwargs,
#         encode_kwargs=encode_kwargs
#     )
#
#
# def store_chroma(docs, embeddings, persist_directory="VectorStore"):
#     """
#     讲文档向量化，存入向量数据库
#     :param docs:
#     :param embeddings:
#     :param persist_directory:
#     :return:
#     """
#     db = Chroma.from_documents(docs, embeddings, persist_directory=persist_directory)
#     db.persist()
#     return db
#
#
# # 加载embedding模型
# embeddings = load_embedding_model('text2vec3')
# # embeddings = load_embedding_model('text2vec3')
# # 加载数据库
# if not os.path.exists('VectorStore'):
#     documents = load_documents()
#     db = store_chroma(documents, embeddings)
# else:
#     db = Chroma(persist_directory='VectorStore', embedding_function=embeddings)
# # 创建llm
# llm = ChatGLM(
#     endpoint_url='http://127.0.0.1:8000',
#     max_token=80000,
#     top_p=0.9
# )
# # # 创建qa
# # QA_CHAIN_PROMPT = PromptTemplate.from_template("""根据下面的上下文（context）内容回答问题。
# # 如果你不知道答案，就回答不知道，不要试图编造答案。
# # 答案最多3句话，保持答案简洁。
# # 总是在答案结束时说”谢谢你的提问！“
# # {context}
# # 问题：{question}
# # """)
#
# QA_CHAIN_PROMPT = PromptTemplate.from_template(
#     """Answer the question according to the context below.
# If you don't know the answer, answer no and don't try to make it up.
# 3 sentences maximum. Keep your answers brief.
# Always end your answer by saying "Thank you for asking! "
# {context}
# 问题：{question}
# """)
#
# retriever = db.as_retriever()
# qa = RetrievalQA.from_chain_type(
#     llm=llm,
#     retriever=retriever,
#     verbose=True,
#     chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
# )
#
#
# def add_text(history, text):
#     history = history + [(text, None)]
#     return history, gr.update(value="", interactive=False)
#
#
# def add_file(history, file):
#     """
#     上传文件后的回调函数，将上传的文件向量化存入数据库
#     :param history:
#     :param file:
#     :return:
#     """
#     global qa
#     directory = os.path.dirname(file.name)
#     documents = load_documents(directory)
#     db = store_chroma(documents, embeddings)
#     retriever = db.as_retriever()
#     qa.retriever = retriever
#     history = history + [((file.name,), None)]
#     return history
#
#
# def bot(history):
#     """
#     聊天调用的函数
#     :param history:
#     :return:
#     """
#     message = history[-1][0]
#     if isinstance(message, tuple):
#         response = "文件上传成功！！"
#     else:
#         response = qa({"query": message})['result']
#     history[-1][1] = ""
#     for character in response:
#         history[-1][1] += character
#         time.sleep(0.05)
#         yield history
#
#
# with gr.Blocks() as demo:
#     chatbot = gr.Chatbot(
#         [],
#         elem_id="chatbot",
#         bubble_full_width=False,
#         avatar_images=(None, (os.path.join(os.path.dirname(__file__), "avatar.png"))),
#     )
#
#     with gr.Row():
#         txt = gr.Textbox(
#             scale=4,
#             show_label=False,
#             placeholder="Enter text and press enter, or upload an image",
#             container=False,
#         )
#         btn = gr.UploadButton("📁", file_types=['txt'])
#
#     txt_msg = txt.submit(add_text, [chatbot, txt], [chatbot, txt], queue=False).then(
#         bot, chatbot, chatbot
#     )
#     txt_msg.then(lambda: gr.update(interactive=True), None, [txt], queue=False)
#     file_msg = btn.upload(add_file, [chatbot, btn], [chatbot], queue=False).then(
#         bot, chatbot, chatbot
#     )
#
# demo.queue()
# if __name__ == "__main__":
#     demo.launch()

import time
import os
import gradio as gr
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.llms import ChatGLM
from langchain.prompts import PromptTemplate
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA


# Load embedding model
embedding_model_dict = {
    "ernie-tiny": "nghuyong/ernie-3.0-nano-zh",
    "ernie-base": "nghuyong/ernie-3.0-base-zh",
    "text2vec": "GanymedeNil/text2vec-large-chinese",
    "text2vec2": "uer/sbert-base-chinese-nli",
    "text2vec3": "shibing624/text2vec-base-chinese",
}


def load_documents(directory="documents"):
    """
    Load files in the 'documents' directory and split them.
    :param directory: The directory containing the documents.
    :return: A list of loaded documents.
    """
    loader = DirectoryLoader(directory)
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=256, chunk_overlap=0)
    split_docs = text_splitter.split_documents(documents)
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
        encode_kwargs=encode_kwargs,
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


# Load embedding model
embeddings = load_embedding_model("text2vec3")

# Load vector database
if not os.path.exists("VectorStore"):
    documents = load_documents()
    db = store_chroma(documents, embeddings)
else:
    db = Chroma(persist_directory="VectorStore", embedding_function=embeddings)

# Create LLM
llm = ChatGLM(
    endpoint_url="http://127.0.0.1:8000",
    max_token=80000,
    top_p=0.9,
)

# Create QA chain prompt
QA_CHAIN_PROMPT = PromptTemplate.from_template(
    """Answer the question according to the context below.
If you don't know the answer, answer no and don't try to make it up.
3 sentences maximum. Keep your answers brief.
Always end your answer by saying "Thank you for asking!".
{context}
Question: {question}
"""
)

retriever = db.as_retriever()
qa = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    verbose=True,
    chain_type_kwargs={"prompt": QA_CHAIN_PROMPT},
)


def add_text(history, text):
    history = history + [(text, None)]
    return history, gr.update(value="", interactive=False)


def add_file(history, file):
    """
    Upload the file and vectorize it for storage in the database.
    :param history: The chat history.
    :param file: The file to upload.
    :return: The updated chat history.
    """
    global qa
    directory = os.path.dirname(file.name)
    documents = load_documents(directory)
    db = store_chroma(documents, embeddings)
    retriever = db.as_retriever()
    qa.retriever = retriever
    history = history + [((file.name,), None)]
    return history


def bot(history):
    """
    Function for chat interaction.
    :param history: The chat history.
    :return: The updated chat history with the response.
    """
    message = history[-1][0]
    if isinstance(message, tuple):
        response = "File uploaded successfully!"
    else:
        response = qa({"query": message})["result"]
    history[-1][1] = ""
    for character in response:
        history[-1][1] += character
        time.sleep(0.05)
        yield history


# Build the Gradio interface
with gr.Blocks() as demo:
    chatbot = gr.Chatbot(
        [],
        elem_id="chatbot",
        show_label=False,
        bubble_full_width=True,
        avatar_images=(None, None),
    )

    with gr.Row():
        txt = gr.Textbox(
            placeholder="Enter text and press enter, or upload a file",
            container=False,
            show_label=False,
        )
        btn = gr.UploadButton("📁", file_types=["txt"])

    txt_msg = txt.submit(add_text, [chatbot, txt], [chatbot, txt], queue=False).then(
        bot, chatbot, chatbot
    )
    txt_msg.then(lambda: gr.update(interactive=True), None, [txt], queue=False)

    file_msg = btn.upload(add_file, [chatbot, btn], [chatbot], queue=False).then(
        bot, chatbot, chatbot
    )

    gr.Markdown("## Local Knowledge-Based LLM Q&A Application")
    gr.Markdown(
        "This application allows users to upload files and ask questions based on their content."
    )

demo.queue()
if __name__ == "__main__":
    demo.launch()
