from django.contrib import admin
from .models import Transaction, TransferReason

@admin.register(TransferReason)
class TransferReasonAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    ordering = ('name',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('type', 'from_user', 'to_user', 'amount', 'reason', 'created_at')
    list_filter = ('type', 'reason')
    search_fields = ('from_user__username', 'to_user__username', 'description')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')