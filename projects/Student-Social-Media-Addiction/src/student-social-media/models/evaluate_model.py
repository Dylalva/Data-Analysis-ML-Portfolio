import os
import joblib
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

def evaluate_model(model_path: str, processed_data: str):
    model = joblib.load(model_path)
    scaler = joblib.load(model_path.replace('.pkl','_scaler.pkl'))
    le = joblib.load(model_path.replace('.pkl','_label_encoder.pkl'))

    df = pd.read_csv(processed_data)
    X = df.drop(columns=['Affects_Academic_Performance'])
    y = le.transform(df['Affects_Academic_Performance'])

    X_scaled = scaler.transform(X)
    y_pred = model.predict(X_scaled)

    print(classification_report(y, y_pred, target_names=le.classes_))

    cm = confusion_matrix(y, y_pred)
    sns.heatmap(cm, annot=True, fmt='d')
    plt.show()

if __name__=='__main__':
    evaluate_model(
        os.getenv('MODEL_PATH','./models/rf_model.pkl'),
        os.getenv('PROCESSED_DATA_PATH','./data/processed/processing_dataset.csv')
    )