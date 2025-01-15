from django.contrib import admin
from api.models import *
# Register your models here.
admin.site.register(Transaction)
admin.site.register(TransactionCategory)
admin.site.register(TransactionType)
admin.site.register(Wallet)
admin.site.register(Customuser)
