import enum
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from a8t_tools.db import pagination as pg
from a8t_tools.db import sorting as sr
from a8t_tools.schemas.pydantic import APIModel
from pydantic import BaseModel


class TronDetailsFull(APIModel):
    id: UUID
    address: str
    balance_trx: Decimal
    bandwidth: int
    energy: int
    created_at: datetime
    updated_at: datetime


class TronCredentials(APIModel):
    address: str


class TronDetails(BaseModel):
    address: str
    balance_trx: Decimal
    bandwidth: int
    energy: int


class TronSorts(enum.StrEnum):
    id = enum.auto()
    energy = enum.auto()
    bandwidth: enum.auto()
    balance_trx: enum.auto()
    created_at = enum.auto()


@dataclass
class TronListRequestSchema:
    pagination: pg.PaginationCallable[TronDetailsFull] | None = None
    sorting: sr.SortingData[TronSorts] | None = None
