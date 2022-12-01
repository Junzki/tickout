# -*- coding:utf-8 -*-
import typing as ty
from email.message import Message
from email.header import decode_header
from tickout.log import LOG
from .parsers.cmb_transaction import CMBTransactionParser

RULES = [
    (
        dict(sender='95555@message.cmbchina.com',
             subject='一卡通账户变动通知'),
        CMBTransactionParser
    )
]


def dispatch(message: Message):
    headers = parse_headers(message)
    parser = match(headers)
    if not parser:
        LOG.warning("No matched rule for message: %s" % (', '.join(['%s=%s' % h for h in headers.items()])))
        return None

    return parser


def match(headers: ty.Dict[str, str]):
    for rule, p in RULES:
        matched = True
        for field, pattern in rule.items():
            v = headers.get(field)
            matched = (pattern == v)

        if matched:
            return p

    return None


def parse_headers(message: Message):
    sender = message.get('From')

    subject_raw = message.get('Subject')
    try:
        subject, charset = decode_header(subject_raw)[0]
        subject = subject.decode(charset)
    except Exception as e:
        LOG.error("Cannot parse subject: %s, error: %s" % (subject_raw, e))
        subject = ''

    return dict(sender=sender,
                subject=subject)
