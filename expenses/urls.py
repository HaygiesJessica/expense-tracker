from django.urls import path
from .views import *
from .views import get_category_monthly_expense 

urlpatterns = [
    path('expenses/add', add_expense),
    path('expenses/summary/month', get_monthly_expense),
    path('expenses/summary/year/<int:year>/', yearly_summary),
    path('expenses/category/<str:category>', get_expense_by_category),
    path('expenses/budget/set', set_budget),
    path('expenses/budget/', get_budget_by_category),
    path('expenses/budget/status', get_budget_status), 
    path('expenses/summary/day/', get_daily_summary),
    path('expenses/total', get_total_expenses),
    path("expenses/search", search_expenses, name="search_expenses"),
    path("expenses/category/breakdown/", category_expense_breakdown, name="category_expense_breakdown"),
    path("expenses/highest", get_highest_expense, name="highest_expense"), 
    path("expenses/category/total", get_total_expense_by_category, name="total_expense_by_category"),
    path("expenses/category/month", get_category_monthly_expense),
    path('expenses/delete/<int:expense_id>', delete_expense),
]
