import pytest
from engine import Engine
from utils import log
from collections import defaultdict
from engine.account import default_account


# use monkey patch to substitute init and inject unit test data
def new_init(self, data):
    self._client_accounts = defaultdict(default_account)
    self._transactions = dict()
    self._data = data
    self._logger = log.get_log("tests")


@pytest.fixture()
def engine(monkeypatch, request):
    monkeypatch.setattr(Engine, "__init__", new_init)
    return Engine(request.param)
