import pandas as pd
import numpy as np
from datetime import datetime
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier

print("🚀 Pipeline Execution Started...")

# 1. Load Dataset
csv_path = "online_retail.csv"
print(f"📥 Loading dataset from {csv_path}...")
df = pd.read_csv(csv_path, encoding="ISO-8859-1")

# 2. Data Cleaning
print("🧹 Cleaning raw data...")
df = df.dropna(subset=['CustomerID'])
df['CustomerID'] = df['CustomerID'].astype(int)
df = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)]
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
df['TotalSum'] = df['Quantity'] * df['UnitPrice']

# 3. Calculate RFM Metrics
print("📊 Calculating RFM metrics...")
snapshot_date = df['InvoiceDate'].max() + pd.Timedelta(days=1)
rfm = df.groupby('CustomerID').agg({
    'InvoiceDate': lambda x: (snapshot_date - x.max()).days,
    'InvoiceNo': 'nunique',
    'TotalSum': 'sum'
}).reset_index()

rfm.columns = ['CustomerID', 'Recency', 'Frequency', 'Monetary']

# 4. Define Churn Label
rfm['Is_Churned'] = (rfm['Recency'] > 90).astype(int)

# 5. Train XGBoost Model
print("🤖 Training XGBoost Churn Model...")
X = rfm[['Recency', 'Frequency', 'Monetary']]
y = rfm['Is_Churned']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42)
model.fit(X_train, y_train)

# Predict churn probability
rfm['Churn_Probability'] = model.predict_proba(X)[:, 1]

# Segment Risk
def assign_risk(prob):
    if prob >= 0.7:
        return 'High Risk'
    elif prob >= 0.4:
        return 'Medium Risk'
    else:
        return 'Low Risk'

rfm['Risk_Segment'] = rfm['Churn_Probability'].apply(assign_risk)

# 6. Push Output to PostgreSQL Database
DB_USER = 'postgres'
DB_PASS = 'YOUR_POSTGRES_PASSWORD'  # <-- Yahan apna pgAdmin password likho
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'ecommerce_db'

print("💾 Connecting to PostgreSQL database...")
engine = create_engine(f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

table_name = 'customer_churn_predictions'
rfm.to_sql(table_name, engine, if_exists='replace', index=False)

print(f"✅ SUCCESS: Data successfully written to PostgreSQL table '{table_name}'!")