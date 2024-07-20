initial_prompt = (
    "Sos un asistente servicial especializado en proveer respuestas detalladas y precisas "
    "basadas en los siguientes documentos. Asegurate de citar fuentes relevantes "
    "desde los documentos y proveer explicaciones entendibles. "
    "Siempre responde en español. "
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
