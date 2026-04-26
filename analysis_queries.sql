CREATE TABLE accounts (
    account_id VARCHAR(20),
    account_name VARCHAR(100),
    industry VARCHAR(50),
    country VARCHAR(10),
    signup_date VARCHAR(20),  
    referral_source VARCHAR(50),
    plan_tier VARCHAR(20),
    seats INT,
    is_trial BOOLEAN,
    churn_flag BOOLEAN);

COPY accounts
FROM 'E:/Ravenstack_Project/data/ravenstack_accounts.csv'
WITH (FORMAT CSV, HEADER TRUE, DELIMITER ',');

CREATE TABLE subscriptions (
	subscription_id VARCHAR(20),
    account_id VARCHAR(20),
    start_date VARCHAR(20),
    end_date VARCHAR(20),
    plan_tier VARCHAR(20),
    seats INT,
    mrr_amount DECIMAL(10,2),
    arr_amount DECIMAL(10,2),
    is_trial BOOLEAN,
    upgrade_flag BOOLEAN,
    downgrade_flag BOOLEAN,
    churn_flag BOOLEAN,
    billing_frequency VARCHAR(20),
    auto_renew_flag BOOLEAN);

COPY subscriptions
FROM 'E:/Ravenstack_Project/data/ravenstack_subscriptions.csv'
WITH (FORMAT CSV, HEADER TRUE, DELIMITER ',');

CREATE TABLE churn_events(
	 churn_event_id VARCHAR(20),
    account_id VARCHAR(20),
    churn_date VARCHAR(20),
    reason_code VARCHAR(50),
    refund_amount_usd DECIMAL(10,2),
    preceding_upgrade_flag BOOLEAN,
    preceding_downgrade_flag BOOLEAN,
    is_reactivation BOOLEAN,
    feedback_text TEXT);

COPY churn_events
FROM 'E:/Ravenstack_Project/data/ravenstack_churn_events.csv'
WITH (FORMAT CSV, HEADER TRUE, DELIMITER ',');

CREATE TABLE feature_usage (
    usage_id VARCHAR(20),
    subscription_id VARCHAR(20),
    usage_date VARCHAR(20),
    feature_name VARCHAR(100),
    usage_count INT,
    usage_duration_secs INT,
    error_count INT,
    is_beta_feature BOOLEAN
);

COPY feature_usage
FROM 'E:/Ravenstack_Project/data/ravenstack_feature_usage.csv'
WITH (FORMAT CSV, HEADER TRUE, DELIMITER ',');

CREATE TABLE support_tickets (
    ticket_id VARCHAR(20),
    account_id VARCHAR(20),
    submitted_at VARCHAR(20),
    closed_at VARCHAR(20),
    resolution_time_hours DECIMAL(10,2),
    priority VARCHAR(20),
    first_response_time_minutes INT,
    satisfaction_score DECIMAL(3,2),
    escalation_flag BOOLEAN
);

COPY support_tickets
FROM 'E:/Ravenstack_Project/data/ravenstack_support_tickets.csv'
WITH (FORMAT CSV, HEADER TRUE, DELIMITER ',');


SELECT COUNT(*) AS total_customers FROM accounts;SELECT COUNT(*) AS total_customers FROM accounts;

SELECT 
    COUNT(*) FILTER (WHERE churn_flag = TRUE) AS churned_customers,
    COUNT(*) FILTER (WHERE churn_flag = FALSE) AS active_customers
FROM accounts;

SELECT industry, COUNT(*) AS customer_count
FROM accounts
GROUP BY industry
ORDER BY customer_count DESC;

SELECT 
    plan_tier,
    SUM(mrr_amount) AS total_revenue,
    COUNT(*) AS subscription_count
FROM subscriptions
WHERE churn_flag = FALSE
GROUP BY plan_tier
ORDER BY total_revenue DESC;





















