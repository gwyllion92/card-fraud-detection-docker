Pipeline de Detección de Fraude en Tarjetas de Crédito 🚀
Un proyecto integral de Machine Learning diseñado para detectar transacciones fraudulentas con tarjetas de crédito mediante ingeniería de características avanzada, análisis exploratorio de datos y modelado predictivo.

El repositorio está estructurado como un paquete modular de Python (src) y completamente contenedorizado con Docker para garantizar la reproducibilidad y ejecución fluida mediante JupyterLab.

🛠️ Tecnologías y Requisitos
Lenguaje: Python 3.13

Contenedores: Docker

Librerías principales: Pandas, NumPy, Scikit-Learn, XGBoost, Matplotlib, Seaborn

Entorno: JupyterLab con instalación modular del paquete local src (pyproject.toml)

Visualización: Power BI

📁 Estructura del Repositorio
Plaintext
├── dashboards/             # Archivo .pbix de Power BI y captura de vista previa (preview.png)
├── data/                   # Directorio de datos (ver instrucciones de descarga abajo)
├── notebooks/              # Cuadernos Jupyter (EDA, Feature Engineering, Modelado y Detección de Anomalías)
├── src/                    # Paquete personalizado de Python con funciones auxiliares
│   ├── __init__.py
│   └── utils.py
├── .dockerignore           # Reglas de exclusión para Docker
├── .gitignore              # Reglas de exclusión para Git
├── Dockerfile              # Configuración de Docker para el entorno contenedorizado
├── pyproject.toml          # Configuración del paquete para instalación editable (pip install -e .)
└── requirements.txt        # Dependencias del proyecto
📊 Acceso al Dataset
Debido a los límites de tamaño de archivo en GitHub, los archivos de datos se encuentran excluidos del control de versiones.

Descargá fraudTrain.csv y fraudTest.csv desde el dataset Credit Card Fraud Detection en Kaggle.

Ubicá ambos archivos .csv dentro de la carpeta data/ antes de construir la imagen de Docker o ejecutar scripts locales.

🐳 Inicio Rápido con Docker
Construir la imagen de Docker:

Bash
docker build --no-cache -t fraud-detection-app .
Ejecutar el contenedor:

Bash
docker run -p 8888:8888 -e JUPYTER_TOKEN="tu_contraseña_aqui" fraud-detection-app
Abrir JupyterLab:
Navegá a http://localhost:8888 en tu navegador web para interactuar con los cuadernos y el entorno del proyecto.