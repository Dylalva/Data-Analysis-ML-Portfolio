import os
import pandas as pd
from sklearn.impute import SimpleImputer

def load_raw_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path)

def impute_numeric(df: pd.DataFrame, num_cols: list) -> pd.DataFrame:
    imputer = SimpleImputer(strategy='mean')
    df[num_cols] = imputer.fit_transform(df[num_cols])
    return df

def impute_categorical(df: pd.DataFrame, cat_cols: list) -> pd.DataFrame:
    imputer = SimpleImputer(strategy='most_frequent')
    df[cat_cols] = imputer.fit_transform(df[cat_cols])
    return df

def save_data(df: pd.DataFrame, output_path: str):
    df.to_csv(output_path, index=False)

if __name__ == "__main__":
    raw_path    = os.getenv('RAW_DATA_PATH', './data/raw/Students Social Media Addiction.csv')
    output_path = os.getenv('INTERIM_DATA_PATH', './data/interim/processing_dataset.csv')
    num_cols    = ['Student_ID', 'Age', 'Avg_Daily_Usage_Hours', 'Sleep_Hours_Per_Night', 'Mental_Health_Score',
                'Conflicts_Over_Social_Media', 'Addicted_Score']
    cat_cols    = ['Gender', 'Academic_Level', 'Country', 'Most_Used_Platform', 'Relationship_Status']


    df = load_raw_data(raw_path)
    df = impute_numeric(df, num_cols)
    df = impute_categorical(df, cat_cols)
    save_data(df, output_path)