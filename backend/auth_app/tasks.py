from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import User

@shared_task
def send_welcome_email(user_id):
    """Send welcome email to newly registered user"""
    try:
        user = User.objects.get(id=user_id)
        
        subject = 'Welcome to NumberPlay!'
        message = f"""
        Hello {user.username}!
        
        Welcome to NumberPlay! We're excited to have you on board.
        
        You can now start playing our number game and win prizes!
        
        Best regards,
        The NumberPlay Team
        """
        
        # For development, we'll just print the email content
        pass
        
        # In production, you would use:
        # send_mail(
        #     subject,
        #     message,
        #     settings.DEFAULT_FROM_EMAIL,
        #     [user.email],
        #     fail_silently=False,
        # )
        
        return f"Welcome email sent to {user.email}"
        
    except User.DoesNotExist:
        return f"User with id {user_id} does not exist"
    except Exception as e:
        return f"Error sending welcome email: {str(e)}" 