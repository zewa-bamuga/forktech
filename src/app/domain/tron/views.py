from dependency_injector import wiring
from fastapi import APIRouter, Depends

from a8t_tools.db import pagination, sorting

from app.api import deps
from app.containers import Container
from app.domain.tron.core.commands import TronCreateCommand
from app.domain.tron.core.query import TronCredentialsQuery, TronManagementListQuery
from app.domain.tron.core.schemas import TronCredentials, TronDetails, TronDetailsFull, TronSorts, TronListRequestSchema

router = APIRouter()


@router.post("/create", response_model=None)
@wiring.inject
async def add_address(
        payload: TronCredentials,
        query: TronCredentialsQuery = Depends(wiring.Provide[Container.tron.tron_credentials_query]),
        command: TronCreateCommand = Depends(wiring.Provide[Container.tron.create_command]),
):
    return await command(query.get_address_info(payload))


@router.get(
    "/get/list",
    response_model=pagination.CountPaginationResults[TronDetails],
)
@wiring.inject
async def get_tron_list(
        query: TronManagementListQuery = Depends(
            wiring.Provide[Container.tron.management_list_query]
        ),
        pagination: pagination.PaginationCallable[TronDetailsFull] = Depends(
            deps.get_skip_limit_pagination_dep(TronDetailsFull)
        ),
        sorting: sorting.SortingData[TronSorts] = Depends(
            deps.get_sort_order_sorting_dep(
                TronSorts,
                TronSorts.created_at,
                sorting.SortOrders.desc,
            )
        ),
) -> pagination.Paginated[TronDetailsFull]:
    return await query(
        TronListRequestSchema(pagination=pagination, sorting=sorting)
    )