import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer

import joblib

df = pd.read_csv('../data/steam_store_data_2024.csv')
df.head()

# Limpiar las columnas de precios y porcentaje de descuento
df['price'] = df['price'].replace({'\$': '', ',': ''}, regex=True).astype(float)
df['salePercentage'] = df['salePercentage'].replace({'%': '', ',': ''}, regex=True).astype(float)

df['price'].fillna(df['price'].mean(), inplace=True)
df['salePercentage'].fillna(0, inplace=True)
# Imputar valores faltantes con SimpleImputer
imputer = SimpleImputer(strategy="most_frequent")
df['description'] = imputer.fit_transform(df[['description']]).flatten()

# Convertir las columnas de reseñas a categorías ordenadas
review_order = ['Mostly Negative', 'Mixed', 'Mostly Positive', 'Very Positive', 'Overwhelmingly Positive']
df['recentReviews'] = pd.Categorical(df['recentReviews'], categories=review_order, ordered=True)
df['allReviews'] = pd.Categorical(df['allReviews'], categories=review_order, ordered=True)

# Imputación de missing values en las reseñas
df['recentReviews'] = imputer.fit_transform(df[['recentReviews']]).flatten()
df['allReviews'] = imputer.fit_transform(df[['allReviews']]).flatten()

# Extraer palabras clave de las descripciones de los juegos
vectorizer = CountVectorizer(stop_words='english', max_df=0.40)
X = vectorizer.fit_transform(df['description'])

# Convertir la matriz en un DataFrame
df_words = pd.DataFrame(X.toarray(), columns=vectorizer.get_feature_names_out())

# Mostrar las primeras 10 palabras más frecuentes
top_words = df_words.sum(axis=0).sort_values(ascending=False).head(10)
print(top_words)

wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(top_words)

plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.savefig('../figure/WordFreq.png')
plt.show()

gaming_categories = {
    'action': ['action', 'shooter', 'fight', 'horror'],
    'adventure': ['adventure', 'exploration'],
    'puzzle': ['puzzle'],
    'rpg': ['role', 'rpg'],
    'simulation': ['simulation'],
    'strategy': ['strategy', 'tactical'],
    'sports': ['sports']
}

# Crear una nueva columna para las categorías
df['category'] = np.nan

# Asignar categorías basadas en las palabras clave
for category, keywords in gaming_categories.items():
    for keyword in keywords:
        if keyword in df_words.columns:  # Comprobar si la palabra clave está en las columnas de df_words
            mask = df_words[keyword] > 0  # Verifica si la palabra clave está presente en cada fila
            df.loc[mask, 'category'] = category
        else:
            print(f"'{keyword}' no está en las columnas de df_words.")

df['category'].fillna('Unknow', inplace=True)

plt.figure(figsize=(10, 6))
sns.countplot(data=df, x='allReviews', palette='viridis')
plt.title('Distribución de las reseñas')
plt.savefig('../figure/DistResenas.png')
plt.show()

# Distribución de los precios
sns.boxplot(data=df, x='price', color='lightblue')
plt.title('Distribución de los precios')
plt.savefig('../figure/DistPrec.png')
plt.show()

# Distribución de los descuentos
sns.boxplot(data=df, x='salePercentage', color='lightgreen')
plt.title('Distribución de los descuentos')
plt.savefig('../figure/DistDesc.png')
plt.show()

# Distribución de las categorías
sns.countplot(data=df, x='category', palette='Set2')
plt.title('Distribución de las categorías de juegos')
plt.xticks(rotation=45)
plt.savefig('../figure/DistCatJuego.png')
plt.show()

plt.figure(figsize=(12, 6))
sns.boxplot(x='category', y='price', data=df, palette='Set2')
plt.title('Distribución de Precios por Categoría')
plt.xlabel('Categoría')
plt.ylabel('Precio')
plt.xticks(rotation=45) 
plt.savefig('../figure/DistPrecPerCat.png')
plt.show()

plt.figure(figsize=(12, 6))
sns.countplot(x='category', hue='recentReviews', data=df, palette='Set2')
plt.title('Distribución de Reseñas Recientes por Categoría')
plt.xlabel('Categoría')
plt.ylabel('Número de Reseñas Recientes')
plt.xticks(rotation=45)
plt.legend(title='Reseñas Recientes')
plt.savefig('../figure/DistResenasRecientesPerCat.png')
plt.show()

