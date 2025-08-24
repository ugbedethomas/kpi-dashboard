from django.shortcuts import render
import pandas as pd
from django.contrib import messages
from django.shortcuts import redirect
from .models import Transaction
from .helpers import kpi_summary

# Create your views here.
from django.http import HttpResponse

def dashboard_home_min(request):
    return HttpResponse("KPI Dashboard — it’s alive ✅")

def dashboard_home_min(request):
    return render(request, "home.html")

def upload_csv(request):
    if request.method == 'POST' and request.FILES.get('file'):
        f = request.FILES['file']
        try:
            if f.name.endswith('.xlsx'):
                df = pd.read_excel(f)
            else:
                df = pd.read_csv(f)
        except Exception as e:
            messages.error(request, f'Upload failed: {e}')
            return redirect('upload_csv')

        df.columns = df.columns.str.lower()
        required = {'date','order_id','product','qty','unit_price'}
        if not required.issubset(set(df.columns)):
            messages.error(request, 'Missing columns: date, order_id, product, qty, unit_price')
            return redirect('upload_csv')

        df['category'] = df.get('category', 'General')
        df['currency'] = df.get('currency', 'NGN')
        df['date'] = pd.to_datetime(df['date']).dt.date
        df['qty'] = df['qty'].fillna(1).astype(int)
        df['unit_price'] = df['unit_price'].astype(float)

        objs = [Transaction(
            date=row['date'], order_id=str(row['order_id']), product=str(row['product']),
            category=str(row.get('category','General'))[:64], qty=int(row['qty']),
            unit_price=float(row['unit_price']), currency=str(row.get('currency','NGN'))[:8]
        ) for _, row in df.iterrows()]
        Transaction.objects.bulk_create(objs)
        messages.success(request, f'Uploaded {len(objs)} records!')
        return redirect('home')

    return render(request, "upload.html")
def dashboard_home_min(request):
    kpis = kpi_summary()
    return render(request, "dashboard_home.html", {"kpis": kpis})
from django.http import HttpResponse
import csv
from io import BytesIO

def export_csv(request):
    qs = Transaction.objects.all().order_by('date')
    resp = HttpResponse(content_type='text/csv')
    resp['Content-Disposition'] = 'attachment; filename="transactions.csv"'
    w = csv.writer(resp)
    w.writerow(['date','order_id','product','category','qty','unit_price','currency','amount'])
    for t in qs:
        w.writerow([t.date, t.order_id, t.product, t.category, t.qty, t.unit_price, t.currency, t.amount])
    return resp

def export_xlsx(request):
    qs = Transaction.objects.all().order_by('date')
    import pandas as pd
    df = pd.DataFrame([{
        'date': t.date,'order_id': t.order_id,'product': t.product,'category': t.category,
        'qty': t.qty,'unit_price': t.unit_price,'currency': t.currency,'amount': t.amount
    } for t in qs])
    bio = BytesIO()
    with pd.ExcelWriter(bio, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Transactions')
    bio.seek(0)
    resp = HttpResponse(bio.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    resp['Content-Disposition'] = 'attachment; filename="transactions.xlsx"'
    return resp
