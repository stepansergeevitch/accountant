from datetime import datetime
from pycountry import currencies
from collections import namedtuple
from typing import Dict, Any

Account = namedtuple(
    "Account",
    [
        "id",
        "sendId",
        "currency",
        "cashbackType",
        "balance",
        "creditLimit",
        "maskedPan",
        "type",
        "iban",
    ],
)


def make_account(**kwargs: Dict[str, Any]) -> Account:
    if "currencyCode" in kwargs:
        kwargs["currency"] = currencies.get(
            numeric=str(kwargs["currencyCode"]),
        )
        del kwargs["currencyCode"]
    if "balance" in kwargs:
        kwargs["balance"] = kwargs["balance"] / 100.0
    if "creditLimit" in kwargs:
        kwargs["creditLimit"] = kwargs["creditLimit"] / 100.0

    try:
        return Account(**kwargs)
    except TypeError:
        print(kwargs)
        raise


Statement = namedtuple(
    "Statement",
    [
        "id",
        "time",
        "description",
        "mcc",
        "originalMcc",
        "amount",
        "operationAmount",
        "currency",
        "commissionRate",
        "cashbackAmount",
        "balance",
        "hold",
        "counterEdrpou",
        "counterIban",
        "receiptId",
        "comment",
    ],
)


def make_statement(**kwargs: Dict[str, Any]) -> Statement:
    if "amount" in kwargs:
        kwargs["amount"] = kwargs["amount"] / 100.0
    if "time" in kwargs:
        kwargs["time"] = datetime.fromtimestamp(kwargs["time"])
    if "currencyCode" in kwargs:
        kwargs["currency"] = currencies.get(
            numeric=str(kwargs["currencyCode"]),
        )
        del kwargs["currencyCode"]
    if "counterEdrpou" not in kwargs:
        kwargs["counterEdrpou"] = ""
    if "counterIban" not in kwargs:
        kwargs["counterIban"] = ""
    if "receiptId" not in kwargs:
        kwargs["receiptId"] = ""
    if "comment" not in kwargs:
        kwargs["comment"] = ""

    try:
        return Statement(**kwargs)
    except TypeError:
        print(kwargs)
        raise
