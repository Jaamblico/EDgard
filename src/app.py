import gradio as gr
from respond import respondFn, initialize_chat_engine
from upload import upload_file
from utils import js_func
import os

initialize_chat_engine()


def print_like_dislike(x: gr.LikeData):
    print(x.index, x.value, x.liked)


def handle_text_and_file(history, chatInput):
    if history is None:
        history = []

    files = chatInput.get("files", [])
    text = chatInput.get("text", "")

    for file_path in files:
        file_url, file_name = upload_file(file_path)
        file_link = f"<a href='{file_url}' download>{file_name}</a>"
        history.append([file_link, None])

    if text:
        history.append([text, None])
        history = respondFn(history)

    return history, {"text": "", "files": None}


with gr.Blocks(js=js_func, fill_height=True) as demo:
    chatbot = gr.Chatbot(
        elem_id="chatbot",
        bubble_full_width=False,
        scale=1,
    )
    chat_input = gr.MultimodalTextbox(
        interactive=True,
        placeholder="Ingrese su mensaje o suba un archivo...",
        show_label=False,
    )
    chat_input.submit(
        handle_text_and_file,
        [chatbot, chat_input],
        [chatbot, chat_input],
    )

    chatbot.like(print_like_dislike, None, None)

demo.queue()
if __name__ == "__main__":
    demo.launch()
