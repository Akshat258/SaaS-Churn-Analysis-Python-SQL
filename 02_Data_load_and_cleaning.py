import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus
import os

DB_USER = 'postgres'
DB_PASSWORD = 'your_password_here'
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'ravenstack_db'

encoded_password = quote_plus(DB_PASSWORD)
connection_string = f'postgresql://{DB_USER}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
engine = create_engine(connection_string)

print("\n Loading data from database...")

accounts = pd.read_sql("SELECT * FROM accounts", engine)
subscriptions = pd.read_sql("SELECT * FROM subscriptions", engine)
churn_events = pd.read_sql("SELECT * FROM churn_events", engine)
feature_usage = pd.read_sql("SELECT * FROM feature_usage", engine)
support_tickets = pd.read_sql("SELECT * FROM support_tickets", engine)

print(" Data loaded successfully!")
print(f"   Accounts: {len(accounts):,} rows")
print(f"   Subscriptions: {len(subscriptions):,} rows")
print(f"   Churn Events: {len(churn_events):,} rows")
print(f"   Feature Usage: {len(feature_usage):,} rows")
print(f"   Support Tickets: {len(support_tickets):,} rows")

# DATA CLEANING
print("\n" + "="*60)
print("CLEANING DATA")
print("="*60)

# Fix date columns
print("\n  Converting date columns...")

accounts['signup_date'] = pd.to_datetime(accounts['signup_date'], format='%d-%m-%Y', errors='coerce')
subscriptions['start_date'] = pd.to_datetime(subscriptions['start_date'], format='%Y-%m-%d', errors='coerce')
subscriptions['end_date'] = pd.to_datetime(subscriptions['end_date'], format='%Y-%m-%d', errors='coerce')
churn_events['churn_date'] = pd.to_datetime(churn_events['churn_date'], format='%Y-%m-%d', errors='coerce')
support_tickets['submitted_at'] = pd.to_datetime(support_tickets['submitted_at'], format='%Y-%m-%d', errors='coerce')
support_tickets['closed_at'] = pd.to_datetime(support_tickets['closed_at'], format='%Y-%m-%d', errors='coerce')
feature_usage['usage_date'] = pd.to_datetime(feature_usage['usage_date'], format='%Y-%m-%d', errors='coerce')

print("    All dates converted to datetime format")

# Check missing values
print("\n  Checking missing values...")

print("\n   Accounts missing values:")
missing_accounts = accounts.isnull().sum()
if missing_accounts.sum() > 0:
    print(missing_accounts[missing_accounts > 0])
else:
    print("   No missing values ")

print("\n   Churn Events missing values:")
missing_churn = churn_events.isnull().sum()
if missing_churn.sum() > 0:
    print(missing_churn[missing_churn > 0])
else:
    print("   No missing values ")

print("\n   Support Tickets missing values:")
missing_support = support_tickets.isnull().sum()
if missing_support.sum() > 0:
    print(missing_support[missing_support > 0])
else:
    print("   No missing values ")

# 3. Handle missing values
print("\n Handling missing values...")

# Fill missing feedback with placeholder
if 'feedback_text' in churn_events.columns:
    original_missing = churn_events['feedback_text'].isnull().sum()
    churn_events['feedback_text'].fillna('No feedback provided', inplace=True)
    print(f"    Filled {original_missing} missing feedback_text entries")

# Fill missing satisfaction scores with median
if 'satisfaction_score' in support_tickets.columns:
    original_missing = support_tickets['satisfaction_score'].isnull().sum()
    median_satisfaction = support_tickets['satisfaction_score'].median()
    support_tickets['satisfaction_score'].fillna(median_satisfaction, inplace=True)
    print(f"    Filled {original_missing} missing satisfaction_score with median: {median_satisfaction:.2f}")

# 4. Create useful calculated fields
print("\n  Creating calculated fields...")

# Add month/year columns for trend analysis
accounts['signup_month'] = accounts['signup_date'].dt.month
accounts['signup_year'] = accounts['signup_date'].dt.year
accounts['signup_month_name'] = accounts['signup_date'].dt.strftime('%B')
print("    Added signup_month, signup_year, signup_month_name to accounts")

# Calculate subscription duration
subscriptions['duration_days'] = (subscriptions['end_date'] - subscriptions['start_date']).dt.days
print("    Added duration_days to subscriptions")

# Add month to churn events
churn_events['churn_month'] = churn_events['churn_date'].dt.month
churn_events['churn_year'] = churn_events['churn_date'].dt.year
print("    Added churn_month, churn_year to churn_events")

# 5. Data quality summary
print("\n" + "="*60)
print("DATA QUALITY SUMMARY")
print("="*60)

print(f"\n Accounts:")
print(f"   Date range: {accounts['signup_date'].min()} to {accounts['signup_date'].max()}")
print(f"   Churned customers: {accounts['churn_flag'].sum()}")
print(f"   Active customers: {(~accounts['churn_flag']).sum()}")

print(f"\n Subscriptions:")
print(f"   Total MRR: ₹{subscriptions['mrr_amount'].sum():,.2f}")
print(f"   Average MRR: ₹{subscriptions['mrr_amount'].mean():,.2f}")
print(f"   Active subscriptions: {(~subscriptions['churn_flag']).sum()}")

print(f"\n Churn Events:")
print(f"   Total churn events: {len(churn_events)}")
print(f"   Date range: {churn_events['churn_date'].min()} to {churn_events['churn_date'].max()}")

# 6. Export cleaned data
print("\n" + "="*60)
print("EXPORTING CLEANED DATA")
print("="*60)

# Create exports folder if it doesn't exist
if not os.path.exists('exports'):
    os.makedirs('exports')
    print(" Created 'exports' folder")

# Save cleaned data as CSV
accounts.to_csv('exports/accounts_cleaned.csv', index=False)
subscriptions.to_csv('exports/subscriptions_cleaned.csv', index=False)
churn_events.to_csv('exports/churn_events_cleaned.csv', index=False)
support_tickets.to_csv('exports/support_tickets_cleaned.csv', index=False)
feature_usage.to_csv('exports/feature_usage_cleaned.csv', index=False)

print("\n Cleaned data exported to 'exports' folder:")
print("   - accounts_cleaned.csv")
print("   - subscriptions_cleaned.csv")
print("   - churn_events_cleaned.csv")
print("   - support_tickets_cleaned.csv")
print("   - feature_usage_cleaned.csv")

print("\n" + "="*60)
print(" DATA CLEANING COMPLETE!")
print("="*60)
print("\n Ready for analysis! All data is now clean and structured.")
