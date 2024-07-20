import shutil
from utils import initial_prompt
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.response_synthesizers import ResponseMode, get_response_synthesizer

# Configure response synthesizer
response_synthesizer = get_response_synthesizer(response_mode=ResponseMode.REFINE)

def upload_file(files):
    for file in files:
        shutil.copy(file, dst='./data')
    global documents, index, query_engine
    documents = SimpleDirectoryReader("data").load_data()
    index = VectorStoreIndex.from_documents(documents)
    query_engine = index.as_query_engine(
        response_synthesizer=response_synthesizer,
        prompt_template=initial_prompt
    )
    return "Files uploaded successfully!"
