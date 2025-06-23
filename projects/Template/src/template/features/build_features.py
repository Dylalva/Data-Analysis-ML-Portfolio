import os
import pandas as pd
from sklearn.preprocessing import OneHotEncoder

def load_interim_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path)

def encode_and_engineer(df: pd.DataFrame) -> pd.DataFrame:
    encoder = OneHotEncoder(sparse=False)
    encoded = encoder.fit_transform(df[['Stage_fear', 'Drained_after_socializing']])
    cols = encoder.get_feature_names_out(['Stage_fear', 'Drained_after_socializing'])
    df_encoded = pd.DataFrame(encoded, columns=cols, index=df.index)
    df = pd.concat([df.drop(columns=['Stage_fear','Drained_after_socializing']), df_encoded], axis=1)

    # Feature engineering
    df['Interaction_Time'] = df['Social_event_attendance'] + df['Going_outside']
    df['Social_Stress'] = ((df['Stage_fear_Yes']==1) | (df['Drained_after_socializing_Yes']==1)).astype(int)
    df['Friends_to_Events_Ratio'] = df['Friends_circle_size'] / (df['Social_event_attendance'] + 1e-5)
    df['Social_Media_Engagement'] = df['Post_frequency'] * df['Social_event_attendance']
    df['Social_Behavior'] = (df['Social_event_attendance'] + df['Going_outside'] + df['Friends_circle_size'])/3
    df['Energy_Social'] = (df['Drained_after_socializing_No']==1).astype(int)

    # Clip outliers
    for col in ['Time_spent_Alone','Social_event_attendance','Going_outside','Friends_circle_size','Post_frequency']:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        df[col] = df[col].clip(Q1 - 1.5*IQR, Q3 + 1.5*IQR)

    return df

def save_features(df: pd.DataFrame, output_path: str):
    df.to_csv(output_path, index=False)

if __name__=='__main__':
    input_path = os.getenv('INTERIM_DATA_PATH','./data/interim/processing_dataset.csv')
    output_path = os.getenv('PROCESSED_DATA_PATH','./data/processed/processing1_dataset.csv')
    df = load_interim_data(input_path)
    df = encode_and_engineer(df)
    save_features(df, output_path)