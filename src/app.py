import gradio as gr
from upload import upload_file
from respond import respond
from utils import js_func

# Crear interfaz de Gradio
with gr.Blocks(js=js_func) as demo:
    gr.Markdown("## File Upload Interface")
    upload_button = gr.UploadButton("Click to Upload a File", file_types=["csv", "pdf", "txt", "docx", "json"], file_count="multiple")
    file_output = gr.Textbox(label="File Upload Status")
    upload_button.upload(upload_file, upload_button, file_output)

    gr.Markdown("## Query Interface")
    chatbot = gr.Chatbot()
    query_input = gr.Textbox(placeholder="Ingrese su pregunta aquí...", show_label=False)
    state = gr.State([])
    query_input.submit(respond, inputs=[query_input, state], outputs=[chatbot, query_input, state])
    send_button = gr.Button("Enviar")
    send_button.click(respond, inputs=[query_input, state], outputs=[chatbot, query_input, state])

if __name__ == "__main__":
    demo.launch()
