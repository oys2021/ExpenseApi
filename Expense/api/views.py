from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Sum
from decimal import Decimal
from datetime import datetime, timedelta
from collections import defaultdict

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken

from api.models import *
from api.serializers import *

# -------------------- AUTH & USERS --------------------

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            "user": serializer.data,
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAdminUser])  # type: ignore
def list_users(request):
    users = Customuser.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    user = request.user
    if request.method == 'GET':
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# -------------------- WALLETS --------------------

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def wallet_list(request):
    user = request.user
    if request.method == 'GET':
        wallets = Wallet.objects.filter(user=user)
        serializer = WalletSerializer(wallets, many=True, context={'request': request})
        return Response(serializer.data)

    if Wallet.objects.filter(user=user, name=request.data.get('name')).exists():
        return Response({'error': 'Wallet with this name already exists'}, status=status.HTTP_400_BAD_REQUEST)

    serializer = WalletSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save(user=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def wallet_details(request, usr, pk):
    if request.user.username != usr:
        return Response({'error': 'Unauthorized access'}, status=status.HTTP_403_FORBIDDEN)

    wallet = get_object_or_404(Wallet, user=request.user, pk=pk)

    if request.method == 'GET':
        serializer = WalletSerializer(wallet, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = WalletSerializer(wallet, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        wallet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([AllowAny])
def user_total_balance(request, usr):
    if request.user.username != usr:
        return Response({'error': 'Unauthorized access'}, status=status.HTTP_403_FORBIDDEN)

    user = get_object_or_404(Customuser, username=usr)
    total_balance = Wallet.objects.filter(user=user).aggregate(Sum('balance'))['balance__sum'] or 0
    total_balance = Decimal(total_balance).quantize(Decimal('0.00'))
    return Response({'username': user.username, 'total_balance': str(total_balance)})


@api_view(['GET'])
@permission_classes([AllowAny])
def user_wallet_list(request, usr):
    wallets = Wallet.objects.filter(user__username=usr)
    formatted_data = [{"label": wallet.name, "value": wallet.name} for wallet in wallets]
    return Response(formatted_data)


# -------------------- TRANSACTION TYPES --------------------

@api_view(['GET', 'POST'])
def transaction_type_list(request):
    if request.method == 'GET':
        transaction_types = TransactionType.objects.all()
        serializer = TransactionTypeSerializer(transaction_types, many=True)
        return Response(serializer.data)
    serializer = TransactionTypeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def transaction_type_details(request, pk):
    transaction_type = get_object_or_404(TransactionType, pk=pk)

    if request.method == 'GET':
        serializer = TransactionTypeSerializer(transaction_type)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = TransactionTypeSerializer(transaction_type, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        transaction_type.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# -------------------- TRANSACTION CATEGORIES --------------------

@api_view(['GET', 'POST'])
def transaction_category_list(request):
    if request.method == 'GET':
        categories = TransactionCategory.objects.all()
        serializer = TransactionCategorySerializer(categories, many=True)
        return Response(serializer.data)
    serializer = TransactionCategorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def transaction_category_details(request, pk):
    category = get_object_or_404(TransactionCategory, pk=pk)

    if request.method == 'GET':
        serializer = TransactionCategorySerializer(category)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = TransactionCategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([AllowAny])
def income_category_list(request):
    income_type = TransactionType.objects.filter(name='Income').first()
    categories = TransactionCategory.objects.filter(transaction_type=income_type)
    formatted_data = [{"label": c.name, "value": c.name} for c in categories]
    return Response(formatted_data)


@api_view(['GET'])
@permission_classes([AllowAny])
def expense_category_list(request):
    expense_type = TransactionType.objects.filter(name='Expense').first()
    categories = TransactionCategory.objects.filter(transaction_type=expense_type)
    formatted_data = [{"label": c.name, "value": c.name} for c in categories]
    return Response(formatted_data)


# -------------------- TRANSACTIONS --------------------

@api_view(['GET', 'POST'])
def transaction_list(request, usr):
    if request.user.username != usr:
        return Response({'error': 'Unauthorized access'}, status=status.HTTP_403_FORBIDDEN)

    transactions = Transaction.objects.filter(user__username=usr)

    if request.method == 'GET':
        total_income = transactions.filter(transaction_type__name='Income').aggregate(total=Sum('amount'))['total'] or 0
        total_expense = transactions.filter(transaction_type__name='Expense').aggregate(total=Sum('amount'))['total'] or 0

        serializer = TransactionSerializer(transactions, many=True)
        return Response({
            "transactions": serializer.data,
            "total_income": Decimal(total_income),
            "total_expense": Decimal(total_expense)
        })

    serializer = TransactionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def transaction_details(request, usr, pk):
    if request.user.username != usr:
        return Response({'error': 'Unauthorized access'}, status=status.HTTP_403_FORBIDDEN)

    transaction = get_object_or_404(Transaction, user__username=usr, pk=pk)

    if request.method == 'GET':
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = TransactionSerializer(transaction, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        transaction.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# -------------------- TRANSACTION ANALYTICS --------------------

@api_view(['GET'])
@permission_classes([AllowAny])
def transaction_grouped_by_day(request, usr):
    today = timezone.localtime(timezone.now()).date()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    transactions = Transaction.objects.filter(user__username=usr, date__date__range=[start_of_week, end_of_week])
    grouped = defaultdict(lambda: {'income': Decimal(0), 'expense': Decimal(0)})

    for t in transactions:
        day = t.date.strftime('%a')
        if t.transaction_type.name == 'Income':
            grouped[day]['income'] += Decimal(t.amount)
        else:
            grouped[day]['expense'] += Decimal(t.amount)

    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    data = {
        "labels": days,
        "datasets": [{"data": list(zip([grouped[d]['income'] for d in days], [grouped[d]['expense'] for d in days]))}],
        "transactions": TransactionSerializer(transactions, many=True).data
    }
    return Response(data)


@api_view(['GET'])
@permission_classes([AllowAny])
def transaction_grouped_by_week(request, usr):
    today = timezone.localtime(timezone.now()).date()
    current_month = today.month
    current_year = today.year

    first_day = datetime(current_year, current_month, 1).date()
    last_day = (datetime(current_year, current_month + 1, 1) - timedelta(days=1)).date()

    weeks = []
    start = first_day - timedelta(days=first_day.weekday())
    while start <= last_day:
        end = min(start + timedelta(days=6), last_day)
        weeks.append((start, end))
        start = end + timedelta(days=1)

    grouped = defaultdict(lambda: {'income': Decimal(0), 'expense': Decimal(0)})
    transactions = Transaction.objects.filter(user__username=usr, date__date__range=[first_day, last_day])

    for t in transactions:
        for idx, (ws, we) in enumerate(weeks):
            if ws <= t.date.date() <= we:
                label = f"Week {idx + 1}"
                if t.transaction_type.name == 'Income':
                    grouped[label]['income'] += Decimal(t.amount)
                else:
                    grouped[label]['expense'] += Decimal(t.amount)
                break

    labels = [f"Week {i+1}" for i in range(len(weeks))]
    data = {
        "labels": labels,
        "datasets": [{"data": list(zip([grouped[l]['income'] for l in labels], [grouped[l]['expense'] for l in labels]))}],
        "transactions": TransactionSerializer(transactions, many=True).data
    }
    return Response(data)


@api_view(['GET'])
@permission_classes([AllowAny])
def transaction_grouped_by_month(request, usr):
    current_year = timezone.localtime(timezone.now()).year
    transactions = Transaction.objects.filter(user__username=usr, date__year=current_year)

    grouped = defaultdict(lambda: {'income': Decimal(0), 'expense': Decimal(0)})
    for t in transactions:
        month = t.date.strftime('%b')
        if t.transaction_type.name == 'Income':
            grouped[month]['income'] += Decimal(t.amount)
        else:
            grouped[month]['expense'] += Decimal(t.amount)

    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    data = {
        "labels": months,
        "datasets": [{"data": list(zip([grouped[m]['income'] for m in months], [grouped[m]['expense'] for m in months]))}],
        "transactions": TransactionSerializer(transactions, many=True).data
    }
    return Response(data)
