# -*- encoding: utf-8 -*-

from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
from django.template.loader import get_template
from django.template import Context


def mail(title, body_txt, body_html, e_from, to):
    try:
        msg = EmailMultiAlternatives(title, body_txt, e_from, to)
        msg.attach_alternative(body_html, "text/html")
        msg.send()
        return True
    except Exception as e:
        print e.__class__, ' - ', e.message
    finally:
        return None
