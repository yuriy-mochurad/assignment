# QA Assignment

# Description 
This task is implementation of a simple dummy payment engine that processes the
payments accounts.
- Implemented with Python, using `csv` library for reading the input data.
- CSV schema is checked with `csvvalidator` lib (to be replaced once more time available.)
- Logging is generated in `./tmp` library using `structlog`. In general current state of logging should be improved, but it is good for debugging.
- Unit tests are implemented with `pytest` using monkeypatching technique to inject data.

## Requrements
- python >= 3.6

## Working environment
This solution is tested on macos 12.0.1 with python 3.8. But in general it should be cross platform solution

## Installation

1. Install `virtualenv`:

    `pip3 install virtualenv`

2. Create virtual environment:

    `python3 -m venv venv`

3. Activate virtual environment

    `source venv/bin/activate`
    
4. Install dependencies:

    `pip3 install -r requirements.txt`
    
Note: all the setup can be automated later

## Running tests

` python -m pytest tests`

Running the tests will generate the log under `./tmp/logs`.

## Running engine

`python3 payment_engine.py <path_to_csv>`

## Additional assumptions

- deposit and withdrawal transactions follow the same dispute process and impact the balances the same.
- If dispute on the transaction id is over and account is not locked - another dispute can occur

## Next steps

- add more unit tests
- improve logging
- Solution is not tested with big amounts of data. Reading everything, and storing everything in memory might not be the best solution. For reading we might need to use generator to yield one row at a time. For storing the already processed transactions TBD.
- Replace `csvvalidator` with more supported library (or fork and patch existing one)