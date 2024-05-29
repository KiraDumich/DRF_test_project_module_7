
from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# from .views import MyTokenObtainPairView
from users.apps import UsersConfig
from users.views import UserRegisterView, UserUpdateView, UserRetrieveView, UserListView, \
    UserDeleteView, PaymentViewSet

app_name = UsersConfig.name
router = DefaultRouter()
router.register(r'payment', PaymentViewSet, basename='payment')

urlpatterns = [
    path('create/', UserRegisterView.as_view(), name='users-create'),
    path('detail/<int:pk>/', UserRetrieveView.as_view(), name='user-detail'),
    path('update/<int:pk>/', UserUpdateView.as_view(), name='user-update'),
    path('delete/<int:pk>/', UserDeleteView.as_view(), name='user-delete'),
    path('users_list/', UserListView.as_view(), name='users_list'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + router.urls
