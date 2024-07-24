from storage import save_prompts


# Command handling functions
def handle_save_inform(user_message, saved_prompts):
    try:
        command, prompt_name, prompt_text = user_message.split(" ", 2)
        saved_prompts[prompt_name] = prompt_text
        save_prompts(saved_prompts)
        response = f"Prompt '{prompt_name}' guardado correctamente!"
    except ValueError:
        response = "Error: Debe tener este formato /guardar-informe nombre Prompt"
    return response


def handle_create_inform(user_message, saved_prompts, chat_engine):
    try:
        command, prompt_name = user_message.split(" ", 1)
        if prompt_name in saved_prompts:
            prompt_text = saved_prompts[prompt_name]
            response = chat_engine.chat(prompt_text)
        else:
            response = f"Prompt '{prompt_name}' no encontrado!"
    except ValueError:
        response = "Error: Debe tener este formato /crear-informe nombre"
    return response


def handle_list_informs(saved_prompts):
    response = "Prompts guardados:\n" + "\n".join(saved_prompts.keys())
    return response


def handle_delete_inform(user_message, saved_prompts):
    try:
        command, prompt_name = user_message.split(" ", 1)
        if prompt_name in saved_prompts:
            del saved_prompts[prompt_name]
            save_prompts(saved_prompts)
            response = f"Prompt '{prompt_name}' borrado correctamente!"
        else:
            response = f"Prompt '{prompt_name}' no encontrado!"
    except ValueError:
        response = "Error: Debe tener este formato /borrar-informe nombre"
    return response
