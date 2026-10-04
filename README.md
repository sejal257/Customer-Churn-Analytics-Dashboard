# 📊 Customer Churn Analytics & Predictive Web Dashboard

An end-to-end Machine Learning pipeline and interactive web platform built to predict customer churn, perform RFM segmentation, and assist business stakeholders in data-backed decision-making.

## 🚀 Tech Stack
- **Language:** Python
- **Database:** PostgreSQL 16
- **Machine Learning:** XGBoost, Scikit-Learn, Pandas, NumPy
- **Dashboard & UI:** Streamlit
- **Visualizations:** Matplotlib, Seaborn

## 📌 Features
- **Data Pipeline:** Automated ETL process reading transactional records and storing engineered features in PostgreSQL.
- **RFM Analysis:** Calculates Recency, Frequency, and Monetary metrics for customer segmentation.
- **Predictive Model:** XGBoost Classifier trained to detect high-risk churn customers.
- **Interactive Web App:** Real-time metrics visualization and churn risk scoring powered by Streamlit.

## 📂 Dataset
This project utilizes the **Online Retail II / UCI Machine Learning Repository** dataset. Due to GitHub file size limits (>25MB), the raw CSV dataset is excluded from this repository and processed directly via local PostgreSQL pipelines.

## 🛠️ How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/sejal257/Customer-Churn-Analytics-Dashboard.git](https://github.com/sejal257/Customer-Churn-Analytics-Dashboard.git)
   cd Customer-Churn-Analytics-Dashboard
