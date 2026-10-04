import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine

# Database Connection
engine = create_engine('postgresql://postgres@localhost:5432/ecommerce_db')
df = pd.read_sql("SELECT * FROM customer_churn_predictions", engine)

# Printed columns to verify
print("Columns in Database:", df.columns.tolist())

# Auto-detect churn column name
churn_col = [col for col in df.columns if 'churn' in col.lower() or 'pred' in col.lower()]
target_col = churn_col[0] if churn_col else df.columns[-1]

# Setup Figure
plt.figure(figsize=(12, 5))

# Chart 1: Churn Count Distribution
plt.subplot(1, 2, 1)
sns.countplot(data=df, x=target_col, palette=['#2ecc71', '#e74c3c'])
plt.title(f'Customer Churn Distribution ({target_col})')
plt.xlabel('Prediction')
plt.ylabel('Number of Customers')

# Chart 2: RFM or Feature Scatter Plot
plt.subplot(1, 2, 2)
num_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
if len(num_cols) >= 2:
    sns.scatterplot(data=df, x=num_cols[0], y=num_cols[1], hue=target_col, palette=['#2ecc71', '#e74c3c'], alpha=0.7)
    plt.title(f'{num_cols[0]} vs {num_cols[1]} by Churn')

plt.tight_layout()
plt.savefig('churn_visualizations.png')
print("✅ Visualization saved as 'churn_visualizations.png'!")
plt.show()