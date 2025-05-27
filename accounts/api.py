# Django imports
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login as auth_login, logout
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import redirect

# Python imports
import json
import pyotp
import random
import logging
from datetime import timedelta

# Project imports
from accounts.models import User, UserActionLog, TwoFactorCode

# Initialize logger
logger = logging.getLogger(__name__)


@require_POST
def register(request):
    # TODO: Implement registration logic
    return JsonResponse({'message': 'Register endpoint (stub)'})

@require_POST
def login(request):
    
    # Check if user is already logged in
    if request.user.is_authenticated:
        return JsonResponse({'message': 'You are already logged in.'}, status=200)
    
    try:
        data = json.loads(request.body.decode())
    except Exception:
        logger.error(f"Invalid JSON received from {request.META.get('REMOTE_ADDR')}")
        return JsonResponse({'error': 'Invalid JSON.'}, status=400)

    email = data.get('email')
    password = data.get('password')
    ip_address = request.META.get('REMOTE_ADDR')
    user_agent = request.META.get('HTTP_USER_AGENT', '')

    if not email or not password:
        logger.error(f"Missing email or password from {request.META.get('REMOTE_ADDR')}")
        return JsonResponse({'error': 'Email and password are required.'}, status=400)

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        # Log failed attempt
        UserActionLog.objects.create(
            user=None,
            static_user={'email': email},
            action='login_failed',
            details='User not found',
            ip_address=ip_address,
            user_agent=user_agent,
        )
        logger.error(f"User not found: {email} from {request.META.get('REMOTE_ADDR')}")
        return JsonResponse({'error': 'User not found.'}, status=401)

    if not user.is_active:
        UserActionLog.objects.create(
            user=user,
            static_user={'email': user.email, 'uuid': str(user.uuid)},
            action='login_failed',
            details='Inactive account',
            ip_address=ip_address,
            user_agent=user_agent,
        )
        logger.error(f"Inactive account: {email} from {request.META.get('REMOTE_ADDR')}")
        return JsonResponse({'error': 'Account is inactive.'}, status=403)

    if not user.check_password(password):
        UserActionLog.objects.create(
            user=user,
            static_user={'email': user.email, 'uuid': str(user.uuid)},
            action='login_failed',
            details='Incorrect password',
            ip_address=ip_address,
            user_agent=user_agent,
        )
        logger.error(f"Incorrect password: {email} from {request.META.get('REMOTE_ADDR')}")
        return JsonResponse({'error': 'Invalid credentials.'}, status=401)

    # 2FA check
    if user.tfa_enabled:
        # Determine available methods
        methods = []
        if user.tfa_secret:
            methods.append('totp')
        # Default to email, but could be SMS if phone is present
        if user.phone:
            methods.append('sms')
        methods.append('email')
        preferred = 'sms' if 'sms' in methods else 'email'
        logger.info(f"2FA required for {email} from {request.META.get('REMOTE_ADDR')}")
        return JsonResponse({
            'tfa_required': True,
            'methods': methods,
            'preferred': preferred,
            'user_uuid': str(user.uuid),
            'message': 'Two-factor authentication code required.'
        })

    # Success: log in
    auth_login(request, user)
    user.last_login = timezone.now()
    user.save(update_fields=['last_login'])
    UserActionLog.objects.create(
        user=user,
        static_user={'email': user.email, 'uuid': str(user.uuid)},
        action='login_success',
        details='Login successful',
        ip_address=ip_address,
        user_agent=user_agent,
    )
    logger.info(f"Login successful for {email} from {request.META.get('REMOTE_ADDR')}")
    return JsonResponse({'message': 'Login successful', 'user': {
        'uuid': str(user.uuid),
        'email': user.email,
        'full_name': user.full_name,
        'is_staff': user.is_staff,
        'role': user.role.name if user.role else None,
        'organization': user.organization.name if user.organization else None,
    }})


@csrf_exempt
@require_POST
def logout_api(request):
    logout(request)
    return JsonResponse({'message': 'Logout successful.'}) 


@require_POST
def forgot_password(request):
    # TODO: Implement forgot password logic
    return JsonResponse({'message': 'Forgot password endpoint (stub)'})


@require_POST
def reset_password(request):
    # TODO: Implement reset password logic
    return JsonResponse({'message': 'Reset password endpoint (stub)'})


@csrf_exempt
@require_POST
def verify_2fa(request):
    """
    Expects: user_uuid, method, code
    method: 'totp', 'sms', or 'email'
    """
    
    # Check if user is already logged in
    if request.user.is_authenticated:
        return JsonResponse({'message': 'You are already logged in.'}, status=200)
    
    # Try to parse JSON payload
    try:
        data = json.loads(request.body.decode())
    except Exception:
        logger.error(f"Invalid JSON received from {request.META.get('REMOTE_ADDR')}")
        return JsonResponse({'error': 'Invalid JSON.'}, status=400)
    
    # Extract data from payload
    user_uuid = data.get('user_uuid')
    method = data.get('method')
    code = data.get('code')
    ip_address = request.META.get('REMOTE_ADDR')
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    
    # Validate required fields
    if not user_uuid or not method or not code:
        logger.error(f"Missing required fields from {request.META.get('REMOTE_ADDR')}")
        return JsonResponse({'error': 'user_uuid, method, and code are required.'}, status=400)
    
    # Get user by UUID
    try:
        user = User.objects.get(uuid=user_uuid)
    except User.DoesNotExist:
        logger.error(f"User not found: {user_uuid} from {request.META.get('REMOTE_ADDR')}")
        return JsonResponse({'error': 'User not found.'}, status=404)
    
    # Check if 2FA is enabled
    if not user.tfa_enabled:
        logger.error(f"2FA not enabled for user: {user_uuid} from {request.META.get('REMOTE_ADDR')}")
        return JsonResponse({'error': '2FA is not enabled for this user.'}, status=400)
    
    # Handle TOTP verification
    if method == 'totp':
        if not user.tfa_secret:
            logger.error(f"TOTP not configured for user: {user_uuid} from {request.META.get('REMOTE_ADDR')}")
            return JsonResponse({'error': 'TOTP is not configured.'}, status=400)
        totp = pyotp.TOTP(user.tfa_secret)
        if totp.verify(code):
            auth_login(request, user)
            user.last_login = timezone.now()
            user.save(update_fields=['last_login'])
            UserActionLog.objects.create(
                user=user,
                static_user={'email': user.email, 'uuid': str(user.uuid)},
                action='login_success',
                details='2FA (TOTP) login successful',
                ip_address=ip_address,
                user_agent=user_agent,
            )
            return JsonResponse({'message': 'Login successful', 'user': {
                'uuid': str(user.uuid),
                'email': user.email,
                'full_name': user.full_name,
                'is_staff': user.is_staff,
                'role': user.role.name if user.role else None,
                'organization': user.organization.name if user.organization else None,
            }})
        else:
            UserActionLog.objects.create(
                user=user,
                static_user={'email': user.email, 'uuid': str(user.uuid)},
                action='login_failed',
                details='Invalid TOTP code',
                ip_address=ip_address,
                user_agent=user_agent,
            )
            return JsonResponse({'error': 'Invalid TOTP code.'}, status=401)
    elif method in ['sms', 'email']:
        # Find latest unused, unexpired code
        now = timezone.now()
        tfa_code = TwoFactorCode.objects.filter(user=user, method=method, used=False, expires_at__gt=now).order_by('-created_at').first()
        if not tfa_code or tfa_code.code != code:
            UserActionLog.objects.create(
                user=user,
                static_user={'email': user.email, 'uuid': str(user.uuid)},
                action='login_failed',
                details=f'Invalid {method} 2FA code',
                ip_address=ip_address,
                user_agent=user_agent,
            )
            return JsonResponse({'error': f'Invalid {method} 2FA code.'}, status=401)
        # Mark code as used
        tfa_code.used = True
        tfa_code.save(update_fields=['used'])
        auth_login(request, user)
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])
        UserActionLog.objects.create(
            user=user,
            static_user={'email': user.email, 'uuid': str(user.uuid)},
            action='login_success',
            details=f'2FA ({method}) login successful',
            ip_address=ip_address,
            user_agent=user_agent,
        )
        return JsonResponse({'message': 'Login successful', 'user': {
            'uuid': str(user.uuid),
            'email': user.email,
            'full_name': user.full_name,
            'is_staff': user.is_staff,
            'role': user.role.name if user.role else None,
            'organization': user.organization.name if user.organization else None,
        }})
    else:
        return JsonResponse({'error': 'Invalid 2FA method.'}, status=400)


@csrf_exempt
@require_POST
def send_2fa_code(request):
    """
    Expects: user_uuid, method
    Generates and sends a 6-digit code via email or SMS.
    """
    
    # Check if user is already logged in
    if request.user.is_authenticated:
        return JsonResponse({'message': 'You are already logged in.'}, status=200)
    
    try:
        data = json.loads(request.body.decode())
    except Exception:
        return JsonResponse({'error': 'Invalid JSON.'}, status=400)
    user_uuid = data.get('user_uuid')
    method = data.get('method')
    if not user_uuid or not method:
        return JsonResponse({'error': 'user_uuid and method are required.'}, status=400)
    try:
        user = User.objects.get(uuid=user_uuid)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found.'}, status=404)
    if not user.tfa_enabled:
        return JsonResponse({'error': '2FA is not enabled for this user.'}, status=400)
    # Generate code
    code = f"{random.randint(100000, 999999)}"
    expires_at = timezone.now() + timedelta(minutes=10)
    TwoFactorCode.objects.create(user=user, code=code, method=method, expires_at=expires_at)
    # Send code
    if method == 'email':
        send_mail(
            'Your CalmPOS Login Code',
            f'Your login code is: {code}',
            'no-reply@calmpos.com',
            [user.email],
            fail_silently=False,
        )
        return JsonResponse({'message': '2FA code sent via email.'})
    elif method == 'sms':
        # TODO: Integrate with SMS gateway
        # For now, just simulate
        print(f"Send SMS to {user.phone}: Your login code is {code}")
        return JsonResponse({'message': '2FA code sent via SMS (simulated).'})
    else:
        return JsonResponse({'error': 'Invalid 2FA method.'}, status=400)
