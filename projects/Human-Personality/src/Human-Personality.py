import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import joblib
import warnings
from sklearn.model_selection import train_test_split, RandomizedSearchCV, cross_val_score, GridSearchCV, learning_curve
from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, f1_score, accuracy_score, f1_score, classification_report, confusion_matrix, roc_curve, auc

warnings.filterwarnings('ignore')

df = pd.read_csv('../data/raw/personality_dataset.csv')

df.head(5)

num_cols   = ['Time_spent_Alone', 'Social_event_attendance', 'Going_outside', 'Friends_circle_size', 'Post_frequency']
cat_cols   = ['Stage_fear', 'Drained_after_socializing']
target_col = 'Personality'

df.describe()

print(df.info())
print(df.isnull().sum())

df.hist(grid=True, bins=25, figsize=(15,8))

plt.figure(figsize=(8, 6))
sns.countplot(x=target_col, data=df)
plt.title('Distribución de los tipos de Personalidad')
plt.xlabel('Personalidad')
plt.ylabel('Cantidad')
plt.show()

sns.pairplot(df[num_cols + [target_col]], hue=target_col, diag_kind='hist')
plt.suptitle('Categorías númericas con respecto a la Personalidad', y=1.05)
plt.show()

plt.figure(figsize=(8, 6))
for i, col in enumerate(num_cols, 1):
    plt.subplot(3, 2, i)
    sns.boxplot(x=target_col, y=col, data=df)
    plt.title(f'{col} by Personality')
plt.tight_layout()
plt.suptitle('Distribución de categorías en base a la personalidad', y=1.05)
plt.show()

corr_matrix = df[num_cols].corr(method='spearman')
sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap='coolwarm')
plt.title('Mapa de calor de correlación entre atributos')
plt.show()

# Transformación de los datos

# Para columnas numéricas:
numeric_imputer = SimpleImputer(strategy='mean')  # o 'median'
df[num_cols] = numeric_imputer.fit_transform(df[num_cols])

# Para columnas categóricas:
categorical_imputer = SimpleImputer(strategy='most_frequent')
df[cat_cols] = categorical_imputer.fit_transform(df[cat_cols])

df.isnull().sum()


cat_encoder = OneHotEncoder(sparse=False)

encoded_cols = cat_encoder.fit_transform(df[cat_cols])

encoded_df = pd.DataFrame(encoded_cols, columns=cat_encoder.get_feature_names_out(cat_cols))

df = pd.concat([df, encoded_df], axis=1)

df = df.drop(columns=cat_cols)

# Tiempo de interacción social calculado
df['Interaction_Time'] = df['Social_event_attendance'] + df['Going_outside']

# Tensión social (1 si hay miedo al escenario o se siente agotado después de socializar, 0 si no)
df['Social_Stress'] = ((df['Stage_fear_Yes'] == 1) | (df['Drained_after_socializing_Yes'] == 1)).astype(int)

#  Amigos vs. eventos sociales
df['Friends_to_Events_Ratio'] = df['Friends_circle_size'] / (df['Social_event_attendance'] + 1e-5)

# Actividad en redes sociales
df['Social_Media_Engagement'] = df['Post_frequency'] * df['Social_event_attendance']

# Comportamiento social combinado
df['Social_Behavior'] = (df['Social_event_attendance'] + df['Going_outside'] + df['Friends_circle_size']) / 3

# Escala de energía social
df['Energy_Social'] = (df['Drained_after_socializing_No'] == 1).astype(int)

# Manejar outliers en las num_cols
for col in num_cols:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    df[col] = df[col].clip(lower=lower_bound, upper=upper_bound)

df.to_csv('../data/processed/processing_dataset.csv')

X = df.drop(columns=[target_col])
y = df[target_col]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

smote = SMOTE(random_state=42)
X_train, y_train = smote.fit_resample(X_train, y_train)

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

target_encoder = LabelEncoder()
y_train = target_encoder.fit_transform(y_train)
y_test = target_encoder.transform(y_test)


models = {
    'logistic': {
        'model': LogisticRegression(max_iter=1000),
        'use_scaled': True,
        'params': {'C': np.logspace(-4, 4, 20), 'solver': ['lbfgs', 'liblinear']}
    },
    'svm': {
        'model': SVC(probability=True),
        'use_scaled': True,
        'params': {'C': np.logspace(-3, 3, 20), 'kernel': ['rbf', 'linear'], 'gamma': ['scale', 'auto', 0.1, 1]}
    },
    'rf': {
        'model': RandomForestClassifier(random_state=42),
        'use_scaled': False,
        'params': {'n_estimators': [100, 150, 200], 'max_depth': [None, 10, 20], 'min_samples_split': [2, 5, 10]}
    },
    'knn': {
        'model': KNeighborsClassifier(),
        'use_scaled': True,
        'params': {'n_neighbors': [3, 5, 7, 9], 'weights': ['uniform', 'distance']}
    },
    'dt': {
        'model': DecisionTreeClassifier(random_state=42),
        'use_scaled': False,
        'params': {'max_depth': [None, 5, 10, 15], 'min_samples_split': [2, 5, 10]}
    }
}

# Trabajar los hiperparámetros
results = []
best_models = {}
for model_name, mp in models.items():
    clf = GridSearchCV(mp['model'], mp['params'], cv=3, scoring='f1_weighted', n_jobs=-1)
    X_train_current = X_train_scaled if mp['use_scaled'] else X_train
    clf.fit(X_train_current, y_train)
    results.append({
        'model': model_name,
        'best_score': clf.best_score_,
        'best_params': clf.best_params_
    })
    best_models[model_name] = clf.best_estimator_

df_results = pd.DataFrame(results)

df_results

model_names = [result['model'] for result in results]
model_scores = [result['best_score'] for result in results]

colors = plt.cm.viridis(np.linspace(0, 1, len(model_names)))

plt.figure(figsize=(10, 6))
plt.bar(model_names, model_scores, color=colors)
plt.ylim(min(model_scores) - 0.05, max(model_scores) + 0.001)
plt.ylabel('Best Score')
plt.title('Comparación de Modelos')

plt.show()


rf_model = best_models['rf']
rf_predictions = rf_model.predict(X_test)

accuracy = accuracy_score(y_test, rf_predictions)
f1 = f1_score(y_test, rf_predictions, average='weighted')

print(f"Accuracy: {accuracy}")
print(f"F1 Score: {f1}")

for model_name, model in best_models.items():
    model_predic = model.predict(X_test)
    accuracy = accuracy_score(y_test, model_predic)
    f1 = f1_score(y_test, model_predic, average='weighted')
    print('------------------------------')
    print(model_name + ':\n')
    print(f"Accuracy: {accuracy}")
    print(f"F1 Score: {f1}")

final_model = best_models['rf']

y_predic = final_model.predict(X_test)
print(classification_report(y_test, y_predic, target_names=target_encoder.classes_))

# Matriz de confusión
plt.figure(figsize=(8, 6))
sns.heatmap(confusion_matrix(y_test, y_predic), annot=True, fmt='d', cmap='Blues')
plt.title('Matriz de confusión del modelo seleccionado')
plt.xlabel('Predicted')
plt.ylabel('True')
plt.show()

importances = pd.Series(final_model.feature_importances_, index=X.columns)
importances = importances.sort_values(ascending=False)
sns.set(style="whitegrid", palette="muted")

plt.figure(figsize=(10,6))
sns.barplot(x=importances.values, y=importances.index)
plt.title("Importancia de variables en Random Forest")
plt.show()

# Predecir probabilidades para obtener la curva ROC
y_prob = final_model.predict_proba(X_test)[:, 1]  # Probabilidad de la clase positiva
fpr, tpr, thresholds = roc_curve(y_test, y_prob)
roc_auc = auc(fpr, tpr)

# Graficar
plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, color='blue', lw=2, label=f'ROC curve (AUC = {roc_auc:.2f})')
plt.plot([0, 1], [0, 1], color='gray', linestyle='--')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Curva ROC - Random Forest')
plt.legend(loc='lower right')
plt.show()

train_sizes, train_scores, test_scores = learning_curve(
    rf_model, X_train_scaled, y_train, cv=3, scoring='f1_weighted', n_jobs=-1
)

train_mean = np.mean(train_scores, axis=1)
test_mean = np.mean(test_scores, axis=1)

plt.figure(figsize=(8, 6))
plt.plot(train_sizes, train_mean, label='Entrenamiento', color='blue')
plt.plot(train_sizes, test_mean, label='Validación', color='green')
plt.xlabel('Tamaño de Entrenamiento')
plt.ylabel('F1 Score')
plt.title('Curva de Aprendizaje - Random Forest')
plt.legend()
plt.show()

cv_scores = cross_val_score(final_model, X_train_scaled, y_train, cv=5, scoring='f1_weighted')

plt.figure(figsize=(8, 6))
plt.plot(range(1, len(cv_scores) + 1), cv_scores, marker='o', linestyle='-', color='purple')
plt.title('Puntajes de Validación Cruzada - Random Forest')
plt.xlabel('Fold')
plt.ylabel('F1 Score')
plt.show()

plt.figure(figsize=(8, 6))
plt.hist([y_test, y_predic], bins=20, label=['Verdadero', 'Predicción'], alpha=0.7)
plt.legend(loc='best')
plt.title('Distribución de Verdaderos vs Predicciones')
plt.show()