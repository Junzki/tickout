# -*- coding:utf-8 -*-
import datetime
import re
import typing as ty
import dataclasses

from email.message import Message

from tickout.exceptions import ParseError
from tickout.log import LOG


@dataclasses.dataclass
class Transaction:
    transaction_date: ty.Optional[datetime.datetime] = None
    account: str = ''
    explanation: str = ''
    debit: int = 0
    credit: int = 0
    balance: int = 0

    def values(self):
        return (self.transaction_date,
                self.account, self.explanation,
                self.debit, self.credit,
                self.balance)


class CMBTransactionParser(object):
    ALLOWED_CONTENT_TYPE = {
        'text/plain',
        'text/html'
    }

    PATTERNS = [
        # 快捷支付
        re.compile(r"您账户(?P<account>\d{4})于(?P<month>[01]\d)月(?P<day>[0-3]\d)日"
                   r"(?P<hour>[0-2]\d):(?P<minute>[0-6]\d)在【(?P<merchant>.+)】"
                   r"发生(?P<exchange_type>.+)(?P<entry>(扣款|收款|退款))，人民币(?P<value>\d+\.\d{0,2})，"
                   r"余额(?P<balance>\d+\.\d{0,2})"),

        # 银联提现
        re.compile(r"您账户(?P<account>\d{4})于(?P<month>[01]\d)月(?P<day>[0-3]\d)日"
                   r"(?P<hour>[0-2]\d):(?P<minute>[0-6]\d)(?P<exchange_type>.+)(?P<entry>(入账))"
                   r"人民币(?P<value>\d+\.\d{0,2})元，余额(?P<balance>\d+\.\d{0,2})元（(?P<explanation>.+)）"),

        # 绑定卡转入
        re.compile(r"您账户(?P<account>\d{4})于(?P<month>[01]\d)月(?P<day>[0-3]\d)日"
                   r"((?P<hour>[0-2]\d):(?P<minute>[0-6]\d))?收到(?P<exchange_type>.+)(?P<entry>(入账|转入))"
                   r"人民币(?P<value>\d+\.\d{0,2})元?，余额(?P<balance>\d+\.\d{0,2})元?，"
                   r"付方(?P<merchant>.*)，账号尾号(?P<merchant_account>\d{4})，备注：(?P<explanation>.+)"),

        # 他行转账
        re.compile(r"您账户(?P<account>\d{4})于(?P<month>[01]\d)月(?P<day>[0-3]\d)日"
                   r"((?P<hour>[0-2]\d):(?P<minute>[0-6]\d))?实时(?P<entry>(入账|转入|转至))(?P<exchange_type>他行)"
                   r"人民币(?P<value>\d+\.\d{0,2})元?，余额(?P<balance>\d+\.\d{0,2})元?，收款人(?P<merchant>.+)"),

        re.compile(r"您的?账户(?P<account>\d{4})于((?P<year>\d{4})年)?(?P<month>[01]\d)月(?P<day>[0-3]\d)日"
                   r"((?P<hour>[0-2]\d):(?P<minute>[0-6]\d))?(?P<exchange_type>他行)实时(?P<entry>(入账|转入))"
                   r"人民币(?P<value>\d+\.\d{0,2})元?，余额(?P<balance>\d+\.\d{0,2})元?，付方(?P<merchant>.+)"),

        # 信用卡还款
        re.compile(r"您账户(?P<account>\d{4})于(?P<month>[01]\d)月(?P<day>[0-3]\d)日"
                   r"((?P<hour>[0-2]\d):(?P<minute>[0-6]\d))?(?P<exchange_type>信用卡)(?P<entry>(还款))交易"
                   r"人民币(?P<value>\d+\.\d{0,2})元?，余额(?P<balance>\d+\.\d{0,2})元?"),

        # 预借现金
        re.compile(r"(?P<explanation>预借现金)入账通知，"
                   r"您的?账户(?P<account>\d{4})于((?P<year>\d{4})年)?(?P<month>[01]\d)月(?P<day>[0-3]\d)日"
                   r"((?P<hour>[0-2]\d):(?P<minute>[0-6]\d))?(?P<entry>(入账|转入))(金额)?"
                   r"人民币(?P<value>\d+\.\d{0,2})元?，余额(?P<balance>\d+\.\d{0,2})元?"),

        # Apple Pay
        re.compile(r"您账户(?P<account>\d{4})(（设备卡号\d{4}）)?于(?P<month>[01]\d)月(?P<day>[0-3]\d)日"
                   r"((?P<hour>[0-2]\d):(?P<minute>[0-6]\d))?线上免密(?P<entry>(支付))"
                   r"人民币(?P<value>\d+\.\d{0,2})元?，余额(?P<balance>\d+\.\d{0,2})元?，(?P<exchange_type>.+)，"
                   r"(?P<merchant>.+)"),

        # 支付宝提现
        re.compile(r"您账户(?P<account>\d{4})于(?P<month>[01]\d)月(?P<day>[0-3]\d)日"
                   r"((?P<hour>[0-2]\d):(?P<minute>[0-6]\d))?(?P<entry>(收款))"
                   r"人民币(?P<value>\d+\.\d{0,2})元?，余额(?P<balance>\d+\.\d{0,2})元?，"
                   r"备注：(?P<explanation>.+)，更多详情请查看招商银行APP动账通知。"),

        re.compile(r"您的?账户(?P<account>\d{4})于((?P<year>\d{4})年)?(?P<month>[01]\d)月(?P<day>[0-3]\d)日"
                   r"((?P<hour>[0-2]\d):(?P<minute>[0-6]\d))?(:\d{2})?(?P<entry>(扣款))(?P<explanation>(归还个贷))，"
                   r"人民币(?P<value>\d+\.\d{0,2})元?，余额(?P<balance>\d+\.\d{0,2})元?"),

        re.compile(r"您的?账户(?P<account>\d{4})于((?P<year>\d{4})年)?(?P<month>[01]\d)月(?P<day>[0-3]\d)日"
                   r"((?P<hour>[0-2]\d):(?P<minute>[0-6]\d))?(:\d{2})?(?P<entry>(入账))(?P<explanation>(工资))"
                   r"\((?P<merchant>.+)\)，人民币(?P<value>\d+\.\d{0,2})元?，余额(人民币)?(?P<balance>\d+\.\d{0,2})元?。")
    ]

    ENTRIES = {
        '扣款': 'credit',
        '转至': 'credit',
        '还款': 'credit',
        '支付': 'credit',
        '入账': 'debit',
        '转入': 'debit',
        '收款': 'debit',
        '退款': 'debit'
    }

    ACCOUNT_PREFIX = 'CMB'

    steps = ('account', 'transaction_date', 'explanation', 'entry', 'balance')

    @classmethod
    def _parse_account(cls, t: Transaction, groups: ty.Dict[str, ty.Any]) -> Transaction:
        account = '{}-{}'.format(cls.ACCOUNT_PREFIX, groups['account'])
        t.account = account
        return t

    @classmethod
    def _parse_transaction_date(cls, t: Transaction, groups: ty.Dict[str, ty.Any]) -> Transaction:
        month = int(groups['month'])
        day = int(groups['day'])
        hour = int(groups.get('hour') or 0)
        minute = int(groups.get('minute') or 0)
        transaction_date = datetime.datetime(year=datetime.date.today().year,
                                             month=month,
                                             day=day,
                                             hour=hour,
                                             minute=minute)
        t.transaction_date = transaction_date
        return t

    @classmethod
    def _parse_explanation(cls, t: Transaction, groups: ty.Dict[str, ty.Any]) -> Transaction:
        explanation = groups.get('explanation', '')
        exchange_type = groups.get('exchange_type', '')
        if exchange_type == '本行':
            exchange_type = cls.ACCOUNT_PREFIX

        if exchange_type == '信用卡':
            explanation = '还款'

        merchant = groups.get('merchant', '')
        merchant_account = groups.get('merchant_account', '')
        merchant = '-'.join((merchant, merchant_account)).strip('-')

        if not (explanation or explanation or merchant):
            raise ValueError("Transaction has no explanation")

        explanation = '::'.join((exchange_type, merchant, explanation)).strip('::')
        t.explanation = explanation

        return t

    @classmethod
    def _parse_entry(cls, t: Transaction, groups: ty.Dict[str, ty.Any]) -> Transaction:
        entry = cls.ENTRIES[groups['entry']]
        value = int(groups['value'].replace('.', ''))  # to cents

        setattr(t, entry, value)

        return t

    @classmethod
    def _parse_balance(cls, t: Transaction, groups: ty.Dict[str, ty.Any]) -> Transaction:
        balance = int(groups['balance'].replace('.', ''))
        t.balance = balance
        return t

    @classmethod
    def parse(cls, message: Message) -> Transaction:
        transaction = Transaction()

        payloads = message.get_payload()
        for p in payloads:
            type_ = p.get_content_type() or p.get_default_type()
            if type_ not in cls.ALLOWED_CONTENT_TYPE:
                continue

            transaction = cls._parse_payload(transaction, p)

        return transaction

    @classmethod
    def _parse_payload(cls, t: Transaction, payload: Message) -> ty.Optional[Transaction]:
        charset = payload.get_content_charset()

        try:
            content = payload.get_payload(decode=True)
            if not content:
                return t

            content = content.decode(charset)
        except Exception as e:
            raise ParseError(e)

        m = None
        for pattern in cls.PATTERNS:
            m = pattern.match(content)
            if m:
                break

        if not m:
            LOG.error("Missed match message: %s" % content)
            return None

        groups = m.groupdict()
        for step in cls.steps:
            step_method = getattr(cls, '_parse_%s' % step, None)
            if not step_method:
                continue

            try:
                t = step_method(t, groups)
            except Exception as e:
                raise ParseError(str(e))

        return t
