# -*- coding: utf-8 -*-
import csv
import sys
from . import log

# TODO: package csvvalidator might not be the best as it is not supported very much
# and looks like some methods are not python3 compatible. But it is doing the job for now.
from csvvalidator import *


def validate(file_path, headers):
    validator = CSVValidator(headers)
    validator.add_value_check("type", str, message="Type must be a string")
    validator.add_value_check("client", int, message="Client must be an integer")
    validator.add_value_check("tx", int, message="Transaction must be an integer")
    validator.add_value_check("amount", float, message="Amount must be float")
    with open(file_path) as csv_file:
        reader = csv.reader(csv_file, delimiter=",")
        problems = validator.validate(reader)
        if problems:
            logger = log.get_log("csv_validator")
            logger.info(msg=f"CSV failed schema validation: {problems}")
            logger.info(msg="Exiting...")
            sys.exit(1)
