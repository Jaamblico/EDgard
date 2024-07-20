import gradio as gr
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.response_synthesizers import ResponseMode, get_response_synthesizer
import shutil

# Define el prompt inicial
initial_prompt = (
    "Sos un asistente servicial especializado en proveer respuestas detalladas y precisas "
    "basadas en los siguientes documentos. Asegurate de citar fuentes relevantes "
    "desde los documentos y proveer explicaciones entendibles. "
    "Siempre responde en español. "
)
# Load documents and create index
documents = SimpleDirectoryReader("data").load_data()
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()

# Configure response synthesizer
response_synthesizer = get_response_synthesizer(response_mode=ResponseMode.REFINE)

def upload_file(files):
    for file in files:
        shutil.copy(file, dst='./data')
        # boto3 to upload file to s3
    # Reindexar documentos después de subir archivos
    global documents, index, query_engine
    documents = SimpleDirectoryReader("data").load_data()
    index = VectorStoreIndex.from_documents(documents)
    query_engine = index.as_query_engine(
        response_synthesizer=response_synthesizer,
        prompt_template=initial_prompt
    )
    return "Files uploaded successfully!"

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

# Crear interfaz de Gradio
with gr.Blocks(theme="dark") as demo:
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
