import decimal
import random

import factory
from faker import Faker

from app.domain.common import models
from tests import utils

fake = Faker()


class TronFactory(utils.AsyncSQLAlchemyModelFactory):
    address = factory.LazyAttribute(lambda _: fake.uuid4()[:34])
    bandwidth = factory.LazyAttribute(lambda _: random.randint(0, 10000))
    energy = factory.LazyAttribute(lambda _: random.randint(0, 10000))
    balance_trx = factory.LazyAttribute(
        lambda _: decimal.Decimal(random.uniform(0.0, 1000.0)).quantize(
            decimal.Decimal("0.000001")
        )
    )

    class Meta:
        model = models.Tron
