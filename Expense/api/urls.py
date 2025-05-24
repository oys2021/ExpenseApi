from django.urls import path
from . import views
from rest_framework_simplejwt.views import (  # type: ignore
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # --- Auth ---
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # --- User Management ---
    path('register/', views.register_user, name='register_user'),
    path('users/', views.list_users, name='list_users'),
    path('user/', views.user_profile, name='user_profile'),
    path('user/total-balance/<str:usr>/', views.user_total_balance, name='user-total-balance'),

    # --- Wallets ---
    path('wallets/', views.wallet_list, name='wallets_list'),
    path('user_wallet_list/<str:usr>/', views.user_wallet_list, name='user_wallet_list'),
    path('wallet/<str:usr>/<int:pk>/', views.wallet_details, name='wallet-detail'),

    # --- Transaction Types & Categories ---
    path('transaction-types/', views.transaction_type_list, name='transaction-type-list'),
    path('transaction-type/<int:pk>/', views.transaction_type_details, name='transaction-type-detail'),
    path('transaction-categories/', views.transaction_category_list, name='transaction-category-list'),
    path('transaction-category/<int:pk>/', views.transaction_category_details, name='transaction-category-detail'),

    # --- Transactions ---
    path('transactions/<str:usr>/', views.transaction_list, name='transaction-list'),
    path('transaction/<str:usr>/<int:pk>/', views.transaction_details, name='transaction-detail'),
    path('transactions_by_day/<str:usr>/', views.transaction_grouped_by_day, name='transactions_by_day'),
    path('transactions_by_week/<str:usr>/', views.transaction_grouped_by_week, name='transactions_by_week'),
    path('transactions_by_month/<str:usr>/', views.transaction_grouped_by_month, name='transactions_by_month'),

    # --- Categories ---
    path('income_category_list/', views.income_category_list, name='income_category_list'),
    path('expense_category_list/', views.expense_category_list, name='expense_category_list'),

    # # --- Protected Example ---
    # path('protected/', views.protected_view, name='protected'),
]
