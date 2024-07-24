initial_prompt = (
    "Eres un asistente servicial especializado en proporcionar respuestas detalladas y precisas "
    "basadas únicamente en los documentos indexados. Asegúrate de citar fuentes relevantes de los documentos en cada respuesta "
    "y ofrecer explicaciones claras y comprensibles. Responde siempre en español."
)

# Forces dark theme
js_func = """
function refresh() {
    const url = new URL(window.location);

    if (url.searchParams.get('__theme') !== 'dark') {
        url.searchParams.set('__theme', 'dark');
        window.location.href = url.href;
    }
}
"""
