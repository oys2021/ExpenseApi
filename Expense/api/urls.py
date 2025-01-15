from django.urls import path
from . import views
from rest_framework_simplejwt.views import ( # type: ignore
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('income_category_list/', views.income_category_list, name='income_category_list'),
    path('expense_category_list/', views.expense_category_list, name='expense_category_list'),
    path('wallets/<str:usr>/', views.wallet_list, name='wallets-list'),
    path('user_wallet_list/<str:usr>/', views.user_wallet_list, name='user_wallet_list'),
    path('wallet/<str:usr>/<int:pk>/', views.wallet_details, name='wallet-detail'),
    path('transaction-types/', views.transaction_type_list, name='transaction-type-list'),
    path('transaction-type/<int:pk>/', views.transaction_type_details, name='transaction-type-detail'),
    path('transaction-categories/', views.transaction_category_list, name='transaction-category-list'),
    path('transaction-category/<int:pk>/', views.transaction_category_details, name='transaction-category-detail'),
    path('transactions/<str:usr>/', views.transaction_list, name='transaction-list'),
    path('transactions_by_day/<str:usr>/', views.transaction_grouped_by_day, name='transactions_by_day'),
    path('transactions_by_week/<str:usr>/', views.transaction_grouped_by_week, name='transactions_by_week'),
    path('transactions_by_month/<str:usr>/', views.transaction_grouped_by_month, name='transactions_by_month'),
    path('transaction/<str:usr>/<int:pk>/', views.transaction_details, name='transaction-detail'),
    path('register/', views.user_list, name='register_user'),
    path('user/<str:usr>/', views.single_user_list, name='single_user'),
    path('login/', views.login_user, name='login_user'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/total-balance/<str:usr>/', views.user_total_balance, name='user-total-balance'),
]


# import axios from 'axios';

# // Login and obtain tokens
# export const login = async (username, password) => {
#     const response = await axios.post('http://your-api-url/api/token/', {
#         username,
#         password,
#     });
#     const { access, refresh } = response.data;
#     // Save tokens to AsyncStorage
#     await AsyncStorage.setItem('accessToken', access);
#     await AsyncStorage.setItem('refreshToken', refresh);
# };



# // Make an authenticated request
# export const fetchProtectedData = async () => {
#     const token = await AsyncStorage.getItem('accessToken');
#     const response = await axios.get('http://your-api-url/protected/', {
#         headers: {
#             Authorization: `Bearer ${token}`,
#         },
#     });
#     return response.data;
# };



# import React, { useEffect, useState } from 'react';
# import { View, Text, ActivityIndicator } from 'react-native';
# import AsyncStorage from '@react-native-async-storage/async-storage';
# import axios from 'axios';

# const ProtectedScreen = () => {
#     const [data, setData] = useState(null);
#     const [loading, setLoading] = useState(true);
#     const [error, setError] = useState(null);

#     useEffect(() => {
#         const fetchData = async () => {
#             try {
#                 const token = await AsyncStorage.getItem('accessToken');
#                 const response = await axios.get('http://your-api-url/protected/', {
#                     headers: {
#                         Authorization: `Bearer ${token}`,
#                     },
#                 });
#                 setData(response.data);
#             } catch (error) {
#                 setError(error);
#             } finally {
#                 setLoading(false);
#             }
#         };

#         fetchData();
#     }, []);

#     if (loading) {
#         return <ActivityIndicator size="large" color="#0000ff" />;
#     }

#     if (error) {
#         return <Text>Error: {error.message}</Text>;
#     }

#     return (
#         <View>
#             <Text>Protected Data:</Text>
#             <Text>{JSON.stringify(data)}</Text>
#         </View>
#     );
# };

# export default ProtectedScreen;
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def protected_view(request):
#     user = request.user
#     return Response({"message": f"Hello, {user.username}. This view is protected!"})
