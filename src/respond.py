from commands import (
    handle_create_inform,
    handle_delete_inform,
    handle_list_informs,
    handle_save_inform,
)
from utils import initial_prompt
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.response_synthesizers import (
    ResponseMode,
    get_response_synthesizer,
)
from llama_index.llms.openai import OpenAI
from llama_index.core.memory import ChatMemoryBuffer

memory = ChatMemoryBuffer.from_defaults(token_limit=3900)

response_synthesizer = get_response_synthesizer(response_mode=ResponseMode.REFINE)

llm = OpenAI(model="gpt-4", temperature=0)

documents = SimpleDirectoryReader("./data").load_data()
index = VectorStoreIndex.from_documents(documents)
chat_engine = index.as_chat_engine(
    chat_mode="condense_question",
    memory=memory,
    llm=llm,
    verbose=True,
    response_synthesizer=response_synthesizer,
    prompt_template=initial_prompt,
)

response_synthesizer = get_response_synthesizer(response_mode=ResponseMode.REFINE)


def respondFn(user_message, history):
    global saved_prompts

    print(user_message)

    # TODO: Terminar. No funciona, si podes guardar pero no podes ejecutar nada
    if user_message.startswith("/guardar-prompt"):
        response = handle_save_inform(user_message, saved_prompts)
    elif user_message.startswith("/crear-prompt"):
        response = handle_create_inform(user_message, saved_prompts, chat_engine)
    elif user_message.startswith("/listar-prompts"):
        response = handle_list_informs(saved_prompts)
    elif user_message.startswith("/borrar-prompt"):
        response = handle_delete_inform(user_message, saved_prompts)
    elif user_message.startswith("/ejecutar-prompt"):
        command, prompt_name = user_message.split(" ", 1)
        if prompt_name in saved_prompts:
            prompt_text = saved_prompts[prompt_name]
            response = chat_engine.chat(prompt_text)
        else:
            response = f"Prompt '{prompt_name}' no encontrada."
    else:
        messages = [{"role": "system", "content": initial_prompt}]
        for user_msg, bot_msg in history:
            messages.append({"role": "user", "content": user_msg})
            if bot_msg:
                messages.append({"role": "assistant", "content": bot_msg})
        messages.append({"role": "user", "content": user_message})
        response = chat_engine.chat(user_message)

    history.append((user_message, str(response)))
    return history, "", history
