from django.urls import path
from .views import *
from .views import get_total_expenses
from .views import get_monthly_category_expenses
from .views import get_expense_history
from .views import get_monthly_category_expenses
from .views import get_total_budget
from .views import set_monthly_budget
from .views import get_current_budget

urlpatterns = [
    path('expenses/add', add_expense), #1
    path('expenses/summary/month', get_monthly_expense), #2
    path('expenses/summary/year/<int:year>/', yearly_summary), #3
    path('expenses/category/<str:category>', get_expense_by_category), #4
    path('expenses/budget/set/', set_monthly_budget, name='set-monthly-budget'), #5
    path('expenses/budget/', get_current_budget, name='get-current-budget'), #6
    path('expenses/budget/status', get_budget_status), #7
    path('expenses/summary/day/', get_daily_summary), #8
    path("expenses/search", search_expenses, name="search_expenses"), #9
    path("expenses/category/breakdown/", category_expense_breakdown, name="category_expense_breakdown"),#10
    path("expenses/highest", get_highest_expense, name="highest_expense"), #11
    path('expenses/category/total/', get_total_expenses, name='total-expenses-by-category'), #12
    path('expenses/total', get_total_expenses, name='total_expenses'), #13
    path('expenses/category/month/', get_monthly_category_expenses, name='monthly-category-expenses'),
    path('expenses/date/summary', get_expense_summary_by_date, name='expense_summary_by_date'), #15
    path('expenses/category/history/', get_expense_history, name='category-expense-history'), #16
    path('expenses/delete', delete_expense, name='delete_expense'), #17
    path('expenses/update/description', update_expense_description, name='update_expense_description'), #18
    path('expenses/budget/total/', get_total_budget, name='total_budget_for_all_categories'), #19
    path('expenses/category/monthly/', get_monthly_category_expenses, name='monthly_spend_by_category'), #20
]
