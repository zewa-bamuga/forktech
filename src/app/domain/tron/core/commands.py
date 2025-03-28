from app.domain.tron.core.repositories import TronRepository
from app.domain.tron.core.schemas import TronDetails, TronCredentials


class TronCreateCommand:
    def __init__(
            self,
            repository: TronRepository,
     ) -> None:
        self.repository = repository

    async def __call__(self, payload: TronDetails) -> None:
         create_tron = TronDetails(
             address=payload.address,
             balance_trx=payload.balance_trx,
             bandwidth=payload.bandwidth,
             energy=payload.energy,
         )
         await self.repository.create_tron(create_tron)