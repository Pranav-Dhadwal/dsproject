# Customer Churn Prediction — MLOps Project

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Status](https://img.shields.io/badge/Status-In%20Progress-yellow)
![ML](https://img.shields.io/badge/Type-MLOps-orange)

## Overview
A production-grade Machine Learning project that predicts 
whether a telecom customer will churn (leave the service) 
using historical customer data. Built following MLOps 
principles — not just a notebook, but a fully structured, 
reproducible, and maintainable ML system.

---

## Problem Statement
Telecom companies lose significant revenue when customers 
switch to competitors. This project builds an ML pipeline 
that identifies **high-risk customers before they leave**, 
enabling the business to take proactive retention actions.

---

## Project Structure
```
dsproject/
├── src/dsproject/
│   ├── components/
│   │   ├── data_ingestion.py       # CSV → MySQL → Train/Test split
│   │   ├── data_transformation.py  # Encoding, scaling
│   │   ├── model_trainer.py        # Model training & selection
│   │   └── model_monitoring.py     # Performance tracking
│   ├── pipelines/
│   │   ├── training_pipeline.py    # End-to-end training flow
│   │   └── prediction_pipeline.py  # Inference pipeline
│   ├── logger.py                   # Timestamped logging
│   ├── exception.py                # Custom exception handling
│   └── utils.py                    # Reusable utilities
├── data/
│   ├── raw/                        # Raw ingested data
│   └── processed/                  # Train/test splits
├── notebooks/
│   └── eda.ipynb                   # Exploratory data analysis
├── logs/                           # Auto-generated log files
├── template.py                     # Project structure automation
├── setup.py                        # Package configuration
└── requirements.txt                # Dependencies
```

---

## Dataset
- **Source:** Telco Customer Churn (Kaggle)
- **Records:** 7,043 customers
- **Features:** 21 columns
- **Target:** `Churn` — Yes/No
- **Class Distribution:** 73.5% No Churn / 26.5% Churn

---

## Tech Stack
| Category | Tools |
|---|---|
| Language | Python 3.10 |
| Data Processing | Pandas, NumPy |
| Visualization | Matplotlib, Seaborn |
| ML | Scikit-learn |
| Database | MySQL |
| ORM | SQLAlchemy |
| Experiment Tracking | MLflow (Phase 2) |
| Data Versioning | DVC (Phase 2) |
| Version Control | Git & GitHub |
| Environment | virtualenv |

---

## Key Findings from EDA
- **42%** of month-to-month customers churn vs only **3%** on 2-year contracts
- Customers in their **first 12 months** are at highest risk
- High monthly charges (**$70+**) correlate with higher churn
- Customers **without tech support** are significantly more likely to leave
- **Tenure** is the strongest predictor of churn (correlation: -0.35)

---

## MLOps Features
- ✅ Automated project structure generation
- ✅ Timestamped logging system
- ✅ Custom exception handling with file & line tracking
- ✅ MySQL data ingestion pipeline
- ✅ Stratified train/test splitting
- ✅ Modular component-based architecture
- ✅ Reusable model evaluation utilities
- 🔄 DVC data versioning (coming in Phase 2)
- 🔄 MLflow experiment tracking (coming in Phase 2)

---

## Setup & Installation
```bash
# Clone the repository
git clone https://github.com/Pranav-Dhadwal/dsproject.git
cd dsproject

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### Configure environment variables
Create a `.env` file in the project root:
```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_DATABASE=churn_db
```

### Run data ingestion
```bash
python src/dsproject/components/data_ingestion.py
```

### Run EDA notebook
```bash
jupyter notebook notebooks/eda.ipynb
```

---

## Project Roadmap
- [x] Phase 1 — Project setup, logging, data ingestion, EDA
- [ ] Phase 2 — Data transformation, model training, MLflow
- [ ] Phase 3 — Prediction pipeline, Flask app, deployment

---

## Author
**Pranav Dhadwal**
- GitHub: [@Pranav-Dhadwal](https://github.com/Pranav-Dhadwal)
- Email: dhadwal.pranav01@gmail.com

---

*Industrial Training Project — MCA 4th Semester, IUHP*