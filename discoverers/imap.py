# -*- coding: utf-8 -*-
import email
import typing

from imapclient import IMAPClient
from tickout.settings import settings


class IMAPDiscoverer(object):

    def __init__(self):
        self.host = settings.IMAP_SERVER
        self.port = settings.IMAP_PORT
        self.user = settings.IMAP_USER
        self.password = settings.IMAP_PASSWORD
        self.inbox = settings.IMAP_MAILBOX

        self._client: typing.Optional[IMAPClient] = None

    @property
    def client(self):
        if not self._client:
            self._client = self.configure()

        return self._client

    def configure(self) -> IMAPClient:
        client = IMAPClient(self.host, port=self.port)
        client.login(self.user, self.password)

        client.select_folder(self.inbox, readonly=True)
        return client

    def discover(self):
        messages = self.client.search("UNSEEN")

        for uid, message_data in self.client.fetch(messages, "RFC822").items():
            email_message = email.message_from_bytes(message_data[b"RFC822"])
            print(uid, email_message.get("From"), email_message.get("Subject"))
