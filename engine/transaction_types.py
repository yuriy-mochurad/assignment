# -*- coding: utf-8 -*-
import enum


class TransactionTypesMeta(enum.EnumMeta):
    def __contains__(cls, item):
        try:
            cls(item)
        except ValueError:
            return False
        else:
            return True


class TransactionTypes(enum.Enum, metaclass=TransactionTypesMeta):
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    DISPUTE = "dispute"
    RESOLVE = "resolve"
    CHARGEBACK = "chargeback"
