"""Converts python datetimes back to strings so the record is JSON Serializable"""

from decimal import Decimal
from typing import Dict


DATE_FORMAT = "%Y-%m-%d"
DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%LZ"


def transform_record(record: Dict, object_fields: Dict):
    transformed_record = {}
    for field, value in record.items():
        if value is None:
            transformed_record[field] = value
            continue

        object_type = object_fields.get(field)
        if object_type == "date":
            transformed_record[field] = value.strftime(DATE_FORMAT)
        elif object_type == "datetime":
            transformed_record[field] = value.strftime(DATETIME_FORMAT)
        elif isinstance(value, Decimal):
            # singer-sdk 0.40+ parses JSON numbers as Decimal; cast to float
            # so simple_salesforce's json.dumps() can serialize them
            transformed_record[field] = float(value)
        else:
            transformed_record[field] = value

    return transformed_record
