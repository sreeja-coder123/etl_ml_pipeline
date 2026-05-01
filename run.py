from app import create_app
from app.ml_model import train_and_save_model
import os

if not os.path.exists("models/rf_model.pkl"):
    print("Training ML model...")
    train_and_save_model()

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5000)