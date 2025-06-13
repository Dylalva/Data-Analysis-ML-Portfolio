FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
#ENV RAW_DATA_PATH=data/raw/personality_dataset.csv
#ENV INTERIM_DATA_PATH=data/interim/processing_dataset.csv
#ENV PROCESSED_DATA_PATH=data/processed/processing_dataset.csv
#ENV MODEL_OUTPUT_PATH=models/rf_model.joblib
CMD ["bash", "scripts/run_train.sh", "scripts/run_test.sh"]