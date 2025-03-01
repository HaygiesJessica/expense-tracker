from django.contrib import admin
from django.urls import include, path
from django.http import JsonResponse

# Simple welcome page for the root URL
def home(request):
    return JsonResponse({"message": "Welcome to the Expense Tracker API!"})

urlpatterns = [
    path('', home),  # Root URL
    path('admin/', admin.site.urls),
    path('api/', include('expenses.urls')),  # API routes
]
