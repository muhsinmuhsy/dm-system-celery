from auth_app.models import User

from celery import shared_task
from django.core.mail import send_mail
from dm_system import settings

from django.utils import timezone
from datetime import timedelta
from .models import Domain, ExpirationDate

from django.db.models import Min

from django_celery_beat.models import PeriodicTask, IntervalSchedule

@shared_task(bind=True)
def send_mail_func(self):
    users = User.objects.all()
    #timezone.localtime(users.date_time) + timedelta(days=2)
    for user in users:
        mail_subject = "Hi! Celery Testing"
        message = "Hi its Muhsy"
        to_email = user.email
        send_mail(
            subject = mail_subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[to_email],
            fail_silently=True,
        )
    return "Done"


# @shared_task
# def check_expiring_domains():
#     try:
#         tomorrow = timezone.now() + timedelta(days=1)
        
#         # Get the earliest expiration date for each domain
#         expiring_domains = ExpirationDate.objects.filter(expiration_date__date=tomorrow.date())
#         earliest_expirations = expiring_domains.values('domain').annotate(earliest_expiration=Min('expiration_date'))
        
#         if not earliest_expirations:
#             print("No domains expiring tomorrow.")
#             return "No domains expiring tomorrow."

#         for exp in earliest_expirations:
#             domain = Domain.objects.get(id=exp['domain'])
#             exp_date = exp['earliest_expiration']
            
#             try:
#                 user = domain.user
#                 mail_subject = 'Domain Expiry Notice'
#                 message = f'Dear {user.first_name},\n\nYour domain {domain.domain_name} is expiring on {exp_date}. Please renew it as soon as possible.'
#                 send_mail(
#                     subject=mail_subject,
#                     message=message,
#                     from_email=settings.EMAIL_HOST_USER,
#                     recipient_list=[user.email],
#                     fail_silently=True,
#                 )
#                 print(f"Mail sent to {user.email} regarding domain {domain.domain_name}.")
#             except Exception as e:
#                 print(f"Failed to send mail for domain {domain.domain_name}: {e}")

#     except Exception as e:
#         print(f"An error occurred while checking expiring domains: {e}")

#     return "Done"


@shared_task
def check_expiring_domains():
    try:
        # Get the current date and time
        now = timezone.now()

        # Iterate over each user
        for user in User.objects.all():
            # Get the notification preference in days
            notification_days = user.notification_preference
            notify_date = now + timedelta(days=notification_days)
            
            # Find all domains related to this user and filter by expiring domains
            expiring_domains = ExpirationDate.objects.filter(
                domain__user=user,
                expiration_date__date=notify_date.date()
            )
            
            # Ensure there are domains expiring on the notify_date
            if not expiring_domains.exists():
                print(f"No domains expiring in {notification_days} days for user {user.email}.")
                continue

            # Collect all unique domains to avoid multiple notifications for the same domain
            for exp in expiring_domains:
                domain = exp.domain
                exp_date = exp.expiration_date

                try:
                    mail_subject = 'Domain Expiry Notice'
                    message = f'Dear {user.first_name},\n\nYour domain {domain.domain_name} is expiring on {exp_date}. Please renew it as soon as possible.'
                    send_mail(
                        subject=mail_subject,
                        message=message,
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[user.email],
                        fail_silently=True,
                    )
                    print(f"Mail sent to {user.email} regarding domain {domain.domain_name}.")
                except Exception as e:
                    print(f"Failed to send mail for domain {domain.domain_name}: {e}")

    except Exception as e:
        print(f"An error occurred while checking expiring domains: {e}")

    return "Done"
