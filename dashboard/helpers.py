import pandas as pd
from .models import Transaction

def kpi_summary():
    qs = Transaction.objects.all()
    total_revenue = sum(t.amount for t in qs)
    orders = qs.values('order_id').distinct().count()
    aov = (total_revenue / orders) if orders else 0

    # Monthly chart
    df = pd.DataFrame(list(qs.values('date','qty','unit_price')))
    if not df.empty:
        df['amount'] = df['qty'] * df['unit_price']
        df['month'] = pd.to_datetime(df['date']).dt.to_period('M').astype(str)
        monthly = df.groupby('month')['amount'].sum().reset_index()
    else:
        monthly = pd.DataFrame({'month':[], 'amount':[]})

    # Category chart
    df2 = pd.DataFrame(list(qs.values('category','qty','unit_price')))
    if not df2.empty:
        df2['amount'] = df2['qty'] * df2['unit_price']
        cat = df2.groupby('category')['amount'].sum().reset_index().sort_values('amount', ascending=False)
    else:
        cat = pd.DataFrame({'category':[], 'amount':[]})

    return {
        'total_revenue': round(float(total_revenue), 2),
        'orders': orders,
        'aov': round(float(aov), 2),
        'monthly_labels': monthly['month'].tolist(),
        'monthly_values': [round(float(x),2) for x in monthly['amount'].tolist()],
        'cat_labels': cat['category'].fillna('Uncategorized').tolist(),
        'cat_values': [round(float(x),2) for x in cat['amount'].tolist()],
    }
