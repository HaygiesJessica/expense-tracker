from django.urls import path
from .views import *
from .views import get_total_expenses
from .views import get_category_expenditure_current_month


urlpatterns = [
    path('expenses/add', add_expense), #1
    path('expenses/summary/month', get_monthly_expense), #2
    path('expenses/summary/year/<int:year>/', yearly_summary), #3
    path('expenses/category/<str:category>', get_expense_by_category), #4
    path('expenses/budget/set', set_budget), #5
    path('expenses/budget/', get_budget_by_category),#6
    path('expenses/budget/status', get_budget_status), #7
    path('expenses/summary/day/', get_daily_summary), #8
    path("expenses/search", search_expenses, name="search_expenses"), #9
    path("expenses/category/breakdown/", category_expense_breakdown, name="category_expense_breakdown"),#10
    path("expenses/highest", get_highest_expense, name="highest_expense"), #11
    path('expenses/category/total', get_total_expenses, name='total_expenses'), #12 Error -database
    path('expenses/total', get_total_expenses), #13 Error -database
    path('expenses/category/month', get_category_expenditure_current_month, name='category_expenditure_current_month'), #14 Error -database
    path('expenses/date/summary', get_expense_summary_by_date, name='expense_summary_by_date'), #15
    path('expenses/category/history', get_expense_history_for_category, name='expense_history_for_category'), #16 Error -database
    path('expenses/delete', delete_expense, name='delete_expense'), #17
    path('expenses/update/description', update_expense_description, name='update_expense_description'), #18
    path('expenses/budget/total', get_total_budget_for_all_categories, name='total_budget_for_all_categories'), #19 Still Sus
    path('expenses/category/monthly', get_monthly_spend_by_category, name='monthly_spend_by_category'), #20 Error -database
]
