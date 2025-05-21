from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import GetAllUserSerializer, LoginSerializer, UserRegisterSerializer, UserUpdateSerializer
from django.contrib.auth import get_user_model
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from core_auth.custom_authentication import CustomTokenAuthentication
from .models import UserActiveToken


User = get_user_model()


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    # Save or update the latest token for the user
    UserActiveToken.objects.update_or_create(
        user=user,
        defaults={'token': access_token}
    )

    # Fetch active role names for the user
    role_names = list(
        user.user_roles.filter(role__is_active=True).values_list('role__role_name', flat=True)
    )

    return {
        'token': access_token,
        'role_names': role_names,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
    }

class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            user = authenticate(request, username=email, password=password)

            if user is not None:
                tokens = get_tokens_for_user(user)
                return Response(tokens, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRegisterView(APIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User registered successfully", "user": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserUpdateView(APIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, user_id):
        user = User.objects.filter(id=user_id).first()
        if not user:
            return Response({'detail': 'User not found'}, status=404)
        serializer = UserUpdateSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User updated successfully", "user": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserListAPIView(APIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        parameters=[
            OpenApiParameter("email", OpenApiTypes.STR, description="Filter by email", required=False),
            OpenApiParameter("first_name", OpenApiTypes.STR, description="Filter by first name", required=False),
            OpenApiParameter("last_name", OpenApiTypes.STR, description="Filter by last name", required=False),
        ]
    )
    def get(self, request):
        email = request.query_params.get('email')
        first_name = request.query_params.get('first_name')
        last_name = request.query_params.get('last_name')

        users = User.objects.all()

        # Apply filters if provided
        if email:
            users = users.filter(email__icontains=email)
        if first_name:
            users = users.filter(first_name__icontains=first_name)
        if last_name:
            users = users.filter(last_name__icontains=last_name)

        # Pagination setup
        paginator = PageNumberPagination()
        paginator.page_size = 10  # or use settings value
        result_page = paginator.paginate_queryset(users, request)

        serializer = GetAllUserSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)



class UserDetailAPIView(APIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, user_id):
        user = User.objects.filter(id=user_id).first()
        if not user:
            return Response({'detail': 'User not found'}, status=404)

        serializer = GetAllUserSerializer(user)
        return Response(serializer.data, status=200)