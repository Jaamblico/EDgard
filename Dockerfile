# Utiliza una imagen base ligera
FROM python:3.12-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos necesarios al contenedor
COPY . /app

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto en el que Gradio se ejecuta
EXPOSE 7860

# Comando para ejecutar la aplicación
CMD ["python", "starter.py"]
