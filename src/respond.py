from utils import initial_prompt
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.response_synthesizers import (
    ResponseMode,
    get_response_synthesizer,
)
from llama_index.llms.openai import OpenAI
from llama_index.core.memory import ChatMemoryBuffer
import os

memory = ChatMemoryBuffer.from_defaults(token_limit=3900)

response_synthesizer = get_response_synthesizer(response_mode=ResponseMode.REFINE)

llm = OpenAI(model="gpt-4", temperature=0)

documents = None
index = None
chat_engine = None


def initialize_chat_engine():
    global documents, index, chat_engine
    folder = "./data"
    if not os.path.exists(folder):
        os.makedirs(folder)

    if os.listdir(folder):
        documents = SimpleDirectoryReader(folder).load_data()
    else:
        print(
            "No hay archivos en el directorio de datos. Inicializando sin documentos."
        )
        documents = []

    index = VectorStoreIndex.from_documents(documents)
    chat_engine = index.as_chat_engine(
        chat_mode="condense_question",
        memory=memory,
        llm=llm,
        verbose=True,
        response_synthesizer=response_synthesizer,
        prompt_template=initial_prompt,
    )


def respondFn(history):
    if history is None:
        history = []

    if not history:
        return history

    user_message = history[-1][0]
    response = chat_engine.chat(user_message)

    history[-1][1] = str(response)
    return history
