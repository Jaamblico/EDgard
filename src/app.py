import gradio as gr
from respond import respondFn
from upload import upload_file
from utils import js_func

# Crear interfaz de Gradio
with gr.Blocks(js=js_func) as demo:
    gr.Markdown("## Subir archivos")
    upload_button = gr.UploadButton(
        "Seleccionar archivos",
        file_types=["csv", "pdf", "txt", "doc", "docx", "json", "xls", "xlsx"],
        file_count="multiple",
    )
    file_output = gr.Textbox(label="Estado de carga:")
    upload_button.upload(upload_file, upload_button, file_output)

    gr.Markdown("## Query Interface")
    chatbot = gr.Chatbot()
    query_input = gr.Textbox(
        placeholder="Ingrese su pregunta aquí...", show_label=False
    )
    state = gr.State([])
    query_input.submit(
        respondFn, inputs=[query_input, state], outputs=[chatbot, query_input, state]
    )
    send_button = gr.Button("Enviar")
    send_button.click(
        respondFn, inputs=[query_input, state], outputs=[chatbot, query_input, state]
    )


if __name__ == "__main__":
    demo.launch()
