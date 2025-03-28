from app.domain.tron.core import schemas
from app.domain.tron.core.repositories import TronRepository


class TronCreateCommand:
    def __init__(
        self,
        repository: TronRepository,
    ) -> None:
        self.repository = repository

    async def __call__(self, payload: schemas.TronDetails) -> None:
        create_tron = schemas.TronDetails(
            address=payload.address,
            balance_trx=payload.balance_trx,
            bandwidth=payload.bandwidth,
            energy=payload.energy,
        )
        await self.repository.create_tron(create_tron)
