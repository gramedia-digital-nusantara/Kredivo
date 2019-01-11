from enum import Enum


class KredivoPaymentType(Enum):
    thirty_days = '30_days'
    three_months = '3_months'
    six_months = '6_months'
    twelve_months = '12_months'
