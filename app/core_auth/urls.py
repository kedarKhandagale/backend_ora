from django.urls import path
from .views import LoginView, UserDetailAPIView, UserListAPIView
from rest_framework_simplejwt.views import TokenRefreshView
from drf_spectacular.utils import extend_schema_view, extend_schema

#Swagger tags
LoginView = extend_schema_view(post=extend_schema(tags=["core_auth"]))(LoginView)
UserListAPIView = extend_schema_view(get=extend_schema(tags=["core_auth"]))(UserListAPIView)
UserDetailAPIView = extend_schema_view(get=extend_schema(tags=["core_auth"]))(UserDetailAPIView)

app_name = "user"  

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/', UserListAPIView.as_view(), name='user-list'),
    path('users/<int:user_id>/', UserDetailAPIView.as_view(), name='get-user-byID'),
]
