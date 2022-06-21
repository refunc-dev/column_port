from allauth.account.signals import email_confirmed
from allauth.socialaccount.signals import pre_social_login
from django.dispatch import receiver

from allauth.account.models import EmailAddress


@receiver(email_confirmed)
def email_confirmed_(request, email_address, **kwargs):
    user = email_address.user
    old_email = EmailAddress.objects.filter(user=user).exclude(email=email_address.email)
    if old_email.exists():
        user.email = email_address.email
        user.save()
        email_address.primary = True
        email_address.save()
        old_email.delete()
    else:
        pass


@receiver(pre_social_login)
def pre_social_login_(request, sociallogin, **kwargs):

    if sociallogin.is_existing:
        return

    if not sociallogin.email_addresses:
        return

    verified_email = None
    for email in sociallogin.email_addresses:
        if email.verified:
            verified_email = email
            break

    if not verified_email:
        return

    try:
        existing_email = EmailAddress.objects.get(email__iexact=email.email, verified=True)
    except EmailAddress.DoesNotExist:
        return

    sociallogin.connect(request, existing_email.user)