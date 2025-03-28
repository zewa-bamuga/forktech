from a8t_tools.db import pagination, sorting
from dependency_injector import wiring
from fastapi import APIRouter, Depends

from app.api import deps
from app.containers import Container
from app.domain.tron.core import schemas
from app.domain.tron.core.commands import TronCreateCommand
from app.domain.tron.core.query import TronCredentialsQuery, TronManagementListQuery

router = APIRouter()


@router.post("/create", response_model=None)
@wiring.inject
async def add_address(
    payload: schemas.TronCredentials,
    query: TronCredentialsQuery = Depends(
        wiring.Provide[Container.tron.tron_credentials_query]
    ),
    command: TronCreateCommand = Depends(wiring.Provide[Container.tron.create_command]),
):
    return await command(query.get_address_info(payload))


@router.get(
    "/get/list",
    response_model=pagination.CountPaginationResults[schemas.TronDetails],
)
@wiring.inject
async def get_tron_list(
    query: TronManagementListQuery = Depends(
        wiring.Provide[Container.tron.management_list_query]
    ),
    pagination: pagination.PaginationCallable[schemas.TronDetailsFull] = Depends(
        deps.get_skip_limit_pagination_dep(schemas.TronDetailsFull)
    ),
    sorting: sorting.SortingData[schemas.TronSorts] = Depends(
        deps.get_sort_order_sorting_dep(
            schemas.TronSorts,
            schemas.TronSorts.created_at,
            sorting.SortOrders.desc,
        )
    ),
) -> pagination.Paginated[schemas.TronDetailsFull]:
    return await query(
        schemas.TronListRequestSchema(pagination=pagination, sorting=sorting)
    )
