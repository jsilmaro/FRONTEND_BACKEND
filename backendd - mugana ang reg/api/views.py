from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer
from accounts.serializers import UserSerializer
from accounts.models import CustomUser
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.hashers import check_password


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save(commit=False) #prevent premature saving
            user.set_password(serializer.validated_data["password"]) #hash pass correctly
            
            user.save() 

            refresh = RefreshToken.for_user(user)
            return Response({
                "token": str(refresh.access_token),
                "user": UserSerializer(user).data  # Uses serializer for structured response
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = CustomUser.objects.filter(email=email).first()
        if not user:
            return Response({"error": "User does not exist."}, status=status.HTTP_401_UNAUTHORIZED)

        print(f"Stored Password for {email}: {user.password}")  # Debugging
        password_matches = check_password(password, user.password)
        print(f"Password Match: {password_matches}")  # Debugging

        if not password_matches:
            return Response({"error": "Invalid password."}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        return Response({
            "token": str(refresh.access_token),
            "user": UserSerializer(user).data
        }, status=status.HTTP_200_OK)    

class LogoutView(APIView):
    def post(self, request):
        try:
            return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
        except:
            return Response({"error": "Logout failed."}, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_active_accounts(request):
    user = request.user
    active_accounts = [
        {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "avatar": user.avatar.url if user.avatar else None,
            "isActive": True  # Ensuring the logged-in user is marked as active
        }
    ]
    return Response(active_accounts, status=status.HTTP_200_OK)



<<<<<<< HEAD
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.db.models import Sum
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Transaction, Budget, Category
from .serializers import TransactionSerializer, BudgetSerializer, CategorySerializer

class TransactionViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        transactions = Transaction.objects.filter(user=request.user).order_by('-date')
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BudgetViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        budgets = Budget.objects.filter(user=request.user)
        serializer = BudgetSerializer(budgets, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BudgetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_summary(request):
    now = timezone.now()
    start_of_month = now.replace(day=1)
    
    # Calculate monthly totals
    monthly_income = Transaction.objects.filter(
        user=request.user,
        type='income',
        date__gte=start_of_month
    ).aggregate(total=Sum('amount'))['total'] or 0

    monthly_expenses = Transaction.objects.filter(
        user=request.user,
        type='expense',
        date__gte=start_of_month
    ).aggregate(total=Sum('amount'))['total'] or 0

    return Response({
        'total_income': monthly_income,
        'total_expenses': monthly_expenses,
        'current_balance': monthly_income - monthly_expenses,
        'monthly_change': 0  # Calculate based on previous month
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recent_transactions(request):
    transactions = Transaction.objects.filter(
        user=request.user
    ).order_by('-date')[:5]
    return Response(TransactionSerializer(transactions, many=True).data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def spending_by_category(request):
    start_date = request.query_params.get('start_date')
    end_date = request.query_params.get('end_date')
    
    transactions = Transaction.objects.filter(
        user=request.user,
        type='expense',
        date__range=[start_date, end_date]
    ).values('category__name').annotate(total=Sum('amount'))
    
    return Response(transactions)


=======
>>>>>>> cbfd5a5cd942fd8a2048e338c61911d4fb0d398d

