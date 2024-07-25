import shutil

from llama_index.core import SimpleDirectoryReader, VectorStoreIndex


def upload_file(files):
    for file in files:
        shutil.copy(file, dst="./data")
    global documents, index, query_engine
    # Load documents and create index
    documents = SimpleDirectoryReader("./data").load_data()
    index = VectorStoreIndex.from_documents(documents)
    return "Archivo subido correctamente."
