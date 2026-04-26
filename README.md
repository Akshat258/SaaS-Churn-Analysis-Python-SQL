Project Overview

This project analyses churn patterns in a B2B SaaS environment using a dataset of 30,000+ records. The analysis focuses on the "Satisfaction Paradox"—a phenomenon where high support satisfaction scores (4.0/5.0) mask underlying loyalty risks caused by product feature gaps.

Financial Impact Identified: ₹23.5 Lakhs MRR leak (₹2.82 Crore/year).

🛠️ The Technical Stack

Environment: PyCharm (Professional IDE workflow with .py scripts)

Database: PostgreSQL (Schema Design, Complex Joins, Data Aggregation)

Language: Python (Pandas, NumPy for data manipulation)

Library: SQLAlchemy (Database ORM & Pipeline Connection)

📂 Repository Structure

00_Database_Schema.sql: SQL foundation and data import.

01_Database_Connect.py: Establishing the PostgreSQL-Python bridge.

02_Data_load_and_cleaning.py: Median imputation and data standardisation.

03_churn_analysis.py: Core diagnostic logic and revenue impact calculation.

🔍 Key Findings

1. The Satisfaction Paradox
Churned customers maintained an average satisfaction score of 4.0/5.0. The primary driver for leaving was a "Feature Gap" (19% of churn), indicating that product utility is a higher predictor of retention than support quality.

2. Industry Risk
The DevTools industry was identified as the highest-risk segment, with a churn rate of 31.0%.

3. Lead Quality
Partner Referrals proved to be 2x more stable than leads generated from Events.

🧠 Career Learning

This project demonstrates that Technical Skill is the engine, but Business Acumen is the steering wheel. The real value for a data analyst lies in identifying actionable insights like the "Satisfaction Paradox" rather than just calculating surface-level metrics.
