
import gradio as gr
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.response_synthesizers import ResponseMode, get_response_synthesizer
import shutil

# Define el prompt inicial
initial_prompt = "Quiero que tus respuestas tengan el tono de sherlock holmes."

# Load documents and create index
documents = SimpleDirectoryReader("data").load_data()
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()

# Configure response synthesizer
response_synthesizer = get_response_synthesizer(response_mode=ResponseMode.COMPACT)

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

def query_llama_index(user_query):
    response = query_engine.query(user_query)
    return str(response)

# Crear interfaz de Gradio
with gr.Blocks() as demo:
    gr.Markdown("## File Upload Interface")
    upload_button = gr.UploadButton("Click to Upload a File", file_types=["csv", "pdf", "txt", "docx", "json"], file_count="multiple")
    file_output = gr.Textbox(label="File Upload Status")
    upload_button.upload(upload_file, upload_button, file_output)

    gr.Markdown("## Query Interface")
    query_input = gr.Textbox(lines=2, placeholder="Ingrese su pregunta aquí..")
    query_output = gr.Textbox(label="Respuesta")
    query_button = gr.Button("Query")
    query_button.click(query_llama_index, inputs=query_input, outputs=query_output)


if __name__ == "__main__":
    demo.launch()
