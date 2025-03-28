import datetime
import decimal
import uuid

import sqlalchemy as sa
from sqlalchemy import Column, Integer, Numeric, String, orm
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func


@orm.as_declarative()
class Base:
    __tablename__: str

    id: orm.Mapped[uuid.UUID] = orm.mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    created_at: orm.Mapped[datetime.datetime] = orm.mapped_column(
        sa.DateTime(timezone=True), server_default=func.now()
    )
    updated_at: orm.Mapped[datetime.datetime] = orm.mapped_column(
        sa.DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class Tron(Base):
    __tablename__ = "tron"

    address = Column(String(34), unique=True, nullable=True, index=True)

    bandwidth = Column(Integer, default=0, nullable=True)

    energy = Column(Integer, default=0, nullable=True)

    balance_trx = Column(
        Numeric(20, 6), default=decimal.Decimal("0.000000"), nullable=True
    )
