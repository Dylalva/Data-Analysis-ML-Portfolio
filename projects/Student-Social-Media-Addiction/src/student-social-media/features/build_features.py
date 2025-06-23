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

    # Interacción entre Género y Nivel Académico
    df['Gender_Academic_Interaction'] = df['Gender'].astype(str) + "_" + df['Academic_Level'].astype(str)
    
    # Interacción entre Plataforma y Estado de Relación
    df['Platform_Relationship_Interaction'] = df['Most_Used_Platform'] + "_" + df['Relationship_Status']
    
    # Clasificación de uso de redes sociales (Bajo, Medio, Alto)
    def usage_category(hours):
        if hours <= 2:
            return 0  # Bajo
        elif hours <= 5:
            return 1  # Medio
        else:
            return 2  # Alto
    
    df['Usage_Category'] = df['Avg_Daily_Usage_Hours'].apply(usage_category)
    
    # Variables derivadas de salud mental y sueño
    df['Mental_Health_Risk'] = df['Mental_Health_Score'] - df['Sleep_Hours_Per_Night']
    df['Sleep_Usage_Discrepancy'] = df['Sleep_Hours_Per_Night'] - df['Avg_Daily_Usage_Hours']
    
    # Estrés acumulado en relaciones por redes sociales
    df['Relationship_Stress'] = df['Conflicts_Over_Social_Media'] * df['Addicted_Score']
    
    # Interacción entre adicción a redes sociales y rendimiento académico
    df['Addiction_Affects_Academic'] = df['Addicted_Score'] * df['Affects_Academic_Performance'].map({'Yes': 1, 'No': 0}).astype(int)
    
    # Variables de comportamiento en redes sociales
    # Definir plataformas populares
    popular_platforms = ['Instagram', 'Facebook', 'TikTok']
    
    # Frecuencia de uso de plataformas populares
    df['Frequent_Use_Popular_Platforms'] = df['Most_Used_Platform'].apply(lambda x: 1 if x in popular_platforms else 0)
    
    # Impacto del uso de redes sociales en función de la plataforma
    df['Social_Media_Usage_Impact'] = df['Avg_Daily_Usage_Hours'] * df['Most_Used_Platform'].apply(lambda x: 2 if x in ['Instagram', 'TikTok'] else 1)
    
    # Promedios por país
    df['Avg_Country_Usage'] = df.groupby('Country')['Avg_Daily_Usage_Hours'].transform('mean')
    df['Avg_Country_Mental_Health'] = df.groupby('Country')['Mental_Health_Score'].transform('mean')

    return df

def save_features(df: pd.DataFrame, output_path: str):
    df.to_csv(output_path, index=False)

if __name__=='__main__':
    input_path = os.getenv('INTERIM_DATA_PATH','./data/interim/processing_dataset.csv')
    output_path = os.getenv('PROCESSED_DATA_PATH','./data/processed/processing1_dataset.csv')
    df = load_interim_data(input_path)
    df = encode_and_engineer(df)
    save_features(df, output_path)