import pytest


@pytest.mark.parametrize(
    "engine",
    [[{"type": "deposit", "client": "1", "tx": "1", "amount": "1.0"}]],
    indirect=True,
)
def test_deposit(engine):
    engine.run()
    assert engine.client_accounts["1"] == {
        "available": 1.0,
        "held": 0,
        "total": 1.0,
        "locked": False,
    }


@pytest.mark.parametrize(
    "engine",
    [
        [
            {"type": "deposit", "client": "1", "tx": "1", "amount": "3.0"},
            {"type": "withdrawal", "client": "1", "tx": "2", "amount": "1.5"},
        ]
    ],
    indirect=True,
)
def test_withdrawal(engine):
    engine.run()
    assert engine.client_accounts["1"] == {
        "available": 1.5,
        "held": 0,
        "total": 1.5,
        "locked": False,
    }


@pytest.mark.parametrize(
    "engine",
    [
        [
            {"type": "deposit", "client": "1", "tx": "1", "amount": "3.0"},
            {"type": "dispute", "client": "1", "tx": "1"},
        ]
    ],
    indirect=True,
)
def test_dispute(engine):
    engine.run()
    assert engine.client_accounts["1"] == {
        "available": 0,
        "held": 3.0,
        "total": 3.0,
        "locked": False,
    }


@pytest.mark.parametrize(
    "engine",
    [
        [
            {"type": "deposit", "client": "1", "tx": "1", "amount": "3.0"},
            {"type": "dispute", "client": "1", "tx": "1"},
            {"type": "resolve", "client": "1", "tx": "1"},
        ]
    ],
    indirect=True,
)
def test_resolve(engine):
    engine.run()
    assert engine.client_accounts["1"] == {
        "available": 3.0,
        "held": 0.0,
        "total": 3.0,
        "locked": False,
    }


@pytest.mark.parametrize(
    "engine",
    [
        [
            {"type": "deposit", "client": "1", "tx": "1", "amount": "3.0"},
            {"type": "dispute", "client": "1", "tx": "1"},
            {"type": "chargeback", "client": "1", "tx": "1"},
        ]
    ],
    indirect=True,
)
def test_chargeback(engine):
    engine.run()
    assert engine.client_accounts["1"] == {
        "available": 0.0,
        "held": 0.0,
        "total": 0.0,
        "locked": True,
    }


@pytest.mark.parametrize(
    "engine",
    [[{"type": "withdrawal", "client": "1", "tx": "2", "amount": "1.5"}]],
    indirect=True,
)
def test_withdraw_not_enough_money(engine):
    engine.run()
    assert engine.client_accounts["1"] == {
        "available": 0.0,
        "held": 0.0,
        "total": 0.0,
        "locked": False,
    }


@pytest.mark.parametrize(
    "engine",
    [
        [
            {"type": "deposit", "client": "1", "tx": "1", "amount": "1.0"},
            {"type": "deposit", "client": "1", "tx": "1", "amount": "1.0"},
        ]
    ],
    indirect=True,
)
def test_deposit_same_id_twice(engine):
    engine.run()
    assert engine.client_accounts["1"] == {
        "available": 1.0,
        "held": 0.0,
        "total": 1.0,
        "locked": False,
    }


# TODO: add more negative tests
