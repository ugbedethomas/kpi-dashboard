from django.contrib import admin
from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('date','order_id','product','category','qty','unit_price','currency')
    search_fields = ('order_id','product','category')
    list_filter = ('category','currency','date')
