from django.contrib import admin
from .models import Wallet, Transaction, Category, WalletInvitation, FutureTransaction


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'balance', 'objective')
    list_filter = ('owner',)
    search_fields = ('name', 'owner__email', 'users__email')
    filter_horizontal = ('users',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('title', 'wallet', 'user', 'amount', 'is_income', 'date')
    list_filter = ('is_income', 'wallet', 'category', 'user')
    search_fields = ('title', 'description', 'wallet__name', 'user__email')
    date_hierarchy = 'date'

@admin.register(FutureTransaction)
class FutureTransactionAdmin(admin.ModelAdmin):
    list_display = ('title', 'wallet', 'execution_date', 'frequency', 'active')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(WalletInvitation)
class WalletInvitationAdmin(admin.ModelAdmin):
    list_display = ('wallet', 'created_by', 'token', 'is_used', 'expires_at')
    list_filter = ('is_used', 'wallet')
    search_fields = ('wallet__name', 'created_by__email', 'token')
    readonly_fields = ('token', 'created_at', 'expires_at')

    def has_add_permission(self, request):
        return False

