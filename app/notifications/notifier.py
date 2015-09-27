# -*- coding: utf-8 -*-

from django.core.mail import EmailMessage
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.generic import View
from django.template import Template, Context
import logging

from .models import NotificationTemplate, EmailContact, SMSContact

logger = logging.getLogger(__name__)


def send_notification(template, params):
    try:
        options = NotificationTemplate.objects.get(name=template)
    except NotificationTemplate.DoesNotExist:
        logger.error("Notification template with name %s does not exist." % template)
        return False

    if options.use_email:
        emails = list(EmailContact.objects.all().values_list('email', flat=True))
        if emails:
            msg = EmailMessage()
            msg.subject = options.email_subject.format(**params)
            msg.body = Template(options.email_template).render(Context(params))
            msg.from_email = options.email_from.format(**params)
            msg.to = emails
            msg.content_subtype = "html"
            sent_count = msg.send()
            logger.info("Sent %d notifications by email (%s)" % (sent_count, template))

    if options.use_sms:
        logger.error("Sending sms is not supported for now")
