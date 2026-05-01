import pickle, os
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

MODEL_PATH = "models/rf_model.pkl"
ENCODERS_PATH = "models/encoders.pkl"

SOURCE_TYPES = ["mysql", "postgres", "s3", "api", "csv"]
PIPELINE_TYPES = ["batch_daily", "batch_hourly", "stream", "micro_batch", "weekly_snapshot"]

def generate_training_data():
    import numpy as np
    np.random.seed(42)
    n = 500
    data = {
        "source_type": np.random.choice(SOURCE_TYPES, n),
        "volume_gb": np.random.exponential(5, n).round(2),
        "update_frequency_hrs": np.random.choice([1,6,12,24,168], n),
        "num_columns": np.random.randint(5, 200, n),
        "has_joins": np.random.choice([0,1], n),
        "priority": np.random.choice([1,2,3], n),
    }
    df = pd.DataFrame(data)
    def label(row):
        if row.update_frequency_hrs <= 1: return "stream"
        if row.update_frequency_hrs <= 6: return "micro_batch"
        if row.update_frequency_hrs <= 12: return "batch_hourly"
        if row.update_frequency_hrs == 168: return "weekly_snapshot"
        return "batch_daily"
    df["pipeline_type"] = df.apply(label, axis=1)
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/training_data.csv", index=False)
    return df

def train_and_save_model():
    df = generate_training_data()
    le_src = LabelEncoder()
    le_tgt = LabelEncoder()
    df["source_enc"] = le_src.fit_transform(df["source_type"])
    df["label"] = le_tgt.fit_transform(df["pipeline_type"])
    features = ["source_enc","volume_gb","update_frequency_hrs",
                "num_columns","has_joins","priority"]
    X, y = df[features], df["label"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    acc = clf.score(X_test, y_test)
    print(f"Model accuracy: {acc:.2%}")
    os.makedirs("models", exist_ok=True)
    with open(MODEL_PATH,"wb") as f: pickle.dump(clf, f)
    with open(ENCODERS_PATH,"wb") as f: pickle.dump((le_src, le_tgt), f)
    return acc

def predict_pipeline(schema: dict) -> str:
    with open(MODEL_PATH,"rb") as f: clf = pickle.load(f)
    with open(ENCODERS_PATH,"rb") as f: le_src, le_tgt = pickle.load(f)
    src = schema.get("source_type","mysql")
    if src not in le_src.classes_: src = "mysql"
    features = [[
        le_src.transform([src])[0],
        float(schema.get("volume_gb", 1.0)),
        float(schema.get("update_frequency_hrs", 24)),
        int(schema.get("num_columns", 20)),
        int(schema.get("has_joins", 0)),
        int(schema.get("priority", 2)),
    ]]
    pred = clf.predict(features)[0]
    return le_tgt.inverse_transform([pred])[0]