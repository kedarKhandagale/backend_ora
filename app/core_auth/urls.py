from django.urls import path
from .views import LoginView, UserDetailAPIView, UserListAPIView, UserRegisterView, UserUpdateView
from rest_framework_simplejwt.views import TokenRefreshView
from drf_spectacular.utils import extend_schema_view, extend_schema

#Swagger tags
LoginView = extend_schema_view(post=extend_schema(tags=["core_auth"]))(LoginView)
UserRegisterView = extend_schema_view(post=extend_schema(tags=["core_auth"]))(UserRegisterView)
UserListAPIView = extend_schema_view(get=extend_schema(tags=["core_auth"]))(UserListAPIView)
UserDetailAPIView = extend_schema_view(get=extend_schema(tags=["core_auth"]))(UserDetailAPIView)

app_name = "user"  

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path("register/", UserRegisterView.as_view(), name="user-register"),
    path("update/<int:user_id>/", UserUpdateView.as_view(), name="user-update"),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/', UserListAPIView.as_view(), name='user-list'),
    path('users/<int:user_id>/', UserDetailAPIView.as_view(), name='get-user-byID'),
]
