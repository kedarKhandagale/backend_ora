from rest_framework import serializers
from .models import RoleType, UserRoleMapping
from django.contrib.auth import get_user_model
User = get_user_model()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class GetAllUserSerializer(serializers.ModelSerializer):
    role_names = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'created_date', 'role_names']

    def get_role_names(self, obj):
        return list(
            obj.user_roles.filter(role__is_active=True)
               .values_list('role__role_name', flat=True)
        )



class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    role_ids = serializers.ListField(
        child=serializers.PrimaryKeyRelatedField(queryset=RoleType.objects.filter(is_active=True)),
        write_only=True
    )

    class Meta:
        model = User
        fields = ['email', 'first_name', 'middle_name', 'last_name', 'password', 'role_ids', 'is_active']

    def create(self, validated_data):
        role_ids = validated_data.pop('role_ids')
        password = validated_data.pop('password')

        user = User(**validated_data)
        user.set_password(password)
        user.save()

        for role in role_ids:
            UserRoleMapping.objects.create(user=user, role=role)

        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    role_ids = serializers.ListField(
        child=serializers.PrimaryKeyRelatedField(queryset=RoleType.objects.filter(is_active=True)),
        write_only=True,
        required=False
    )
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['first_name', 'middle_name', 'last_name', 'is_active', 'role_ids', 'password']

    def update(self, instance, validated_data):
        role_ids = validated_data.pop('role_ids', None)
        password = validated_data.pop('password', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()

        if role_ids is not None:
            UserRoleMapping.objects.filter(user=instance).delete()
            for role in role_ids:
                UserRoleMapping.objects.create(user=instance, role=role)

        return instance
