# El proyecto utiliza Python 3.13. La imagen slim es una versión ligera y optimizada.
FROM python:3.13-slim

# Crear el directorio /app y establecerlo como el directorio de trabajo
WORKDIR /app

# Copiar el código y los archivos de configuración necesarios para pip
COPY requirements.txt pyproject.toml /app/
COPY src /app/src

# Instalar dependencias e instalar la carpeta src como paquete local editable
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del proyecto (notebooks, data, etc.)
COPY . /app/

# Declarar el puerto expuesto por el contenedor
EXPOSE 8888

# Usar ejecución mediante shell (sh -c) para expandir dinámicamente variables de entorno ($JUPYTER_TOKEN) en tiempo de ejecución, evitando exponer contraseñas estáticas en GitHub
CMD ["sh", "-c", "jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root --IdentityProvider.token=$JUPYTER_TOKEN"]