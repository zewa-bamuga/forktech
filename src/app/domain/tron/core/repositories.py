from a8t_tools.db.pagination import Paginated, PaginationCallable
from a8t_tools.db.sorting import SortingData
from a8t_tools.db.transactions import AsyncDbTransaction
from a8t_tools.db.utils import CrudRepositoryMixin

from app.domain.common import models
from app.domain.common.schemas import IdContainer
from app.domain.tron.core import schemas


class TronRepository(CrudRepositoryMixin[models.Tron]):
    def __init__(self, transaction: AsyncDbTransaction):
        self.model = models.Tron
        self.transaction = transaction

    async def create_tron(self, payload: schemas.TronDetails) -> IdContainer:
        return IdContainer(id=await self._create(payload))

    async def get_tron(
        self,
        pagination: PaginationCallable[schemas.TronDetailsFull] | None = None,
        sorting: SortingData[schemas.TronSorts] | None = None,
    ) -> Paginated[schemas.TronDetailsFull]:
        return await self._get_list(
            schemas.TronDetailsFull,
            pagination=pagination,
            sorting=sorting,
        )
