# Usa una imagen base de Python
FROM python:3.8-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia el archivo requirements.txt
COPY requirements.txt /app/

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el contenido de la carpeta actual al contenedor
COPY . /app/

# Expone el puerto 8001 (si es necesario)
EXPOSE 8001

# Define el comando de ejecución
CMD ["python", "main.py"]

