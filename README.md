# 🚀 ETL ML Pipeline Auto Config Generator

An end-to-end **Machine Learning + ETL Pipeline System** that automatically predicts optimal pipeline configurations and generates production-ready YAML files based on input schema.

It also includes:

* Flask API backend
* ML model training pipeline
* SQLite-based lineage tracking
* Automated CI/CD using GitHub Actions
* Full test coverage with pytest

---

## 📌 Features

* 🔹 Automatic pipeline type prediction using ML (Random Forest)
* 🔹 YAML configuration generator for ETL workflows
* 🔹 REST API using Flask
* 🔹 Pipeline lineage tracking (SQLite DB)
* 🔹 Rollback support for pipeline runs
* 🔹 Automated ML model training
* 🔹 Unit testing with pytest
* 🔹 CI/CD pipeline using GitHub Actions
* 🔹 Code coverage enforcement

---

## 🧠 Tech Stack

* Python 3.10
* Flask
* Scikit-learn
* Pandas, NumPy
* PyYAML
* SQLite
* Pytest
* GitHub Actions (CI/CD)

---

## 📁 Project Structure

```
etl_ml_pipeline/
│
├── app/
│   ├── db.py
│   ├── ml_model.py
│   ├── routes.py
│   ├── yaml_generator.py
│
├── data/
│   └── training_data.csv
│
├── models/
│   ├── rf_model.pkl
│   └── encoders.pkl
│
├── tests/
│   ├── test_model.py
│   └── test_routes.py
│
├── .github/workflows/
│   └── ci.yml
│
├── run.py
├── requirements.txt
├── pipeline_lineage.db
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/sreeja-coder123/etl_ml_pipeline.git
cd etl_ml_pipeline
```

---

### 2. Create virtual environment (optional but recommended)

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🚀 Run the Project

### Start Flask server:

```bash
python run.py
```

Server runs at:

```
http://127.0.0.1:5000
```

---

## 📡 API Endpoints

### 🔹 Health Check

```http
GET /health
```

Response:

```json
{ "status": "ok" }
```

---

### 🔹 Generate Pipeline

```http
POST /generate-pipeline
```

Example request:

```json
{
  "table_name": "orders",
  "source_type": "postgres",
  "volume_gb": 2.5,
  "update_frequency_hrs": 24,
  "num_columns": 30,
  "has_joins": 1,
  "priority": 2
}
```

Response:

```json
{
  "run_id": 1,
  "pipeline_type": "batch_daily",
  "yaml_config": "..."
}
```

---

### 🔹 Lineage Tracking

```http
GET /lineage
```

---

### 🔹 Rollback Pipeline

```http
POST /rollback/<run_id>
```

---

## 🤖 ML Model

* Algorithm: Random Forest Classifier

* Features:

  * source_type
  * volume_gb
  * update_frequency_hrs
  * num_columns
  * has_joins
  * priority

* Output:

  * batch_daily
  * batch_hourly
  * stream
  * micro_batch
  * weekly_snapshot

---

🧪 Testing

Run tests using:

```bash
pytest tests/ --cov=app
```

---
## 🔄 CI/CD Pipeline

GitHub Actions automatically:

✔ Installs dependencies
✔ Trains ML model
✔ Runs unit tests
✔ Checks code coverage
✔ Uploads coverage report

CI: PASSING ✔

## Running Screenshots

<img width="815" height="408" alt="Screenshot 2026-05-01 213452" src="https://github.com/user-attachments/assets/f3f61bfc-45d7-4cf1-b3f6-2e3c5abb42d0" />

<img width="1454" height="293" alt="Screenshot 2026-05-01 214145" src="https://github.com/user-attachments/assets/3d407f80-b6b3-4d83-818c-bed82404c3e1" />


## Example Workflow

1. User sends schema via API
2. ML model predicts pipeline type
3. YAML configuration is generated
4. Pipeline run is logged in database
5. Lineage tracking is updated
6. CI ensures code quality automatically

📌 Future Improvements

* Streamlit dashboard UI
* Cloud deployment (AWS / Render)
* Advanced model tuning

---
