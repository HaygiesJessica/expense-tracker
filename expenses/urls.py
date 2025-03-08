from django.urls import path
from .views import *
from .views import get_category_monthly_expense 

urlpatterns = [
    path('expenses/add', add_expense), #1
    path('expenses/summary/month', get_monthly_expense), #2
    path('expenses/summary/year/<int:year>/', yearly_summary), #3
    path('expenses/category/<str:category>', get_expense_by_category), #4
    path('expenses/budget/set', set_budget), #5
    path('expenses/budget/', get_budget_by_category),#6
    path('expenses/budget/status', get_budget_status), #7
    path('expenses/summary/day/', get_daily_summary), #8
    path('expenses/total', get_total_expenses),
    path("expenses/search", search_expenses, name="search_expenses"), #9
    path("expenses/category/breakdown/", category_expense_breakdown, name="category_expense_breakdown"),#10
    path("expenses/highest", get_highest_expense, name="highest_expense"), #11
    path("expenses/category/total", get_total_expense_by_category, name="total_expense_by_category"), #12 error
    path("expenses/category/month", get_category_monthly_expense),
    path('expenses/delete/<int:expense_id>', delete_expense),
]
