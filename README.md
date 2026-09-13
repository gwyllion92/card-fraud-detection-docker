# Pipeline de Detección de Fraude en Tarjetas de Crédito 💳

Proyecto integral de Machine Learning diseñado para detectar transacciones fraudulentas con tarjetas de crédito mediante ingeniería de características avanzada, análisis exploratorio de datos y modelado predictivo.

El repositorio incluye un paquete Python local (`src/utils.py`) con funciones reutilizables para el pipeline de datos, y está completamente contenedorizado con Docker para garantizar la reproducibilidad y ejecución fluida mediante JupyterLab.


## 🛠️ Tecnologías y Requisitos

- **Lenguaje:** Python 3.13
- **Contenedores:** Docker
- **Librerías principales:** Pandas, NumPy, Scikit-Learn, XGBoost, Matplotlib, Seaborn
- **Entorno:** JupyterLab, con el paquete local `src` instalado en modo editable (vía `pyproject.toml`)
- **Visualización:** Power BI

## 📁 Estructura del Repositorio

```
├── dashboard/              # Archivo .pbix de Power BI y captura de vista previa
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
```

## 📓 Notebooks

1. **01_EDA.ipynb:** Análisis exploratorio: patrones de fraude por hora, categoría y monto.
2. **02_Feature_Engineering.ipynb:** Transformación de variables: distancia Haversine, variables temporales, encoding.
3. **03_Modeling.ipynb:** Modelado supervisado: Regresión Logística (baseline) y XGBoost, con selección de threshold vía validación cruzada estratificada (K-folds).
4. **04_Anomaly_Detection.ipynb:** Detección no supervisada con Isolation Forest.
5. **05_Advanced_Anomaly_Detection.ipynb:** Detección no supervisada con Local Outlier Factor (LOF).

## 📈 Resultados Principales

| Modelo | Precision (Fraude) | Recall (Fraude) | F1-score |
|---|---|---|---|
| Regresión Logística (baseline) | 0.02 | 0.74 | 0.04 |
| XGBoost (threshold 0.80) | 0.52 | 0.89 | 0.65 |
| Isolation Forest | — | 0.0196–0.0210 | — |
| Local Outlier Factor | — | 0.1949 | — |

XGBoost fue el modelo más efectivo para producción, superando ampliamente al baseline de Regresión Logística. Los enfoques no supervisados mostraron rendimiento limitado, ya que el fraude en este dataset no siempre se manifiesta como una anomalía estadística, reforzando su rol como complemento (detección de fraude "zero-day") más que como enfoque principal.

## ⚠️ Nota Metodológica

Durante el desarrollo se identificaron y corrigieron dos casos de data leakage: (1) selección del threshold de clasificación evaluando directamente sobre el conjunto de test, y (2) entrenamiento y evaluación de los modelos no supervisados sobre el mismo conjunto de datos combinado (train+test). Ambos fueron corregidos separando estrictamente train/test en cada etapa del pipeline — un ejercicio que reforzó la importancia de la validación rigurosa en proyectos de detección de fraude, donde las métricas infladas pueden llevar a decisiones costosas en producción.   


## 📊 Acceso al Dataset

Debido a los límites de tamaño de archivo en GitHub, los archivos de datos se encuentran excluidos del control de versiones.

- Descargá `fraudTrain.csv` y `fraudTest.csv` desde el dataset [Credit Card Transactions Fraud Detection Dataset](https://www.kaggle.com/datasets/kartik2112/fraud-detection) en Kaggle.
- Ubicá ambos archivos `.csv` dentro de la carpeta `data/` antes de construir la imagen de Docker o ejecutar scripts locales.

## 🐳 Inicio Rápido con Docker

**Construir la imagen de Docker:**
```bash
docker build --no-cache -t fraud-detection-app .
```

**Ejecutar el contenedor:**
```bash
docker run -d -p 8888:8888 -e JUPYTER_TOKEN="tu_contraseña_aqui" --name fraud-app fraud-detection-app
```

**Abrir JupyterLab:**
Navegá a http://localhost:8888 en tu navegador web para interactuar con los cuadernos y el entorno del proyecto.