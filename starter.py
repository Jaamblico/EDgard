import gradio as gr
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

# Load documents and create index
documents = SimpleDirectoryReader("data").load_data()
index = VectorStoreIndex.from_documents(documents)

query_engine = index.as_query_engine()

def query_llama_index(user_query):
    response = query_engine.query(user_query)
    return str(response)

# Create Gradio interface
interface = gr.Interface(
    fn=query_llama_index,
    inputs=gr.Textbox(lines=2, placeholder="Ingrese su pregunta aquí.."),
    outputs="text",
    title="EDgard",
    description="Preguntale algo a EDgard sobre los documentos cargados."
)

if __name__ == "__main__":
    interface.launch()
