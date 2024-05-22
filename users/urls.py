from django.urls import path

# from .views import MyTokenObtainPairView
from users.apps import UsersConfig
from users.views import UserRegisterView, UserUpdateView, UserRetrieveView, UserListView, \
    UserDeleteView

app_name = UsersConfig.name

urlpatterns = [
    path('create/', UserRegisterView.as_view(), name='users-create'),
    path('detail/<int:pk>/', UserRetrieveView.as_view(), name='user-detail'),
    path('update/<int:pk>/', UserUpdateView.as_view(), name='user-update'),
    path('delete/<int:pk>/', UserDeleteView.as_view(), name='user-delete'),
    path('users_list/', UserListView.as_view(), name='users_list'),

]