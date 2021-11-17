# -*- coding: utf-8 -*-
import time
import smtplib
import traceback
from dddd_utils.mail.oauth2 import get_oauth2_info, get_oauth_string
from dddd_utils.mail.headers import resolve_addresses, make_addr_alias_user
from dddd_utils.mail.validate import validate_email_with_regex
from dddd_utils.mail.password import handle_password
from dddd_utils.mail.message import prepare_message
from dddd_utils.mail.mail_exception import SendError


class UtilMail(object):
    def __init__(
            self,
            user=None,
            password=None,
            host="smtp.gmail.com",
            port=None,
            smtp_starttls=None,
            smtp_ssl=True,
            smtp_set_debuglevel=0,
            smtp_skip_login=False,
            encoding="utf-8",
            oauth2_file=None,
            soft_email_validation=True,
            **kwargs
    ):
        self.soft_email_validation = soft_email_validation
        if oauth2_file is not None:
            oauth2_info = get_oauth2_info(oauth2_file)
            if user is None:
                user = oauth2_info["email_address"]
        if smtp_skip_login and user is None:
            user = ""
        self.user, self.useralias = make_addr_alias_user(user)
        if soft_email_validation:
            validate_email_with_regex(self.user)
        self.is_closed = None
        self.host = host
        self.port = str(port) if port is not None else "465" if smtp_ssl else "587"
        self.smtp_starttls = smtp_starttls
        self.ssl = smtp_ssl
        self.smtp_skip_login = smtp_skip_login
        self.debuglevel = smtp_set_debuglevel
        self.encoding = encoding
        self.kwargs = kwargs
        self.cache = {}
        self.unsent = []
        self.num_mail_sent = 0
        self.oauth2_file = oauth2_file
        self.credentials = password if oauth2_file is None else oauth2_info

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self.is_closed:
            self.close()
        return False

    @property
    def connection(self):
        return smtplib.SMTP_SSL if self.ssl else smtplib.SMTP

    @property
    def starttls(self):
        if self.smtp_starttls is None:
            return False if self.ssl else True
        return self.smtp_starttls

    def prepare_send(
            self,
            to=None,
            subject=None,
            contents=None,
            attachments=None,
            cc=None,
            bcc=None,
            headers=None,
            prettify_html=True,
            message_id=None,
            group_messages=True,
    ):
        addresses = resolve_addresses(self.user, self.useralias, to, cc, bcc)

        if self.soft_email_validation:
            for email_addr in addresses["recipients"]:
                validate_email_with_regex(email_addr)

        msg = prepare_message(
            self.user,
            self.useralias,
            addresses,
            subject,
            contents,
            attachments,
            headers,
            self.encoding,
            prettify_html,
            message_id,
            group_messages,
        )

        recipients = addresses["recipients"]
        msg_string = msg.as_string()
        return recipients, msg_string

    def send(
            self,
            to=None,
            subject=None,
            contents=None,
            attachments=None,
            cc=None,
            bcc=None,
            preview_only=False,
            headers=None,
            prettify_html=True,
            message_id=None,
            group_messages=True,
    ):
        """ Use this to send an email with gmail"""
        for _ in range(3):
            try:
                self.login()
                recipients, msg_string = self.prepare_send(
                    to,
                    subject,
                    contents,
                    attachments,
                    cc,
                    bcc,
                    headers,
                    prettify_html,
                    message_id,
                    group_messages,
                )
                if preview_only:
                    return (recipients, msg_string)
                return self._attempt_send(recipients, msg_string)
            except:
                continue
        else:
            raise SendError(traceback.format_exc())

    def _attempt_send(self, recipients, msg_string):
        attempts = 0
        while attempts < 3:
            try:
                result = self.smtp.sendmail(self.user, recipients, msg_string)
                print("Message sent to %s", recipients)
                self.num_mail_sent += 1
                return result
            except smtplib.SMTPServerDisconnected as e:
                print(e)
                attempts += 1
                time.sleep(attempts * 3)
        self.unsent.append((recipients, msg_string))
        return False

    def send_unsent(self):
        """
        Emails that were not being able to send will be stored in :attr:`self.unsent`.
        Use this function to attempt to send these again
        """
        for i in range(len(self.unsent)):
            recipients, msg_string = self.unsent.pop(i)
            self._attempt_send(recipients, msg_string)

    def close(self):
        """ Close the connection to the SMTP server """
        self.is_closed = True
        try:
            self.smtp.quit()
        except (TypeError, AttributeError, smtplib.SMTPServerDisconnected):
            pass

    def login(self):
        if self.oauth2_file is not None:
            self._login_oauth2(self.credentials)
        else:
            self._login(self.credentials)

    def _login(self, password):
        """
        Login to the SMTP server using password. `login` only needs to be manually run when the
        connection to the SMTP server was closed by the user.
        """
        self.smtp = self.connection(self.host, self.port, **self.kwargs)
        self.smtp.set_debuglevel(self.debuglevel)
        if self.starttls:
            self.smtp.ehlo()
            if self.starttls is True:
                self.smtp.starttls()
            else:
                self.smtp.starttls(**self.starttls)
            self.smtp.ehlo()
        self.is_closed = False
        if not self.smtp_skip_login:
            password = self.handle_password(self.user, password)
            self.smtp.login(self.user, password)
        print("Connected to SMTP @ %s:%s as %s", self.host, self.port, self.user)

    @staticmethod
    def handle_password(user, password):
        return handle_password(user, password)

    @staticmethod
    def get_oauth_string(user, oauth2_info):
        return get_oauth_string(user, oauth2_info)

    def _login_oauth2(self, oauth2_info):
        if "email_address" in oauth2_info:
            oauth2_info.pop("email_address")
        self.smtp = self.connection(self.host, self.port, **self.kwargs)
        try:
            self.smtp.set_debuglevel(self.debuglevel)
        except AttributeError:
            pass
        auth_string = self.get_oauth_string(self.user, oauth2_info)
        self.smtp.ehlo(oauth2_info["google_client_id"])
        if self.starttls is True:
            self.smtp.starttls()
        self.smtp.docmd("AUTH", "XOAUTH2 " + auth_string)

    def feedback(self, message="Awesome features! You made my day! How can I contribute?"):
        """ Most important function. Please send me feedback :-) """
        self.send("kootenpv@gmail.com", "Yagmail feedback", message)


if __name__ == '__main__':
    a = UtilMail()
    a.send()
