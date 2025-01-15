from django.shortcuts import render
from rest_framework.response import  Response
from rest_framework import status
from api.models import *
from api.serializers import *
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.db.models import Sum
from decimal import Decimal
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime
from collections import defaultdict
# from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer


@api_view(['GET','POST'])
@permission_classes([AllowAny])
def wallet_list(request,usr):
    if request.method =="GET":
        wallet=Wallet.objects.filter(user__username=usr)
        serializer=WalletSerializer(wallet,many=True,context={'request': request})
        formatted_data = [{"label": wallets.name, "value": wallets.name} for wallets in wallet]
        return Response(serializer.data)
    
    elif request.method == "POST":
        data=request.data
        print(data.get('name'))
        existing_wallet = Wallet.objects.filter(user__username=usr, name=data.get('name')).exists()
        
        if existing_wallet:
            return Response({'error': 'Wallet with this name already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer=WalletSerializer(data=data,context={'request': request})
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def user_list(request):
    if request.method == "GET":
        users = Customuser.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
    elif request.method == "POST":
        data = request.data
        if Customuser.objects.filter(username=data.get('username')).exists():
            return Response({"detail": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)
        
        if Customuser.objects.filter(email=data.get('email')).exists():
            return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = UserSerializer(data=data)
        
        # user=User.objects.get(username=data.get('username'))
        
        
        if serializer.is_valid():
            user=serializer.save()
            
            refresh = RefreshToken.for_user(user)
            access = refresh.access_token
            return Response(
            {
                **serializer.data, 
                'access': str(access),
                'refresh': str(refresh),
            },
    status=status.HTTP_201_CREATED
)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    
    
@api_view(['GET','PUT'])
@permission_classes([AllowAny])
def single_user_list(request,usr):
    if request.method == "GET":
        user = Customuser.objects.get(username=usr)
        serializer = UserSerializer(user,context={'request': request})
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        user=Customuser.objects.get(username=usr)
        data=request.data
        serializer = UserSerializer(user, data=data, partial=True,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email=request.data.get('email')
    user = authenticate(username=username, password=password)

    if user:
        return Response({"message": "Login successful"}, status=200)
    else:
        return Response({"error": "Invalid username or password"}, status=401)

@api_view(['GET','PUT','DELETE'])
@permission_classes([AllowAny])
def wallet_details(request,usr,pk):
    try:
        wallet=Wallet.objects.get(user__username=usr,pk=pk)
    except Wallet.DoesNotExist:
        return Response({'error': 'Wallet not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        serializer=WalletSerializer(wallet,context={'request': request})
        return Response(serializer.data)
    
    elif request.method =="PUT":
        serializer=WalletSerializer(wallet,data=request.data,partial=True,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method =="DELETE":
        wallet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
@api_view(["GET","POST"])
@permission_classes([AllowAny])
def transaction_type_list(request):
    if request.method =="GET":
        transaction_type=TransactionType.objects.all()
        serializer=TransactionTypeSerializer(transaction_type,many=True)
        return Response(serializer.data)
    
    elif request.method == "POST":
        serializer=TransactionTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET","PUT","DELETE"])
@permission_classes([AllowAny])
def transaction_type_details(request,pk):
    try:
        transaction_type=TransactionType.objects.get(pk=pk)
        
    except TransactionType.DoesNotExist:
        return Response({'error': 'TransactionType not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method =="GET":
        serializer=TransactionTypeSerializer(transaction_type)
        return Response(serializer.data)
    
    
    elif request.method == "PUT":
        serializer=TransactionTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
        
    elif request.method == "DELETE":
        transaction_type.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
@api_view(["GET","POST"])
@permission_classes([AllowAny])
def transaction_category_list(request):
    transaction_category=TransactionCategory.objects.all()
    
    if request.method == "GET":
        serializer=TransactionCategorySerializer(transaction_category,many=True)
        return Response(serializer.data)
    
    elif request.method =="POST":
        serializer=TransactionCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(["GET","PUT","DELETE"])   
@permission_classes([AllowAny]) 
def transaction_category_details(request,pk):
    try:
        transaction_category=TransactionCategory.objects.get(pk,pk)
        
    except TransactionCategory.DoesNotExist:
        return Response({'error': 'TransactionCategory not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method =="GET":
        serializer=TransactionCategorySerializer(transaction_category)
        return Response(serializer.data)
    
    elif request.method =="PUT":
        serializer=TransactionCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method =="DELETE":
        transaction_category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(["GET", "POST"]) 
@permission_classes([AllowAny])
def transaction_list(request, usr):
    transactions = Transaction.objects.filter(user__username=usr)

    if request.method == "GET":
        total_income = Decimal(transactions.filter(transaction_type__name='Income').aggregate(total=Sum('amount'))['total'] or 0)
        total_expense = Decimal(transactions.filter(transaction_type__name='Expense').aggregate(total=Sum('amount'))['total'] or 0)

        serializer = TransactionSerializer(transactions, many=True)

        response_data = {
            "transactions": serializer.data,
            "total_income": total_income,  
            "total_expense":total_expense
        }

        return Response(response_data)

    elif request.method == "POST":
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   
    
    
@api_view(["GET","PUT","DELETE"])  
@permission_classes([AllowAny])  
def transaction_details(request,usr,pk):
    try:
        transaction=Transaction.objects.get(user__username=usr,pk=pk)
        
    except Transaction.DoesNotExist:
        return Response({'error': 'Transaction not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method =="GET":
        serializer=TransactionSerializer(transaction)
        return Response(serializer.data)
    
    elif request.method =="PUT":
        serializer=TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method =="DELETE":
        transaction.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
          



@api_view(['GET'])
@permission_classes([AllowAny])
def user_total_balance(request, usr):
    try:
        user = Customuser.objects.get(username=usr)
        total_balance = Wallet.objects.filter(user=user).aggregate(Sum('balance'))['balance__sum']
        total_balance = Decimal(total_balance or 0).quantize(Decimal('0.00'))
        return Response({'username': user.username, 'total_balance': str(total_balance)})
    except Customuser.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
    
                



from datetime import datetime, timedelta
from django.utils import timezone

from datetime import datetime, timedelta
from collections import defaultdict
from decimal import Decimal
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

@api_view(["GET"])
@permission_classes([AllowAny])
def transaction_grouped_by_day(request, usr):
    # Get the current date and time in the local timezone
    today = timezone.localtime(timezone.now()).date()
    
    # Calculate the start of the current week (Monday)
    start_of_week = today - timedelta(days=today.weekday())  # Monday of the current week
    
    # Calculate the end of the current week (Sunday, 23:59:59)
    end_of_week = start_of_week + timedelta(days=6)
    
    # Filter the transactions based on the user and current week
    transactions = Transaction.objects.filter(
        user__username=usr,
        date__gte=start_of_week,  # Only transactions from the current week
        date__lte=end_of_week + timedelta(days=1),  # Include transactions up to Sunday 23:59:59
    )
    
    # Group data by day
    grouped_data = defaultdict(lambda: {'income': Decimal(0), 'expense': Decimal(0)})
    
    for transaction in transactions:
        # Get the day of the week from the transaction date (e.g., Mon, Tue, etc.)
        date_str = transaction.date.strftime('%a')  # Get short day name (Mon, Tue, etc.)
        
        # Update income or expense based on the transaction type
        if transaction.transaction_type.name == 'Income':
            grouped_data[date_str]['income'] += Decimal(transaction.amount)
        elif transaction.transaction_type.name == 'Expense':
            grouped_data[date_str]['expense'] += Decimal(transaction.amount)
    
    # Define the days of the week (just for ordering purposes)
    days_of_week = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    
    # Prepare the labels and data for the response
    labels = days_of_week
    income_data = []
    expense_data = []
    
    for day in days_of_week:
        income_data.append(grouped_data[day]['income'])
        expense_data.append(grouped_data[day]['expense'])
        
    serializer=TransactionSerializer(transactions,many=True)
    
    data = {
        "labels": labels,
        "datasets": [
            {
                "data": list(zip(income_data, expense_data)),
            },
        ],
        "transactions":serializer.data
    }
    
    return Response(data)





@api_view(["GET"])
@permission_classes([AllowAny])
def transaction_grouped_by_week(request, usr):
    
    today = timezone.localtime(timezone.now()).date()  
    current_year = today.year
    current_month = today.month
    
    first_day_of_month = datetime(current_year, current_month, 1).date()  # Use .date() to avoid datetime object
    last_day_of_month = datetime(current_year, current_month + 1, 1).date() - timedelta(days=1)  # .date() here too
    
    start_of_week = first_day_of_month - timedelta(days=first_day_of_month.weekday())  # Start from the Monday of the first week
    weeks = []
    while start_of_week <= last_day_of_month:
        end_of_week = start_of_week + timedelta(days=6)
        weeks.append((start_of_week, min(end_of_week, last_day_of_month)))  # Ensure end is within the month
        start_of_week = end_of_week + timedelta(days=1)  # Move to the next week
    
    # Initialize a dictionary to hold the weekly data
    grouped_data = defaultdict(lambda: {'income': Decimal(0), 'expense': Decimal(0)})
    
    # Get all transactions for the user within the current month
    transactions = Transaction.objects.filter(
        user__username=usr,
        date__gte=first_day_of_month,
        date__lte=last_day_of_month,
    )
    
    # Group transactions by week
    for transaction in transactions:
        transaction_date = transaction.date.date()  # Extract the date part (ignore time)
        
        for week_start, week_end in weeks:
            if week_start <= transaction_date <= week_end:  # Compare only date parts
                week_label = f"Week {weeks.index((week_start, week_end)) + 1}"
                
                if transaction.transaction_type.name == 'Income':
                    grouped_data[week_label]['income'] += Decimal(transaction.amount)
                elif transaction.transaction_type.name == 'Expense':
                    grouped_data[week_label]['expense'] += Decimal(transaction.amount)
                break
    
    # Prepare labels and data for the response
    labels = [f"Week {i+1}" for i in range(len(weeks))]
    income_data = []
    expense_data = []
    
    for label in labels:
        income_data.append(grouped_data[label]['income'])
        expense_data.append(grouped_data[label]['expense'])
    
    serializer=TransactionSerializer(transactions,many=True)
    
    data = {
        "labels": labels,
        "datasets": [
            {
                "data": list(zip(income_data, expense_data)),
            },
        ],
        "transactions":serializer.data
    }
    
    return Response(data)

    

@api_view(["GET"])
@permission_classes([AllowAny])
def transaction_grouped_by_month(request, usr):
    # Get the current date
    today = timezone.localtime(timezone.now()).date()  
    current_year = today.year  

    first_day_of_year = datetime(current_year, 1, 1).date()
    last_day_of_year = datetime(current_year, 12, 31).date()

    grouped_data = defaultdict(lambda: {'income': Decimal(0), 'expense': Decimal(0)})

    transactions = Transaction.objects.filter(
        user__username=usr,
        date__gte=first_day_of_year,
        date__lte=last_day_of_year,
    )
    
    for transaction in transactions:
        transaction_date = transaction.date.date()  # Extract the date part (ignore time)
        
        # Use abbreviated month names ('Jan', 'Feb', etc.)
        month_label = transaction_date.strftime('%b')  # Abbreviated month name (e.g., 'Jan', 'Feb')
        
        if transaction.transaction_type.name == 'Income':
            grouped_data[month_label]['income'] += Decimal(transaction.amount)
        elif transaction.transaction_type.name == 'Expense':
            grouped_data[month_label]['expense'] += Decimal(transaction.amount)

    # Prepare labels (months) and data for the response
    months_of_year = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                      'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    income_data = []
    expense_data = []
    
    # For each month in the year, get the total income and expense
    for month in months_of_year:
        income_data.append(grouped_data[month]['income'])
        expense_data.append(grouped_data[month]['expense'])

    # Serialize transactions for the response
    serializer = TransactionSerializer(transactions, many=True)
    
    data = {
        "labels": months_of_year,
        "datasets": [
            {
                "data": list(zip(income_data, expense_data)),
            },
        ],
        "transactions": serializer.data
    }
    
    return Response(data)


@api_view(['GET'])
@permission_classes([AllowAny])  
def income_category_list(request):
    if request.method == "GET":
        income_type = TransactionType.objects.filter(name='Income').first()

        categories = TransactionCategory.objects.filter(transaction_type=income_type)
 
        serializer = TransactionCategorySerializer(categories, many=True, context={'request': request})
        formatted_data = [{"label": category.name, "value": category.name} for category in categories]

        return Response(formatted_data)
    
@api_view(['GET'])
@permission_classes([AllowAny])  
def expense_category_list(request):
    if request.method == "GET":
        expense_type = TransactionType.objects.filter(name='Expense').first()

        categories = TransactionCategory.objects.filter(transaction_type=expense_type)
 
        serializer = TransactionCategorySerializer(categories, many=True, context={'request': request})
        formatted_data = [{"label": category.name, "value": category.name} for category in categories]

        return Response(formatted_data)
    
    
@api_view(['GET'])
@permission_classes([AllowAny])  
def user_wallet_list(request,usr):
    if request.method == "GET":
        wallet=Wallet.objects.filter(user__username=usr) 
        formatted_data = [{"label": wallets.name, "value": wallets.name} for wallets in wallet]
        return Response(formatted_data)
    

        
