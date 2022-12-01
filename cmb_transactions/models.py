# -*- coding:utf-8 -*-
import dataclasses
import datetime
import typing as ty


@dataclasses.dataclass
class Request:
    uid: ty.Optional[int] = None
    charset: ty.Optional[str] = None
    content_length: ty.Optional[int] = -1
    message: ty.Optional[ty.AnyStr] = None


@dataclasses.dataclass
class Transaction:
    transaction_date: ty.Optional[datetime.datetime] = None
    account: str = ''
    explanation: str = ''
    debit: int = 0
    credit: int = 0
    balance: int = 0
