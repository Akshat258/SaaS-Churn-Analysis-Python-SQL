import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus


DB_USER = 'postgres'
DB_PASSWORD = 'your_password_here'
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'ravenstack_db'

encoded_password = quote_plus(DB_PASSWORD)

connection_string = f'postgresql://{DB_USER}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

print(f"\nAttempting to connect as user: {DB_USER}")
print(f"Database: {DB_NAME}")
print(f"Host: {DB_HOST}:{DB_PORT}\n")

try:
    engine = create_engine(connection_string)

    # Test query
    test_query = "SELECT COUNT(*) as total FROM accounts"
    result = pd.read_sql(test_query, engine)

    print(" Connection successful!\n")

    # Get counts from all tables
    print("=" * 60)
    print("DATABASE OVERVIEW")
    print("=" * 60)

    tables = ['accounts', 'subscriptions', 'churn_events', 'feature_usage', 'support_tickets']

    for table in tables:
        count = pd.read_sql(f"SELECT COUNT(*) as count FROM {table}", engine).iloc[0, 0]
        print(f"{table:20s}: {count:,} rows")

    print("\n" + "=" * 60)
    print("Sample data from accounts table:")
    print("=" * 60)
    sample = pd.read_sql("SELECT * FROM accounts LIMIT 3", engine)
    print(sample.to_string())

    print("\n Database connection test complete!")

except Exception as e:
    print(f" Connection failed: {e}")
    print("\n Troubleshooting:")
    print(f"1. Check username is correct (currently: '{DB_USER}')")
    print(f"2. Check password is correct")
    print(f"3. Verify PostgreSQL is running (open pgAdmin)")
    print(f"4. Verify database '{DB_NAME}' exists in pgAdmin")
