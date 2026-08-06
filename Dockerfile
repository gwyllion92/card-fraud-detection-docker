# The project uses Python 3.13. The slim image is a lightweight version.
FROM python:3.13-slim

# Create the /app directory and set it as the working directory
WORKDIR /app

# Copiar el código y los archivos de configuración necesarios para pip
COPY requirements.txt pyproject.toml /app/
COPY src /app/src

# Instalar dependencias e instalar la carpeta src como paquete local editable
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del proyecto (notebooks, data, etc.)
COPY . /app/

# Declare the port exposed by the container.
EXPOSE 8888

# CMD executes Jupyter Lab when the container starts
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--ServerApp.token="]