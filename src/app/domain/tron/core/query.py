from decimal import Decimal

from a8t_tools.db.pagination import Paginated
from tronpy import Tron
from tronpy.exceptions import AddressNotFound
from tronpy.keys import is_address

from app.domain.tron.core import schemas
from app.domain.tron.core.repositories import TronRepository


class TronCredentialsQuery:
    def __init__(self, network: str = "mainnet"):
        self.client = Tron(network=network)

    def get_address_info(
        self, credentials: schemas.TronCredentials
    ) -> schemas.TronDetails:
        try:
            if not is_address(credentials.address):
                raise ValueError("Invalid Tron address format")

            account_info = self.client.get_account(credentials.address)

            return schemas.TronDetails(
                address=credentials.address,
                balance_trx=self._convert_sun_to_trx(account_info.get("balance", 0)),
                bandwidth=account_info.get("free_net_usage", 0),
                energy=account_info.get("account_resource", {}).get("energy_usage", 0),
            )
        except (
            AddressNotFound
        ):  # Добавлено для того, чтобы смотреть пустые кошельки (без этого вылезает ошибка, что кошелек не найден)
            return schemas.TronDetails(
                address=credentials.address,
                balance_trx=Decimal(0),
                bandwidth=0,
                energy=0,
            )

        except Exception as e:
            raise RuntimeError(f"Error fetching data: {str(e)}")

    def _convert_sun_to_trx(self, sun: int) -> Decimal:
        return Decimal(sun) / Decimal(1_000_000)


class TronListQuery:
    def __init__(self, repository: TronRepository):
        self.repository = repository

    async def __call__(
        self, payload: schemas.TronListRequestSchema
    ) -> Paginated[schemas.TronDetailsFull]:
        return await self.repository.get_tron(payload.pagination, payload.sorting)


class TronManagementListQuery:
    def __init__(self, query: TronListQuery) -> None:
        self.query = query

    async def __call__(
        self, payload: schemas.TronListRequestSchema
    ) -> Paginated[schemas.TronDetailsFull]:
        return await self.query(payload)
