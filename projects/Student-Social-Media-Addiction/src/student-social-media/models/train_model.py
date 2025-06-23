import os
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import RandomForestClassifier

def train_and_save_model(input_path: str, model_path: str):
    df = pd.read_csv(input_path)
    X = df.drop(columns=['Affects_Academic_Performance'])
    y = df['Affects_Academic_Performance']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42)

    X_train, y_train = SMOTE(random_state=42).fit_resample(X_train, y_train)

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    joblib.dump(scaler, model_path.replace('.pkl','_scaler.pkl'))

    le = LabelEncoder()
    y_train_enc = le.fit_transform(y_train)
    joblib.dump(le, model_path.replace('.pkl','_label_encoder.pkl'))

    rf = RandomForestClassifier(random_state=42)
    params = {'n_estimators':[100,150,200],'max_depth':[None,10,20],'min_samples_split':[2,5,10]}
    gs = GridSearchCV(rf, params, cv=3, scoring='f1_weighted', n_jobs=-1)
    gs.fit(X_train_scaled, y_train_enc)

    joblib.dump(gs.best_estimator_, model_path)

if __name__=='__main__':
    input_path = os.getenv('PROCESSED_DATA_PATH','./data/processed/processing_dataset.csv')
    model_path = os.getenv('MODEL_OUTPUT_PATH','./models/rf_model.pkl')
    train_and_save_model(input_path, model_path)