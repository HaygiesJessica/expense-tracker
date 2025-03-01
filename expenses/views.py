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
def get_total_expense_by_category(request):
    category = request.GET.get("category")  # Get category from request params
    if not category:
        return JsonResponse({"error": "Category is required"}, status=400)

    total = Expense.objects.filter(category=category).aggregate(total_amount=Sum('amount'))
    
    return JsonResponse({
        "category": category,
        "total_expense": total["total_amount"] or 0
    })

# 1️⃣3️⃣ Get Total Expenses for All Categories
@api_view(['GET'])
def get_total_expenses(request):
    total_expense = Expense.objects.aggregate(Sum("amount"))["amount__sum"]
    if total_expense is None:
        total_expense = 0  # Return 0 if no expenses exist
    return Response({"total_expense": total_expense})

# 1️⃣4️⃣ Get Category Expenditure for Current Month
@api_view(['GET'])
def get_category_monthly_expense(request):
    category = request.GET.get("category", None)
    if not category:
        return Response({"error": "Category parameter is required"}, status=400)

    today = now().date()
    first_day = today.replace(day=1)

    total_expense = (
        Expense.objects.filter(category=category, date__gte=first_day, date__lte=today)
        .aggregate(Sum("amount"))
        .get("amount__sum", 0)
    )

    return Response({"category": category, "total_expense": total_expense})

# 1️⃣5️⃣ Get Expense Summary by Date
@api_view(['GET'])
def get_expense_summary(request, date):
    expenses = Expense.objects.filter(date=date)
    serializer = ExpenseSerializer(expenses, many=True)
    return Response(serializer.data)

# 1️⃣6️⃣ Get Expense History for a Category
@api_view(['GET'])
def get_expense_history(request, category):
    expenses = Expense.objects.filter(category=category).order_by('date')
    serializer = ExpenseSerializer(expenses, many=True)
    return Response(serializer.data)

# 1️⃣7️⃣ Delete Specific Expense
@api_view(['DELETE'])
def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)
    expense.delete()
    return Response({'message': 'Expense deleted'})

# 1️⃣8️⃣ Update Expense Description
@api_view(['PUT'])
def update_expense_description(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)
    expense.description = request.data.get('description', expense.description)
    expense.save()
    return Response({'message': 'Expense updated'})

# 1️⃣9️⃣ Get Total Budget for All Categories
@api_view(['GET'])
def get_total_budget(request):
    return Response({'total_budget': 5000})  # Placeholder

# 2️⃣0️⃣ Get Monthly Spend for Each Category
@api_view(['GET'])
def get_monthly_category_expenses(request):
    from django.utils.timezone import now
    expenses = Expense.objects.filter(date__month=now().month).values('category').annotate(total=Sum('amount'))
    return Response(expenses)
