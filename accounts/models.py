# Django imports
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, 
    PermissionsMixin, 
    BaseUserManager
)
from django.utils import timezone

# Python imports
import os
import uuid


def use_avatar_upload_path(instance, filename):
    """Custom upload path for user avatars."""
    
    # Get the user's UUID
    user_uuid = instance.user.uuid
    
    # Get the file extension
    ext = os.path.splitext(filename)[1]
    
    # Return the full path
    return f'avatars/{user_uuid}/{user_uuid}{ext}'

def organization_logo_upload_path(instance, filename):
    """Custom upload path for organization logos."""
    
    # Get the organization's UUID
    organization_uuid = instance.uuid
    
    # Get the file extension
    ext = os.path.splitext(filename)[1]
    
    # Return the full path
    return f'organizations/{organization_uuid}/{organization_uuid}{ext}'
    
class Organization(models.Model):
    """Represents a business organization or an individual account container."""
    
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    
    name = models.CharField(max_length=255)
    kra_pin = models.CharField(max_length=32, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    contact_phone = models.CharField(max_length=32, blank=True, null=True)
    logo = models.ImageField(upload_to=organization_logo_upload_path, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Role(models.Model):
    """Custom role for RBAC with string-based permissions."""
    
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    permissions = models.JSONField(default=list, help_text="List of permission string constants.")
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='roles', null=True, blank=True)
    # If null, this is a global role

    def __str__(self):
        return self.name

class UserManager(BaseUserManager):
    """Custom user manager for email login and superuser creation."""
    
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model for CalmPOS."""
    
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    
    # User details
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=32, blank=True, null=True)
    pin = models.CharField(max_length=128, blank=True, null=True, help_text="Hashed PIN for POS quick login.")
    rfid_tag = models.CharField(max_length=255, blank=True, null=True)
    
    # Account type
    account_type = models.CharField(max_length=20, choices=[('individual', 'Individual'), ('organization', 'Organization')], default='individual')
    organization = models.ForeignKey(Organization, null=True, blank=True, on_delete=models.SET_NULL, related_name='users')
    role = models.ForeignKey(Role, null=True, blank=True, on_delete=models.SET_NULL, related_name='users')
    
    # Overrides
    override_permissions = models.BooleanField(default=False)
    override_permissions_list = models.JSONField(default=list, help_text="List of permission string constants.")
    
    # Security settings
    tfa_enabled = models.BooleanField(default=False)
    tfa_secret = models.CharField(max_length=255, blank=True, null=True)
    force_password_reset = models.BooleanField(default=False)
    force_tfa_reset = models.BooleanField(default=False)

    # Status
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    # Timestamps
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.email

    def has_permission(self, perm):
        """Check if user has a given permission string."""
        if self.is_superuser:
            return True
        if self.role and perm in self.role.permissions:
            return True
        if self.override_permissions and perm in self.override_permissions_list:
            return True
        return False

class UserProfile(models.Model):
    """Additional user info and preferences."""
    
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to=use_avatar_upload_path, blank=True, null=True)
    # Add more profile fields as needed

class UserPreferences(models.Model):
    """Stores user-specific preferences as explicit fields."""
    
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='preferences')
    
    theme = models.CharField(max_length=32, default='light')
    receive_notifications = models.BooleanField(default=True)
    default_language = models.CharField(max_length=10, default='en')
    # Add more system-defined preference fields as needed
    
    def __str__(self):
        return f'{self.user.email}'

class OrganizationPreferences(models.Model):
    """Stores organization-wide preferences as explicit fields."""
    
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    
    organization = models.OneToOneField(Organization, on_delete=models.CASCADE, related_name='preferences')
    
    default_currency = models.CharField(max_length=10, default='KES')
    enable_vat = models.BooleanField(default=True)
    vat_rate = models.DecimalField(max_digits=5, decimal_places=2, default=16.00)
    # Add more system-defined preference fields as needed
    
    def __str__(self):
        return f'{self.organization.name}'

class PasswordResetToken(models.Model):
    """Tracks password reset tokens/codes for users."""
    
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reset_tokens')
    
    token = models.CharField(max_length=128, unique=True)
    used = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    
    def __str__(self):
        return f'{self.user.email} - {self.token} - {self.used}'

class UserActionLog(models.Model):
    """Detailed audit log for user actions."""
    
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='action_logs')
    static_user = models.JSONField(default=dict, blank=True) # Stored a static copy of the user object that can be used for auditing
    
    action = models.CharField(max_length=255)
    details = models.TextField(blank=True, null=True)
    
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.CharField(max_length=512, blank=True, null=True)
    
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user.email} - {self.action} - {self.timestamp}'

class TwoFactorCode(models.Model):
    """Stores system-generated 2FA codes for SMS/Email verification."""
    
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tfa_codes')
    code = models.CharField(max_length=6)
    method = models.CharField(max_length=10, choices=[('sms', 'SMS'), ('email', 'Email')], default='email')
    
    used = models.BooleanField(default=False)
    attempts = models.IntegerField(default=0) # Number of times the code has been used
    
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f'{self.user.email} - {self.code} - {self.method} - {self.used}'
