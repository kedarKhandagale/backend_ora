from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, Group, Permission
from django.db import models
from django.conf import settings



class RoleType(models.Model):
    role_name = models.CharField(max_length=100)
    role_tag = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.role_name

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("User must have an email address")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if not extra_fields.get("is_staff"):
            raise ValueError("Superuser must have is_staff=True.")
        if not extra_fields.get("is_superuser"):
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=100, default="")
    middle_name = models.CharField(max_length=100, default="")
    last_name = models.CharField(max_length=100, default="")
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_verified = models.BooleanField(default=False)
 
    # Override groups and user_permissions with unique related_names
    groups = models.ManyToManyField(
        Group,
        related_name="core_auth_users",
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
        related_query_name="core_auth_user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="core_auth_users",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
        related_query_name="core_auth_user",
    )

    objects = UserManager()

    USERNAME_FIELD = "email"

    @property
    def formatted_created_date(self):
        return self.created_date.strftime("%d-%b-%y") if self.created_date else None

    @property
    def formatted_updated_date(self):
        return self.updated_date.strftime("%d-%b-%y") if self.updated_date else None

    @property
    def as_dict(self):
        return {
            "user_id": self.pk,
            "email": self.email,
            "first_name": self.first_name,
            "middle_name": self.middle_name,
            "last_name": self.last_name,
            "is_active": self.is_active,
            "created_date": self.formatted_created_date,
            "updated_date": self.formatted_updated_date,
            "is_verified": self.is_verified,
        }


class UserActiveToken(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    token = models.TextField()
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Active token for {self.user.email}"



class UserRoleMapping(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_roles")
    role = models.ForeignKey(RoleType, on_delete=models.CASCADE, related_name="role_users")

    class Meta:
        unique_together = ("user", "role")  # prevent duplicate mappings

    def __str__(self):
        return f"{self.user.email} -> {self.role.role_name}"