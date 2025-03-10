from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Expense
from .serializers import ExpenseSerializer
from django.db.models import Sum
from datetime import datetime
from django.utils.timezone import now
from django.http import JsonResponse
from expenses.models import Expense

# 1️⃣ Add New Expense
@api_view(['POST'])
def add_expense(request):
    serializer = ExpenseSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 2️⃣ Get Monthly Expense Summary
@api_view(['GET'])
def get_monthly_expense(request):
    from django.utils.timezone import now
    total = Expense.objects.filter(date__month=now().month).aggregate(Sum('amount'))
    return Response({'monthly_expense': total['amount__sum']})

# 3️⃣ Get Yearly Expense Summary
@api_view(["GET"])
def yearly_summary(request, year):
    total_expense = Expense.objects.filter(date__year=year).aggregate(Sum("amount"))
    print(f"Year: {year}, Expenses Found: {total_expense}")  # Debugging
    return Response({"yearly_expense": total_expense["amount__sum"]})

# 4️⃣ Get Expense by Category
@api_view(['GET'])
def get_expense_by_category(request, category):
    expenses = Expense.objects.filter(category=category)
    serializer = ExpenseSerializer(expenses, many=True)
    return Response(serializer.data)

# 5️⃣ Set Monthly Budget
@api_view(['POST'])
def set_budget(request):
    category = request.data.get('category')  # Get category from request
    budget_amount = request.data.get('budget_amount')  # Get budget amount

    if not category or not budget_amount:
        return Response({'error': 'Category and budget_amount are required'}, status=400)

    return Response({
        'message': 'Budget set successfully',
        'category': category,
        'budget_amount': budget_amount
    })

# 6️⃣ Get Current Budget
@api_view(['GET'])
def get_budget_by_category(request):
    category = request.GET.get('category')  # Get category from query params

    if not category:
        return Response({'error': 'Category parameter is required'}, status=400)

    # Mocked budget for now (replace with database query)
    budget_data = {
        "Food": 5000,
        "Transport": 2000
    }

    budget_amount = budget_data.get(category, None)

    if budget_amount is None:
        return Response({'error': 'No budget found for this category'}, status=404)

    return Response({
        'category': category,
        'budget_amount': budget_amount
    })

# 7️⃣ Track Spending Against Budget
@api_view(['GET'])
def get_budget_status(request):
    category = request.GET.get('category')  # Get category from query params

    if not category:
        return Response({'error': 'Category parameter is required'}, status=400)

    # Mocked budget for now (replace with database query)
    budget_data = {
        "Food": 5000,
        "Transport": 2000
    }

    budget_amount = budget_data.get(category, None)

    if budget_amount is None:
        return Response({'error': 'No budget found for this category'}, status=404)

    return Response({
        'category': category,
        'budget_amount': budget_amount
    })

# 8️⃣ Get Total Expenses for a Specific Day
@api_view(['GET'])
def get_daily_summary(request):
    date = request.GET.get('date')  # Example: 2024-02-26

    if not date:
        return Response({'error': 'Date parameter is required'}, status=400)

    try:
        datetime.strptime(date, "%Y-%m-%d")  # Validate date format
    except ValueError:
        return Response({'error': 'Invalid date format, use YYYY-MM-DD'}, status=400)

    # ✅ Fetch expenses from the database where `date` matches the given date
    daily_expenses = Expense.objects.filter(date=date)

    if not daily_expenses.exists():
        return Response({'message': 'No expenses found for this date'})

    total_spent = sum(exp.amount for exp in daily_expenses)

    # ✅ Convert expenses into a list of dictionaries for the response
    expenses_list = [
        {"date": str(exp.date), "category": exp.category, "amount": exp.amount}
        for exp in daily_expenses
    ]

    return Response({
        "date": date,
        "total_spent": total_spent,
        "expenses": expenses_list
    })

# 9️⃣ Search Expenses by Date Range
@api_view(['GET'])
def search_expenses(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if not start_date or not end_date:
        return Response({'error': 'Both start_date and end_date are required'}, status=400)

    try:
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
    except ValueError:
        return Response({'error': 'Invalid date format, use YYYY-MM-DD'}, status=400)

    # ✅ Query the database to get expenses between the given dates
    expenses = Expense.objects.filter(date__range=[start_date, end_date])

    if not expenses.exists():
        return Response({'message': 'No expenses found in the given date range'})

    # ✅ Convert expenses to a list of dictionaries
    expenses_list = [
        {"date": str(exp.date), "category": exp.category, "amount": exp.amount}
        for exp in expenses
    ]

    return Response({
        "start_date": str(start_date),
        "end_date": str(end_date),
        "total_expenses": len(expenses_list),
        "expenses": expenses_list
    })

# 🔟 Get Category-wise Expense Breakdown
@api_view(['GET'])
def category_expense_breakdown(request):
    # ✅ Aggregate total expense per category
    breakdown = Expense.objects.values("category").annotate(total_amount=Sum("amount"))

    # ✅ If no expenses found
    if not breakdown.exists():
        return Response({'message': 'No expenses recorded'})

    # ✅ Convert to a list of dictionaries
    breakdown_list = [
        {"category": item["category"], "total_amount": item["total_amount"]}
        for item in breakdown
    ]

    return Response({
        "total_categories": len(breakdown_list),
        "breakdown": breakdown_list
    })

# 1️⃣1️⃣ Get Most Expensive Expense
@api_view(['GET'])
def get_highest_expense(request):
    highest_expense = Expense.objects.order_by('-amount').first()

    if not highest_expense:
        return Response({"message": "No expenses found"}, status=404)

    return Response({
        "category": highest_expense.category,
        "amount": highest_expense.amount,
        "date": highest_expense.date.strftime("%Y-%m-%d")
    })

# 1️⃣2️⃣ Get Total Expenses for a Category ***
@api_view(['GET'])
def get_total_expenses(request):
    # Extract the 'category' query parameter
    category = request.GET.get("category")
    if not category:
        return Response({"error": "Category is required"}, status=400)

    # Query the database to calculate the total expenses for the specified category
    total = Expense.objects.filter(category__iexact=category).aggregate(total_amount=Sum('amount'))

    # Return the total expenses (or 0 if no expenses are found)
    return Response({
        "category": category,
        "total_expense": total["total_amount"] or 0
    })

# 1️⃣4️⃣ Get Category Expenditure for Current Month
@api_view(['GET'])
def get_category_expenditure_current_month(request):
    # Extract the 'category' query parameter
    category = request.GET.get("category")
    if not category:
        return Response({"error": "Category is required"}, status=400)

    # Get the current month and year
    today = datetime.today()
    current_month = today.month
    current_year = today.year

    # Query the database to calculate the total expenses for the specified category in the current month
    total = Expense.objects.filter(
        category__iexact=category,
        date__month=current_month,
        date__year=current_year
    ).aggregate(total_amount=Sum('amount'))

    # Return the total expenses (or 0 if no expenses are found)
    return Response({
        "category": category,
        "month": today.strftime("%B"),  # Full month name (e.g., "October")
        "year": current_year,
        "total_expense": total["total_amount"] or 0
    })

#15th Endpoint
@api_view(['GET'])
def get_expense_summary_by_date(request):
    # Extract the 'date' query parameter
    date_str = request.GET.get("date")
    if not date_str:
        return Response({"error": "Date is required (format: YYYY-MM-DD)"}, status=400)

    try:
        # Parse the date string into a Python date object
        target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return Response({"error": "Invalid date format. Use YYYY-MM-DD"}, status=400)

    # Query the database to fetch all expenses for the specified date
    expenses = Expense.objects.filter(date=target_date)

    # Prepare the summary response
    summary = {
        "date": target_date.strftime("%Y-%m-%d"),
        "total_expense": expenses.aggregate(total_amount=Sum('amount'))["total_amount"] or 0,
        "expenses": [
            {
                "id": expense.id,
                "category": expense.category,
                "amount": str(expense.amount),  # Convert Decimal to string for JSON serialization
                "description": expense.description if hasattr(expense, 'description') else None
            }
            for expense in expenses
        ]
    }

    return Response(summary)

#16th Endpoint
@api_view(['GET'])
def get_expense_history_for_category(request):
    # Extract the 'category' query parameter
    category = request.GET.get("category")
    if not category:
        return Response({"error": "Category is required"}, status=400)

    # Query the database to fetch all expenses for the specified category
    expenses = Expense.objects.filter(category__iexact=category).order_by('date')

    # Prepare the response data
    expense_history = [
        {
            "id": expense.id,
            "amount": str(expense.amount),  # Convert Decimal to string for JSON serialization
            "date": expense.date.strftime("%Y-%m-%d"),
            "description": expense.description if hasattr(expense, 'description') else None
        }
        for expense in expenses
    ]

    return Response({
        "category": category,
        "total_expenses": len(expense_history),
        "expense_history": expense_history
    })

#17th Enpoint
@api_view(['DELETE'])
def delete_expense(request):
    expense_id = request.GET.get("expense_id")
    if not expense_id:
        return Response({"error": "Expense ID is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        expense = Expense.objects.get(id=expense_id)
    except Expense.DoesNotExist:
        return Response({"error": f"Expense with ID {expense_id} not found"}, status=status.HTTP_404_NOT_FOUND)

    expense.delete()

    return Response({
        "message": f"Expense with ID {expense_id} has been deleted",
        "deleted_expense": {
            "id": expense_id,
            "category": expense.category,
            "amount": str(expense.amount),
            "date": expense.date.strftime("%Y-%m-%d"),
            "description": expense.description if hasattr(expense, 'description') else None
        }
    }, status=status.HTTP_200_OK)

#18th Endpoint
@api_view(['PUT'])
def update_expense_description(request):
    # Extract the 'expense_id' and 'new_description' query parameters
    expense_id = request.GET.get("expense_id")
    new_description = request.GET.get("new_description")

    if not expense_id:
        return Response({"error": "Expense ID is required"}, status=status.HTTP_400_BAD_REQUEST)
    if not new_description:
        return Response({"error": "New description is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Fetch the expense by ID
        expense = Expense.objects.get(id=expense_id)
    except Expense.DoesNotExist:
        return Response({"error": f"Expense with ID {expense_id} not found"}, status=status.HTTP_404_NOT_FOUND)

    # Update the description
    old_description = expense.description
    expense.description = new_description
    expense.save()

    # Return confirmation of the update
    return Response({
        "message": f"Description for expense ID {expense_id} has been updated",
        "updated_expense": {
            "id": expense.id,
            "category": expense.category,
            "amount": str(expense.amount),  # Convert Decimal to string for JSON serialization
            "date": expense.date.strftime("%Y-%m-%d"),
            "old_description": old_description,
            "new_description": expense.description
        }
    }, status=status.HTTP_200_OK)

#19th Endpoint
@api_view(['GET'])
def get_total_budget_for_all_categories(request):
    # Query the database to calculate the total amount of expenses
    total_expenses = Expense.objects.aggregate(total_amount=Sum('amount'))['total_amount'] or 0

    # Return the total amount
    return Response({
        "total_expenses": total_expenses
    })

#20th Endpoint
@api_view(['GET'])
def get_monthly_spend_by_category(request):
    # Get the current year and month
    today = datetime.today()
    current_year = today.year
    current_month = today.month

    # Query the database to calculate the total expenses for each category in the current month
    monthly_expenses = (
        Expense.objects
        .filter(date__year=current_year, date__month=current_month)
        .values('category')
        .annotate(total_amount=Sum('amount'))
        .order_by('category')
    )

    # Prepare the response data
    expense_summary = [
        {
            "category": entry['category'],
            "total_amount": str(entry['total_amount'])  # Convert Decimal to string for JSON serialization
        }
        for entry in monthly_expenses
    ]

    return Response({
        "month": today.strftime("%B %Y"),  # e.g., "March 2025"
        "expense_summary": expense_summary
    })
