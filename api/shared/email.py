from django.utils.log import AdminEmailHandler
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from constance import config
import mimetypes
import base64


def send_mail(context, subject, template_html, template_txt, to, provenance=None, files=[]):
    mail = EmailMultiAlternatives(
        "{} {}".format(config.EMAIL_SUBJECT_PREFIX, subject),
        render_to_string(template_txt, context),
        provenance if provenance else config.EMAIL_ADMIN,
        to,
    )
    if template_html:
        mail.attach_alternative(render_to_string(
            template_html, context), 'text/html')
    for index, file in enumerate(files):
        if isinstance(file, str):
            try:
                # file is a base64 encoded image
                name = "attachment{}.png".format(index)
                mail.attach(name, base64.b64decode(
                    file[file.find(",")+1:], validate=True), 'image/png')
            except:
                # file is a path to an uploaded file
                mail.attach_file(file)
        else:
            try:
                # file is a BytesIO (ex : pdf export)
                file_content = file.getvalue()
            except:
                file_content = file.read()
            mail.attach(file.name, file_content,
                        mimetypes.guess_type(file.name)[0])
    mail.send(fail_silently=False)


def mail_admins(subject, message):
    mail = EmailMultiAlternatives(
        "{} {}".format(config.EMAIL_SUBJECT_PREFIX, subject),
        message,
        config.EMAIL_ADMIN,
        [config.EMAIL_ADMIN],
    )
    mail.send(fail_silently=False)


class ConstanceAdminEmailHandler(AdminEmailHandler):
    '''usesdynamic constance settings instead of core django settings'''

    def send_mail(self,
                  subject,
                  message,
                  html_message=None,
                  fail_silently=False,
                  *args,
                  **kwargs):
        if not config.EMAIL_ADMIN:
            return
        subject = '%s%s' % (config.EMAIL_SUBJECT_PREFIX, subject)
        from_email = config.EMAIL_ADMIN
        to = [config.EMAIL_ADMIN]
        mail = EmailMultiAlternatives(
            subject,
            message,
            from_email,
            to,
            connection=self.connection(),
        )
        if html_message:
            mail.attach_alternative(html_message, 'text/html')
        mail.send(fail_silently=fail_silently)
