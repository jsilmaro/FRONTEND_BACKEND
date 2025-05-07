from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (RegisterView, LoginView, get_active_accounts, LogoutView,
                    TransactionViewSet, BudgetViewSet, dashboard_summary,
                    recent_transactions, spending_by_category)

urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
    path("auth/user/", get_active_accounts, name="get_user"),
    path("auth/active-accounts/",
         get_active_accounts,
         name="get_active_accounts"),
    path('auth/token/refresh/',
         TokenRefreshView.as_view(),
         name='token_refresh'),

    # Transaction endpoints
    path('transactions/', TransactionViewSet.as_view(), name='transactions'),
    path('budgets/', BudgetViewSet.as_view(), name='budgets'),

    # Dashboard endpoints
    path('dashboard/summary/', dashboard_summary, name='dashboard_summary'),
    path('dashboard/recent-transactions/',
         recent_transactions,
         name='recent_transactions'),

    # Report endpoints
    path('reports/spending-by-category/',
         spending_by_category,
         name='spending_by_category'),
]
