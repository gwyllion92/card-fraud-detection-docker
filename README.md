## Credit Card Fraud Detection Pipeline 🚀
An end-to-end Machine Learning project designed to detect fraudulent credit card transactions using advanced feature engineering, exploratory data analysis, and predictive modeling.

The repository is structured as a modular Python package (src) and fully containerized with Docker to ensure reproducibility and seamless execution via JupyterLab.

## 🛠️ Tech Stack & Requirements
Language: Python 3.13

Containerization: Docker

Libraries: Pandas, NumPy, Scikit-Learn, XGBoost, Matplotlib, Seaborn

Environment: JupyterLab with modular src package setup (pyproject.toml)

📁 Repository Structure
```text
├── data/                   # Dataset directory (see download instructions below)
├── notebooks/              # Jupyter notebooks for EDA, feature engineering & modeling
├── src/                    # Custom Python package with helper utilities
│   ├── __init__.py
│   └── utils.py
├── .dockerignore           # Docker ignore rules
├── .gitignore              # Git ignore rules
├── Dockerfile              # Docker configuration for containerized environment
├── pyproject.toml          # Package configuration for editable installation
└── requirements.txt        # Project dependencies
```

## 📊 Dataset Access
Due to GitHub file size limits, dataset files are excluded from version control.

1. Download `fraudTrain.csv` and `fraudTest.csv` from the [Credit Card Fraud Detection Dataset on Kaggle](https://www.kaggle.com/datasets/kartik2112/fraud-detection).
2. Place both `.csv` files inside the `data/` directory before building the Docker image or running local scripts.

Place both .csv files inside the data/ directory before building the Docker image or running local scripts.

## 🐳 Quickstart with Docker
1. Build the Docker Image
```bash
docker build --no-cache -t fraud-detection-app .
```

2. Run the Container
```bash
docker run -p 8888:8888 fraud-detection-app
```

3. Open JupyterLab
Navigate to http://localhost:8888 in your web browser to interact with the notebooks and project environment.