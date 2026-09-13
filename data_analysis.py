import pandas as pd

df = pd.read_csv("hearing_care_data.csv")

print(df.head())

print("\nDataset Shape:")
print(df.shape)

print("\nColumns:")
print(df.columns)

print("\nData Types:")
print(df.dtypes)

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Rows:")
print(df.duplicated().sum())

# Fill missing values

df["Gender"] = df["Gender"].fillna("Unknown")

df["City"] = df["City"].fillna("Unknown")

df["Assessment_Score"] = df["Assessment_Score"].fillna(
    df["Assessment_Score"].median()
)

df["Device_Type"] = df["Device_Type"].fillna("None")

print("\nMissing Values After Cleaning:")
print(df.isnull().sum())

# Basic Data Analysis

print("\nTotal Customers:")
print(len(df))

print("\nAverage Age:")
print(df["Age"].mean())

print("\nAverage Assessment Score:")
print(df["Assessment_Score"].mean())

print("\nTotal Revenue:")
print(df["Order_Value"].sum())

print("\nAverage Order Value:")
print(df["Order_Value"].mean())

print("\nDevice Type Count:")
print(df["Device_Type"].value_counts())

print("\nCity-wise Revenue:")
print(df.groupby("City")["Order_Value"].sum().sort_values(ascending=False))

print("\nPurchase Channel Count:")
print(df["Purchase_Channel"].value_counts())

#sqlcodes

import sqlite3

# Connect to SQLite database
conn = sqlite3.connect("hearing_care.db")

# Save Pandas DataFrame into SQL table
df.to_sql("customers", conn, if_exists="replace", index=False)

print("\nSQL table created successfully!")

# Run a SQL query
# SQL Analysis

queries = {
    "Total Customers": """
        SELECT COUNT(*) AS total_customers
        FROM customers;
    """,

    "Average Age": """
        SELECT ROUND(AVG(Age), 2) AS average_age
        FROM customers;
    """,

    "Total Revenue": """
        SELECT ROUND(SUM(Order_Value), 2) AS total_revenue
        FROM customers;
    """,

    "Average Order Value": """
        SELECT ROUND(AVG(Order_Value), 2) AS average_order_value
        FROM customers;
    """
}

for name, query in queries.items():
    print(f"\n{name}:")
    print(pd.read_sql_query(query, conn))


# City-wise Revenue

query = """
SELECT 
    City,
    ROUND(SUM(Order_Value), 2) AS total_revenue
FROM customers
GROUP BY City
ORDER BY total_revenue DESC;
"""

print("\nCity-wise Revenue:")
print(pd.read_sql_query(query, conn))


# Device-wise Revenue

query = """
SELECT
    Device_Type,
    COUNT(*) AS customers,
    ROUND(SUM(Order_Value), 2) AS total_revenue
FROM customers
GROUP BY Device_Type
ORDER BY total_revenue DESC;
"""

print("\nDevice-wise Revenue:")
print(pd.read_sql_query(query, conn))

# Purchase Channel Analysis

query = """
SELECT
    Purchase_Channel,
    COUNT(*) AS customers,
    ROUND(SUM(Order_Value), 2) AS total_revenue,
    ROUND(AVG(Order_Value), 2) AS average_order_value
FROM customers
GROUP BY Purchase_Channel
ORDER BY total_revenue DESC;
"""

print("\nPurchase Channel Analysis:")
print(pd.read_sql_query(query, conn))


# Follow-up Analysis

query = """
SELECT
    Follow_Up_Required,
    COUNT(*) AS customers
FROM customers
GROUP BY Follow_Up_Required
ORDER BY customers DESC;
"""

print("\nFollow-up Analysis:")
print(pd.read_sql_query(query, conn))


conn.close()
