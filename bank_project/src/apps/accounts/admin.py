from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, TransferReason, Transaction

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'balance')
    list_filter = ('is_staff', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Información bancaria', {'fields': ('balance', 'profile_picture', 'favorite_users')}),
    )
    filter_horizontal = ('favorite_users',) + UserAdmin.filter_horizontal

@admin.register(TransferReason)
class TransferReasonAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'type', 'from_user', 'to_user', 'amount', 'reason')
    list_filter = ('type', 'timestamp', 'reason')
    search_fields = ('from_user__username', 'to_user__username', 'description')
    date_hierarchy = 'timestamp'
    readonly_fields = ('timestamp',)

admin.site.register(User, CustomUserAdmin)
