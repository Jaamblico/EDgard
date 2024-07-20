from utils import initial_prompt
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.response_synthesizers import ResponseMode, get_response_synthesizer

# Configure response synthesizer
response_synthesizer = get_response_synthesizer(response_mode=ResponseMode.REFINE)

# Load documents and create index
documents = SimpleDirectoryReader("data").load_data()
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine(
    response_synthesizer=response_synthesizer,
    prompt_template=initial_prompt
)

# Configure response synthesizer
response_synthesizer = get_response_synthesizer(response_mode=ResponseMode.REFINE)

def respond(user_message, history):
    messages = [{"role": "system", "content": initial_prompt}]
    for user_msg, bot_msg in history:
        messages.append({"role": "user", "content": user_msg})
        if bot_msg:
            messages.append({"role": "assistant", "content": bot_msg})
    messages.append({"role": "user", "content": user_message})
    response = query_engine.query(user_message)
    history.append((user_message, str(response)))
    return history, "", history
