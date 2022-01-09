# -*- coding: utf-8 -*-
import csv
from utils.csv_validator import validate
from utils import log
from collections import defaultdict
from .transaction_types import TransactionTypes
from .account import default_account

# TODO: convert to enum and use everywhere
HEADERS = ["type", "client", "tx", "amount"]


class Engine(object):
    def __init__(self, file_path):
        """
        Initializes Engine object.
        :param file_path (str): Path to a csv file to fetch data from
        """
        validate(file_path, HEADERS)
        with open(file_path) as csv_file:
            reader = csv.DictReader(
                csv_file, delimiter=",", fieldnames=HEADERS, skipinitialspace=True
            )
            self._data = [row for row in reader]
        self._client_accounts = defaultdict(default_account)
        self._transactions = dict()
        self._logger = log.get_log("csv_engine")

    @property
    def client_accounts(self):
        return self._client_accounts

    def _is_row_valid(self, row):
        """
        Basic checks if we can proceed with this row
        :param row (dict): Row to verify
        :return (bool):
        """
        if row and row["type"] in HEADERS:
            self._logger.info(msg="Skipping headers...")
            return False
        if row["type"].lower() not in TransactionTypes:
            self._logger.warn(msg=f"Skipping corrupted row: {row}")
            return False
        return True

    def _is_account_locked(self, row):
        if self._client_accounts[row["client"]]["locked"]:
            self._logger.info(
                msg=f"Skipping transaction as account is locked, row: {row}"
            )
            return True
        return False

    def _deposit(self, row):
        """
        Execute deposit transaction
        :param row (dict): transaction data
        :return:
        """
        if row["tx"] in self._transactions:
            self._logger.warn(
                msg=f"Transaction with the same id was already processed, skipping: {row}"
            )
            return
        amount = round(float(row["amount"]), 4)
        self._client_accounts[row["client"]]["available"] += amount
        self._client_accounts[row["client"]]["total"] += amount
        self._transactions[row["tx"]] = {
            "client": row["client"],
            "amount": amount,
            "type": row["type"],
            "disputed": False,
        }

    def _withdrawal(self, row):
        """
        Execute withdrawal transaction
        :param row (dict): transaction data
        :return:
        """
        if row["tx"] in self._transactions:
            self._logger.warn(
                msg=f"Transaction with the same id was already processed, skipping: {row}"
            )
            return
        amount = round(float(row["amount"]), 4)
        if self._client_accounts[row["client"]]["available"] < amount:
            self._logger.info(msg=f"Withdrawal failed for row: {row}")
            return
        self._client_accounts[row["client"]]["available"] -= amount
        self._client_accounts[row["client"]]["total"] -= amount
        self._transactions[row["tx"]] = {
            "client": row["client"],
            "amount": amount,
            "type": row["type"],
            "disputed": False,
        }

    def _dispute(self, row):
        """
        Start dispute process for transaction
        :param row (dict): transaction data
        :return:
        """
        # TODO: extract validations in dispute-like methods to avoid code duplication
        if row["tx"] not in self._transactions:
            self._logger.warn(
                msg=f"Dispute failed for row as transaction do not exist: {row}"
            )
            return
        if row["client"] != self._transactions[row["tx"]]["client"]:
            self._logger.warn(
                msg=f"Dispute client id do not match to client id in transaction: {row}"
            )
            return
        if self._transactions[row["tx"]]["disputed"]:
            self._logger.warn(msg=f"Dispute is already in progress: {row}")
            return
        self._logger.warn(msg="Disputing...")
        amount = self._transactions[row["tx"]]["amount"]
        self._client_accounts[row["client"]]["available"] -= amount
        self._client_accounts[row["client"]]["held"] += amount
        self._transactions[row["tx"]]["disputed"] = True

    def _resolve(self, row):
        """
        Resolve dispute process for transaction
        :param row (dict): transaction data
        :return:
        """
        if row["tx"] not in self._transactions:
            self._logger.warn(
                msg=f"Resolve failed for row as transaction do not exist: {row}"
            )
            return
        if row["client"] != self._transactions[row["tx"]]["client"]:
            self._logger.warn(
                msg=f"Resolve client id do not match to client id in transaction: {row}"
            )
            return
        if not self._transactions[row["tx"]]["disputed"]:
            self._logger.warn(msg=f"Dispute is not in progress: {row}")
            return
        amount = self._transactions[row["tx"]]["amount"]
        self._client_accounts[row["client"]]["available"] += amount
        self._client_accounts[row["client"]]["held"] -= amount
        self._transactions[row["tx"]]["disputed"] = False

    def _chargeback(self, row):
        if row["tx"] not in self._transactions:
            self._logger.warn(
                msg=f"Chargeback failed for row as transaction do not exist: {row}"
            )
            return
        if row["client"] != self._transactions[row["tx"]]["client"]:
            self._logger.warn(
                msg=f"Chargeback client id do not match to client id in transaction: {row}"
            )
            return
        if not self._transactions[row["tx"]]["disputed"]:
            self._logger.warn(msg=f"Dispute is not in progress: {row}")
            return
        amount = self._transactions[row["tx"]]["amount"]
        self._client_accounts[row["client"]]["total"] -= amount
        self._client_accounts[row["client"]]["held"] -= amount
        self._client_accounts[row["client"]]["locked"] = True
        self._transactions[row["tx"]]["disputed"] = False

    def run(self):
        for row in self._data:
            # validate
            if not self._is_row_valid(row):
                continue
            if self._is_account_locked(row):
                continue
            # execute
            if row["type"].lower() == TransactionTypes.DEPOSIT.value:
                self._deposit(row)
                continue
            elif row["type"].lower() == TransactionTypes.WITHDRAWAL.value:
                self._withdrawal(row)
                continue
            elif row["type"].lower() == TransactionTypes.DISPUTE.value:
                self._dispute(row)
                continue
            elif row["type"].lower() == TransactionTypes.RESOLVE.value:
                self._resolve(row)
                continue
            elif row["type"].lower() == TransactionTypes.CHARGEBACK.value:
                self._chargeback(row)
                continue
