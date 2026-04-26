import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

print("\n Loading cleaned data...")
accounts = pd.read_csv('exports/accounts_cleaned.csv')
subscriptions = pd.read_csv('exports/subscriptions_cleaned.csv')
churn_events = pd.read_csv('exports/churn_events_cleaned.csv')
support_tickets = pd.read_csv('exports/support_tickets_cleaned.csv')

accounts['signup_date'] = pd.to_datetime(accounts['signup_date'])
churn_events['churn_date'] = pd.to_datetime(churn_events['churn_date'])

print(" Data loaded\n")

churn_by_industry = accounts.groupby('industry').agg({
    'account_id': 'count',
    'churn_flag': 'sum'
}).rename(columns={'account_id': 'total_customers', 'churn_flag': 'churned_customers'})

churn_by_industry['churn_rate_%'] = (
            churn_by_industry['churned_customers'] / churn_by_industry['total_customers'] * 100).round(2)
churn_by_industry = churn_by_industry.sort_values('churn_rate_%', ascending=False)

print(churn_by_industry)

print(
    f"\n Highest churn industry: {churn_by_industry['churn_rate_%'].idxmax()} ({churn_by_industry['churn_rate_%'].max():.1f}%)")
print(
    f" Lowest churn industry: {churn_by_industry['churn_rate_%'].idxmin()} ({churn_by_industry['churn_rate_%'].min():.1f}%)")

# ANALYSIS 2: Churn Rate by Plan Tier
print("\n" + "=" * 60)
print("ANALYSIS 2: CHURN BY PLAN TIER")
print("=" * 60)

churn_by_plan = accounts.groupby('plan_tier').agg({
    'account_id': 'count',
    'churn_flag': 'sum'
}).rename(columns={'account_id': 'total_customers', 'churn_flag': 'churned_customers'})

churn_by_plan['churn_rate_%'] = (churn_by_plan['churned_customers'] / churn_by_plan['total_customers'] * 100).round(2)
churn_by_plan = churn_by_plan.sort_values('churn_rate_%', ascending=False)

print(churn_by_plan)

print(f"\n Highest churn plan: {churn_by_plan['churn_rate_%'].idxmax()} ({churn_by_plan['churn_rate_%'].max():.1f}%)")
print(f" Lowest churn plan: {churn_by_plan['churn_rate_%'].idxmin()} ({churn_by_plan['churn_rate_%'].min():.1f}%)")

# ANALYSIS 3: Top Churn Reasons
print("\n" + "=" * 60)
print("ANALYSIS 3: TOP CHURN REASONS")
print("=" * 60)

churn_reasons = churn_events['reason_code'].value_counts()
churn_reasons_pct = (churn_reasons / churn_reasons.sum() * 100).round(2)

print("\nChurn Reason Breakdown:")
for reason, count in churn_reasons.items():
    pct = churn_reasons_pct[reason]
    print(f"   {reason:20s}: {count:3d} customers ({pct:5.1f}%)")

print(f"\n #1 Churn Reason: {churn_reasons.index[0]} ({churn_reasons.iloc[0]} customers)")

# ANALYSIS 4: Churn by Referral Source
print("\n" + "=" * 60)
print("ANALYSIS 4: CHURN BY REFERRAL SOURCE")
print("=" * 60)

churn_by_source = accounts.groupby('referral_source').agg({
    'account_id': 'count',
    'churn_flag': 'sum'
}).rename(columns={'account_id': 'total_customers', 'churn_flag': 'churned_customers'})

churn_by_source['churn_rate_%'] = (
            churn_by_source['churned_customers'] / churn_by_source['total_customers'] * 100).round(2)
churn_by_source = churn_by_source.sort_values('churn_rate_%', ascending=False)

print(churn_by_source)

print(
    f"\n Worst performing source: {churn_by_source['churn_rate_%'].idxmax()} ({churn_by_source['churn_rate_%'].max():.1f}%)")
print(
    f" Best performing source: {churn_by_source['churn_rate_%'].idxmin()} ({churn_by_source['churn_rate_%'].min():.1f}%)")

# ANALYSIS 5: Trial Impact on Subscriptions
print("\n" + "=" * 60)
print("ANALYSIS 5: TRIAL vs PAID SUBSCRIPTIONS CHURN")
print("=" * 60)

trial_churn = subscriptions.groupby('is_trial').agg({
    'subscription_id': 'count',
    'churn_flag': 'sum'
}).rename(columns={'subscription_id': 'total', 'churn_flag': 'churned'})

trial_churn['churn_rate_%'] = (trial_churn['churned'] / trial_churn['total'] * 100).round(2)

print(trial_churn)

trial_rate = trial_churn.loc[True, 'churn_rate_%'] if True in trial_churn.index else 0
paid_rate = trial_churn.loc[False, 'churn_rate_%'] if False in trial_churn.index else 0

print(f"\n Trial subscription churn rate: {trial_rate:.1f}%")
print(f" Paid subscription churn rate: {paid_rate:.1f}%")

if trial_rate > paid_rate:
    diff = trial_rate - paid_rate
    print(f"⚠️ Trial subscriptions churn {diff:.1f} percentage points more than paid!")

# ANALYSIS 6: Support Quality Impact
print("\n" + "=" * 60)
print("ANALYSIS 6: SUPPORT QUALITY vs CHURN")
print("=" * 60)

# Merge accounts with support tickets
support_summary = support_tickets.groupby('account_id').agg({
    'ticket_id': 'count',
    'satisfaction_score': 'mean',
    'resolution_time_hours': 'mean',
    'escalation_flag': 'sum'
}).rename(columns={
    'ticket_id': 'total_tickets',
    'satisfaction_score': 'avg_satisfaction',
    'resolution_time_hours': 'avg_resolution_hours',
    'escalation_flag': 'escalations'
})

accounts_support = accounts.merge(support_summary, on='account_id', how='left')

# Compare churned vs active
churned_support = accounts_support[accounts_support['churn_flag'] == True][
    ['avg_satisfaction', 'avg_resolution_hours']].mean()
active_support = accounts_support[accounts_support['churn_flag'] == False][
    ['avg_satisfaction', 'avg_resolution_hours']].mean()

print("\nSupport Metrics Comparison:")
print(f"\n{'Metric':<35} {'Churned':>15} {'Active':>15}")
print("-" * 65)
print(
    f"{'Avg Satisfaction Score':<35} {churned_support['avg_satisfaction']:>15.2f} {active_support['avg_satisfaction']:>15.2f}")
print(
    f"{'Avg Resolution Time (hours)':<35} {churned_support['avg_resolution_hours']:>15.2f} {active_support['avg_resolution_hours']:>15.2f}")

satisfaction_diff = active_support['avg_satisfaction'] - churned_support['avg_satisfaction']
resolution_diff = churned_support['avg_resolution_hours'] - active_support['avg_resolution_hours']

if satisfaction_diff > 0:
    print(f"\n⚠️ Churned customers had {satisfaction_diff:.2f} LOWER satisfaction scores!")

if resolution_diff > 0:
    print(f"⚠️ Churned customers waited {resolution_diff:.2f} hours LONGER for resolution!")

# ANALYSIS 7: Revenue at Risk
print("\n" + "=" * 60)
print("ANALYSIS 7: REVENUE ANALYSIS")
print("=" * 60)

# Merge accounts with subscriptions to get revenue data
accounts_revenue = accounts.merge(
    subscriptions.groupby('account_id')['mrr_amount'].sum().reset_index(),
    on='account_id',
    how='left'
)

churned_revenue = accounts_revenue[accounts_revenue['churn_flag'] == True]['mrr_amount'].sum()
active_revenue = accounts_revenue[accounts_revenue['churn_flag'] == False]['mrr_amount'].sum()
total_revenue = churned_revenue + active_revenue

print(f"\n  Revenue Breakdown:")
print(f"   Lost MRR (churned): ₹{churned_revenue:,.2f}")
print(f"   Active MRR: ₹{active_revenue:,.2f}")
print(f"   Total MRR: ₹{total_revenue:,.2f}")
print(f"\n  Revenue loss: {(churned_revenue / total_revenue * 100):.1f}% of total MRR")

# SUMMARY
print("\n" + "=" * 60)
print("  KEY INSIGHTS SUMMARY")
print("=" * 60)

print(f"""
1. Overall churn rate: {(accounts['churn_flag'].sum() / len(accounts) * 100):.1f}%

2. Highest risk segment:
   - Industry: {churn_by_industry['churn_rate_%'].idxmax()} ({churn_by_industry['churn_rate_%'].max():.1f}% churn)
   - Plan Tier: {churn_by_plan['churn_rate_%'].idxmax()} ({churn_by_plan['churn_rate_%'].max():.1f}% churn)

3. Top 3 churn reasons:
   - #{1}: {churn_reasons.index[0]} ({churn_reasons.iloc[0]} customers, {churn_reasons_pct.iloc[0]:.1f}%)
   - #{2}: {churn_reasons.index[1]} ({churn_reasons.iloc[1]} customers, {churn_reasons_pct.iloc[1]:.1f}%)
   - #{3}: {churn_reasons.index[2]} ({churn_reasons.iloc[2]} customers, {churn_reasons_pct.iloc[2]:.1f}%)

4. Referral source analysis:
   - Worst: {churn_by_source['churn_rate_%'].idxmax()} ({churn_by_source['churn_rate_%'].max():.1f}% churn)
   - Best: {churn_by_source['churn_rate_%'].idxmin()} ({churn_by_source['churn_rate_%'].min():.1f}% churn)

5. Support impact:
   - Churned customers: {churned_support['avg_satisfaction']:.2f} avg satisfaction
   - Active customers: {active_support['avg_satisfaction']:.2f} avg satisfaction
   - Difference: {satisfaction_diff:.2f} points

6. Financial impact:
   - Lost MRR from churn: ₹{churned_revenue:,.2f}
   - Percentage of total revenue: {(churned_revenue / total_revenue * 100):.1f}%
""")

print("=" * 60)
print(" CHURN ANALYSIS COMPLETE!")
print("=" * 60)
print("\n Recommendations:")
print("1. Focus on improving product features (top churn reason)")
print("2. Strengthen support for DevTools industry (31% churn)")
print("3. Investigate why 'event' referrals churn at 30.2%")
print("4. Improve support quality to boost satisfaction scores")
