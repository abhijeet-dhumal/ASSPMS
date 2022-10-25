from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.conf import settings


class SendEmail:

    def __init__(self, templateName=str, data=dict, subject=str):
        self.template = templateName
        self.data = data
        self.subject = subject
        self.fail_silently = False

    def buildHtmlMessage(self, to_list, sender):
        msg_html = render_to_string(
            self.template, self.data
        )
        return msg_html

    def send(self, sendMailTo=None, sendMailFrom=None, **kwrgs):
        if not sendMailFrom:
            sendMailFrom = settings.DEFAULT_FROM_EMAIL

        if sendMailTo:
            try:
                send_mail(
                    self.subject,
                    "",
                    sendMailFrom,
                    sendMailTo,
                    fail_silently=self.fail_silently,
                    html_message=self.buildHtmlMessage(sendMailTo, sendMailFrom),
                )
                # print(send_mail)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
