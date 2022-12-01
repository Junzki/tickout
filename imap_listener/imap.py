# -*- coding: utf-8 -*-
import email
import typing as ty

from email.header import decode_header
from email.generator import Generator
from imapclient import IMAPClient
from tickout.settings import settings
from tickout.log import LOG
from .dispatcher import dispatch


class IMAPDiscoverer(object):

    def __init__(self):
        self.host = settings.IMAP_SERVER
        self.port = settings.IMAP_PORT
        self.user = settings.IMAP_USER
        self.password = settings.IMAP_PASSWORD
        self.inbox = settings.IMAP_MAILBOX

        self._client: ty.Optional[IMAPClient] = None

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
        discovered = list()

        for uid, message_data in self.client.fetch(messages, "RFC822").items():
            message = email.message_from_bytes(message_data[b"RFC822"])
            sender = message.get("From")
            subject = decode_header(message.get('Subject'))
            LOG.info("Received from %(sender)s: %(subject)s", dict(sender=sender, subject=subject))

            parser_klass = dispatch(message)
            if not parser_klass:
                continue

            parser = parser_klass()
            result = parser.parse(message)
            if not result:
                continue

            print(uid, result.values())

        return discovered
