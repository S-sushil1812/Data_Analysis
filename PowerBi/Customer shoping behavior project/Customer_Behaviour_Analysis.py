import pandas as pd
from sqlalchemy import create_engine


# Load the dataset
df= pd.read_csv('customer_shopping_behavior.csv')

#print(df.head())
#print(df.info())
#print(df.describe(include='all'))
#print(df.isnull().sum())

# Impute missing values in 'Review Rating' column with the median value of each category
df['Review Rating']=df.groupby('Category')['Review Rating'].transform(lambda x: x.fillna(x.median()))
#print(df.isnull().sum())

# Standardize column names by converting to lowercase and replacing spaces with underscores
df.columns= df.columns.str.lower()
df.columns = df.columns.str.replace(' ','_')

# Rename 'purchase_amount_(usd)' to 'purchase_amount' for clarity
df= df.rename(columns={'purchase_amount_(usd)': 'purchase_amount'})
#print(df.columns)

# Create age groups column using pd.qcut
lables = ['Young Adults', 'Adults', 'Middle-Aged', 'Seniors']
df['age_group'] = pd.qcut(df['age'], q=4, labels=lables)
#print(df[['age','age_group']].head(20))

# Create column 'purchase_frequency_days'  
frequency_mapping = {
    'Fortnightly': 14,
    'Weekly': 7,
    'Monthly': 30,
    'Quarterly': 90,
    'Bi-Weekly': 14,
    'Every 3 Months': 90,
    'Annually': 365
}
df['purchase_frequency_days'] = df['frequency_of_purchases'].map(frequency_mapping)
#print(df[['purchase_frequency_days','frequency_of_purchases']].head(10))

# Analyze the relationship between 'discount_applied' and 'promo_code_used'acctully we need this column value column
#print((df['discount_applied']==df['promo_code_used']).all())

# Since 'discount_applied' and 'promo_code_used' columns have the same values, we can drop one of them to avoid redundancy
df = df.drop(columns='promo_code_used', axis=1)
#print(df.columns)


# Step 1: Connect to PostgreSQL
# Replace placeholders with your actual details
username = "postgres"      # default user
password = "12345"     # the password you set during installation
host = "localhost"        # if running locally
port = "5432"            # default PostgreSQL port
database = "customer_behavior"   # the database you created in pgAdmin

engine = create_engine(
    f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}"
)

# Step 2: Load DataFrame into PostgreSQL
table_name = "customer"   # choose any table name
df.to_sql(table_name, engine, if_exists="replace", index=False)



