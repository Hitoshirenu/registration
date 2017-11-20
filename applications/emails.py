from django.conf import settings
from django.core import mail

from app import emails
from app.utils import reverse


def create_invite_email(application, request):
    c = {
        'name': application.user.get_full_name,
        'reimb': getattr(application.user, 'reimbursement', None),
        'confirm_url': str(reverse('confirm_app', request=request, kwargs={'id': application.uuid_str})),
        'cancel_url': str(reverse('cancel_app', request=request, kwargs={'id': application.uuid_str}))
    }
    return emails.render_mail('mails/invitation',
                              application.user.email, c)


def create_confirmation_email(application, request):
    c = {
        'name': application.user.get_full_name,
        'token': application.uuid_str,
        'qr_url': 'http://chart.googleapis.com/chart?cht=qr&chs=350x350&chl=%s'
                  % application.uuid_str,
        'cancel_url': str(reverse('cancel_app', request=request, kwargs={'id': application.uuid_str})),
    }
    return emails.render_mail('mails/confirmation',
                              application.user.email, c)


def create_lastreminder_email(application):
    c = {
        'name': application.user.get_full_name,
        # We need to make sure to redirect HTTP to HTTPS in production
        'confirm_url': 'http://%s%s' % (settings.EVENT_DOMAIN,
                                        reverse('confirm_app')),
        'cancel_url': 'http://%s%s' % (settings.EVENT_DOMAIN,
                                       reverse('cancel_app')),
    }
    return emails.render_mail('mails/last_reminder',
                              application.user.email, c)


def send_batch_emails(emails):
    connection = mail.get_connection()
    connection.send_messages(emails)